# @wabee_ai/sdk

JavaScript/TypeScript SDK for building and integrating Wabee AI tools.

## Installation

```bash
npm install @wabee_ai/sdk
```

## Quick Start

```typescript
import { simpleTool } from '@wabee_ai/sdk';
import { z } from 'zod';

// Define input schema
const additionSchema = z.object({
    x: z.number(),
    y: z.number()
});

// Create tool client
const add = simpleTool('addition', additionSchema, {
    host: 'localhost',
    port: 50051
});

// Use the tool
async function main() {
    const [result, error] = await add({ x: 5, y: 3 });
    if (error) {
        console.error('Error:', error);
    } else {
        console.log('Result:', result);
    }
}
```

## Features

- Simple tool creation with TypeScript support
- Input validation using Zod schemas
- gRPC communication with Wabee tools
- Comprehensive error handling
- JSON and Protocol Buffer support

## Documentation

For complete documentation, visit [https://documentation.wabee.ai](https://documentation.wabee.ai)

## License

MIT License - see LICENSE file for details
