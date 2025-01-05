import { z } from 'zod';
import { WabeeClient } from '../client';
import { ToolErrorType, ToolError } from './toolError';

export interface ToolOptions {
    host?: string;
    port?: number;
    useJson?: boolean;
}

export function simpleTool(
    toolName: string,
    schema?: z.ZodType,
    options: ToolOptions = {}
) {
    const client = new WabeeClient(
        options.host,
        options.port,
        options.useJson
    );

    return async function(input: any): Promise<[any, ToolError | null]> {
        // Validate input if schema is provided
        if (schema) {
            try {
                schema.parse(input);
            } catch (error) {
                return [null, new ToolError(
                    ToolErrorType.VALIDATION_ERROR,
                    error instanceof Error ? error.message : 'Invalid input',
                    error instanceof Error ? error : undefined
                )];
            }
        }

        const [result, error] = await client.execute(toolName, input);
        if (error) {
            return [null, new ToolError(
                error.type as ToolErrorType,
                error.message
            )];
        }
        return [result, null];
    };
}
