import * as grpc from '@grpc/grpc-js';
import { ToolServiceClient } from './protos/tool_service';
import { ExecuteRequest, ExecuteResponse, GetToolSchemaRequest, ToolSchema } from './protos/tool_service';
import { ToolErrorResponse } from '../tools/toolError';

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
        const request: ExecuteRequest = {
            toolName,
            jsonData: this.useJson ? JSON.stringify(inputData) : undefined,
            protoData: !this.useJson ? Buffer.from(JSON.stringify(inputData)) : undefined
        };

        return new Promise((resolve) => {
            this.client.execute(request, (error, response) => {
                if (error) {
                    resolve([null, {
                        type: 'RPC_ERROR',
                        message: error.message
                    }]);
                    return;
                }

                if (response.error) {
                    resolve([null, {
                        type: response.error.type,
                        message: response.error.message
                    }]);
                    return;
                }

                try {
                    const result = this.useJson
                        ? JSON.parse(response.jsonResult ?? '')
                        : JSON.parse(Buffer.from(response.protoResult ?? '').toString());
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

    async close(): Promise<void> {
        this.client.close();
    }

    async getToolSchema(toolName: string): Promise<any> {
        const request: GetToolSchemaRequest = { toolName };
        
        return new Promise((resolve, reject) => {
            this.client.getToolSchema(request, (error, response) => {
                if (error) {
                    reject(error);
                    return;
                }
                
                resolve({
                    toolName: response.toolName,
                    description: response.description,
                    fields: response.fields.map(field => ({
                        name: field.name,
                        type: field.type,
                        required: field.required,
                        description: field.description
                    }))
                });
            });
        });
    }
}
