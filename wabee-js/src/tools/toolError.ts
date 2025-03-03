export enum ToolErrorType {
    RETRYABLE = 'retryable',
    PERMANENT = 'permanent',
    INVALID_INPUT = 'invalid_input',
    INTERNAL_ERROR = 'internal_error',
    VALIDATION_ERROR = 'validation_error',
    EXECUTION_ERROR = 'execution_error'
}

export interface ToolErrorResponse {
    type: string;
    message: string;
}

export class ToolError extends Error {
    constructor(
        public type: ToolErrorType,
        message: string,
        public originalError?: Error
    ) {
        super(message);
        this.name = 'ToolError';
    }
}
