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

        try {
            const response = await this.client.execute(request);
            
            if (response.error) {
                return [null, {
                    type: response.error.type,
                    message: response.error.message
                }];
            }

            try {
                const result = this.useJson
                    ? JSON.parse(response.jsonResult ?? '')
                    : JSON.parse(Buffer.from(response.protoResult ?? '').toString());
                return [result, null];
            } catch (e) {
                return [null, {
                    type: 'PARSE_ERROR',
                    message: e instanceof Error ? e.message : 'Failed to parse response'
                }];
            }
        } catch (error) {
            return [null, {
                type: 'RPC_ERROR',
                message: error instanceof Error ? error.message : 'Unknown error occurred'
            }];
        }
    }

    async getToolSchema(toolName: string): Promise<any> {
        const request: GetToolSchemaRequest = { toolName };
        const response = await this.client.getToolSchema(request);
        
        return {
            toolName: response.toolName,
            fields: response.fields.map(field => ({
                name: field.name,
                type: field.type,
                required: field.required,
                description: field.description
            }))
        };
    }
}
