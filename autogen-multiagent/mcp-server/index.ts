import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
    CallToolRequestSchema,
    ListToolsRequestSchema,
    ToolSchema,
} from "@modelcontextprotocol/sdk/types.js";
import fs from "fs/promises";
import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";
import logger from './logger';

const ToolInputSchema = ToolSchema.shape.inputSchema;
type ToolInput = z.infer<typeof ToolInputSchema>;

// Server setup
const server = new Server(
    {
        name: 'manager',
        version: '0.1.0',
    },
    {
        capabilities: {
            tools: {},
        },
    },
);

const ParamsArgsSchema = z.object({
    a: z.number().describe("First number"),
    b: z.number().describe("Second number"),
});

const TableNameArgsSchema = z.object({
    tableName: z.string().describe("Table name"),
});

server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
        tools: [
            {
                name: "add",
                description:
                    "Add two numbers",
                inputSchema: zodToJsonSchema(ParamsArgsSchema) as ToolInput,
            },
            {
                name: "subtract",
                description:
                    "subtract two numbers",
                inputSchema: zodToJsonSchema(ParamsArgsSchema) as ToolInput,
            },
            {
                name: "multiply",
                description:
                    "multiply two numbers",
                inputSchema: zodToJsonSchema(ParamsArgsSchema) as ToolInput,
            },
            {
                name: "divide",
                description:
                    "divide two numbers",
                inputSchema: zodToJsonSchema(ParamsArgsSchema) as ToolInput,
            },
            {
                name: "tableschema",
                description: "Get the schema for a table",
                inputSchema: zodToJsonSchema(TableNameArgsSchema) as ToolInput,
            }
        ]
    }
});

const MockGetTableSchema = (tableName: string): string => {
    if (!tableName) {
        return `Table ${tableName} not found`;
    }
    tableName = tableName.toLowerCase().trim();
    switch (tableName) {
        case "events":
            return "cluster: north.kusto.windows.net, table: events, fields: [id:string,ts:timestamp,type:string,userid:string,systemid:string], types: [infra,code,change]";
        case "users":
            return "cluster: north.kusto.windows.net, table: users, fields: [userid:string,name:string,email:string,lastts:timestamp]";
        case "systems":
            return "cluster: south.kusto.windows.net, table: systems, fields: [systemid:string,name:string,description:string]";
        default:
            return `Table ${tableName} not found`;
    }
}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
    try {
        const { name, arguments: args } = request.params;
        switch (name) {
            case "add": {
                const parsed = ParamsArgsSchema.safeParse(args);
                if (!parsed.success) {
                    throw new Error(`Invalid arguments for read_file: ${parsed.error}`);
                }
                const { a, b } = parsed.data;
                const result = a + b;
                const content = `The result of adding ${a} and ${b} is ${result}`;
                return {
                    content: [{ type: "text", text: content }],
                };
            }
            case "subtract": {
                const parsed = ParamsArgsSchema.safeParse(args);
                if (!parsed.success) {
                    throw new Error(`Invalid arguments for read_file: ${parsed.error}`);
                }
                const { a, b } = parsed.data;
                const result = a + b;
                const content = `The result of subtracting ${b} from ${a} is ${result}`;
                return {
                    content: [{ type: "text", text: content }],
                };
            }
            case "multiply": {
                const parsed = ParamsArgsSchema.safeParse(args);
                if (!parsed.success) {
                    throw new Error(`Invalid arguments for read_file: ${parsed.error}`);
                }
                const { a, b } = parsed.data;
                const result = a * b;
                const content = `The result of multiplying ${a} and ${b} is ${result}`;
                return {
                    content: [{ type: "text", text: content }],
                };
            }
            case "divide": {
                const parsed = ParamsArgsSchema.safeParse(args);
                if (!parsed.success) {
                    throw new Error(`Invalid arguments for read_file: ${parsed.error}`);
                }
                const { a, b } = parsed.data;
                if (b === 0) {
                    throw new Error("Division by zero is not allowed.");
                }
                const result = a / b;
                const content = `The result of dividing ${a} by ${b} is ${result}`;
                return {
                    content: [{ type: "text", text: content }],
                };
            }
            case "tableschema": {
                const parsed = TableNameArgsSchema.safeParse(args);
                if (!parsed.success) {
                    throw new Error(`Invalid arguments for read_file: ${parsed.error}`);
                }
                const content = MockGetTableSchema(parsed.data.tableName);
                return {
                    content: [{ type: "text", text: content }],
                };
            }
            default:
                throw new Error(`Unknown tool: ${name}`);
        }

    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        return {
            content: [{ type: "text", text: `Error: ${errorMessage}` }],
            isError: true,
        };
    }
});


async function startServer() {
    logger.info('Initializing server...');
    const transport = new StdioServerTransport();

    try {
        logger.info('Connecting to transport...');
        await server.connect(transport);
        logger.info('Server started successfully');
    } catch (err) {
        logger.fatal('Failed to start server', {
            error: err instanceof Error ? err.message : String(err),
            stack: err instanceof Error ? err.stack : undefined,
        });
        process.exit(1);
    }
}

startServer().catch(console.error);