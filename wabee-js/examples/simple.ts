import { simpleTool } from '../src';
import { z } from 'zod';

// Define schema for the tool
const additionSchema = z.object({
    x: z.number(),
    y: z.number()
});

// Create tool client
const addTool = simpleTool('addition', additionSchema, {
    host: 'localhost',
    port: 50051
});

// Use the tool
async function main() {
    const [result, error] = await addTool.execute({ x: 5, y: 3 });
    if (error) {
        console.error('Error:', error);
    } else {
        console.log('Result:', result);
    }
}

main().catch(console.error);
