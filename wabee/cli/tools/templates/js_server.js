const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');
const { z } = require('zod');

// Load the tool
const toolName = process.env.WABEE_TOOL_NAME;
const tool = require('./dist').default;

// Convert Zod schema to tool schema format
function zodToToolSchema(schema) {
    if (!schema || !schema.shape) return [];
    
    return Object.entries(schema.shape).map(([name, field]) => {
        let type = 'string'; // default type
        let required = true;  // zod fields are required by default
        
        // Determine field type
        if (field instanceof z.ZodNumber) type = 'number';
        else if (field instanceof z.ZodBoolean) type = 'boolean';
        else if (field instanceof z.ZodArray) type = 'array';
        else if (field instanceof z.ZodObject) type = 'object';
        
        // Check if optional
        if (field instanceof z.ZodOptional) {
            required = false;
            // Get the inner type
            const innerType = field._def.innerType;
            if (innerType instanceof z.ZodNumber) type = 'number';
            else if (innerType instanceof z.ZodBoolean) type = 'boolean';
            else if (innerType instanceof z.ZodArray) type = 'array';
            else if (innerType instanceof z.ZodObject) type = 'object';
        }
        
        return {
            name,
            type,
            required,
            description: field.description || ''
        };
    });
}

// Load proto definition
const PROTO_PATH = path.resolve(__dirname, 'protos/tool_service.proto');
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
});

const protoDescriptor = grpc.loadPackageDefinition(packageDefinition);
const toolService = protoDescriptor.wabee.tools.ToolService;

// Implement the service
const server = new grpc.Server();
server.addService(toolService.service, {
    async execute(call, callback) {
        const { tool_name, input_data } = call.request;
        
        // Parse input based on format
        let parsedInput;
        try {
            if (call.request.json_data) {
                parsedInput = JSON.parse(call.request.json_data);
            } else if (call.request.proto_data) {
                parsedInput = JSON.parse(Buffer.from(call.request.proto_data).toString());
            } else {
                throw new Error('No input data provided');
            }
        } catch (err) {
            callback({
                code: grpc.status.INVALID_ARGUMENT,
                message: 'Failed to parse input data'
            });
            return;
        }

        try {
            const [result, error] = await tool(parsedInput);
            if (error) {
                callback(null, { 
                    error: {
                        type: error.type,
                        message: error.message
                    }
                });
            } else {
                // Support both JSON and protobuf responses
                const response = {};
                if (call.request.json_data) {
                    response.json_result = JSON.stringify(result);
                } else {
                    response.proto_result = Buffer.from(JSON.stringify(result));
                }
                callback(null, response);
            }
        } catch (err) {
            callback({
                code: grpc.status.INTERNAL,
                message: err.message
            });
        }
    },
    
    getToolSchema(call, callback) {
        try {
            // Get schema from the tool
            const schema = tool.schema;
            const fields = zodToToolSchema(schema);
            
            callback(null, {
                tool_name: toolName,
                fields: fields
            });
        } catch (err) {
            callback({
                code: grpc.status.INTERNAL,
                message: 'Failed to retrieve tool schema'
            });
        }
    }
});

// Start the server
const port = process.env.PORT || 50051;
server.bindAsync(
    `0.0.0.0:${port}`,
    grpc.ServerCredentials.createInsecure(),
    (err, port) => {
        if (err) {
            console.error('Failed to start server:', err);
            process.exit(1);
        }
        console.log(`Server running at 0.0.0.0:${port}`);
        server.start();
    }
);
