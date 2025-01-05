import * as grpc from '@grpc/grpc-js';
import { ToolServiceClient } from './protos/tool_service_grpc_pb';
import { wabee } from './protos/tool_service';
import { ToolErrorResponse } from '../tools/toolError';

// Type aliases for convenience
type ExecuteRequest = wabee.tools.ExecuteRequest;
type ExecuteResponse = wabee.tools.ExecuteResponse;
type GetToolSchemaRequest = wabee.tools.GetToolSchemaRequest;
type ToolSchema = wabee.tools.ToolSchema;

export class WabeeClient {
    private client: ToolServiceClient;

    constructor(
        host: string = 'localhost',
        port: number = 50051,
        private useJson: boolean = true
    ) {
        this.client = new ToolServiceClient(
            `${host}:${port}`,
            grpc.credentials.createInsecure()
        );
    }

    async execute(toolName: string, inputData: any): Promise<[any, ToolErrorResponse | null]> {
        return new Promise((resolve, reject) => {
            const request = new ExecuteRequest();
            request.setToolName(toolName);

            if (this.useJson) {
                request.setJsonData(JSON.stringify(inputData));
            } else {
                request.setProtoData(Buffer.from(JSON.stringify(inputData)));
            }

            this.client.execute(request, (error, response) => {
                if (error) {
                    resolve([null, {
                        type: 'RPC_ERROR',
                        message: error.message
                    }]);
                    return;
                }

                if (response.hasError()) {
                    resolve([null, {
                        type: response.getError()?.getType() || 'UNKNOWN_ERROR',
                        message: response.getError()?.getMessage() || 'Unknown error occurred'
                    }]);
                    return;
                }

                try {
                    const result = this.useJson
                        ? JSON.parse(response.getJsonResult())
                        : JSON.parse(response.getProtoResult_asU8().toString());
                    resolve([result, null]);
                } catch (e) {
                    resolve([null, {
                        type: 'PARSE_ERROR',
                        message: e instanceof Error ? e.message : 'Failed to parse response'
                    }]);
                }
            });
        });
    }

    async getToolSchema(toolName: string): Promise<any> {
        return new Promise((resolve, reject) => {
            const request = new GetToolSchemaRequest();
            request.setToolName(toolName);

            this.client.getToolSchema(request, (error, response: ToolSchema) => {
                if (error) {
                    reject(error);
                    return;
                }

                const schema = {
                    toolName: response.getToolName(),
                    fields: response.getFieldsList().map(field => ({
                        name: field.getName(),
                        type: field.getType(),
                        required: field.getRequired(),
                        description: field.getDescription()
                    }))
                };

                resolve(schema);
            });
        });
    }
}
