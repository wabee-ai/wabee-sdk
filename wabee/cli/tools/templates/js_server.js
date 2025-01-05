const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

// Load the tool
const toolName = process.env.WABEE_TOOL_NAME;
const tool = require('./src').default;

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
const toolService = protoDescriptor.wabee.ToolService;

// Implement the service
const server = new grpc.Server();
server.addService(toolService.service, {
    async execute(call, callback) {
        const { tool_name, input } = call.request;
        try {
            const [result, error] = await tool(input);
            if (error) {
                callback(null, { error });
            } else {
                callback(null, { result: JSON.stringify(result) });
            }
        } catch (err) {
            callback({
                code: grpc.status.INTERNAL,
                message: err.message
            });
        }
    },
    
    getToolSchema(call, callback) {
        // TODO: Implement schema retrieval
        callback(null, {
            tool_name: toolName,
            fields: []
        });
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
