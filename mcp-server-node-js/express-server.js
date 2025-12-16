
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import express from 'express';
import { server } from './mcp-server.js';

// Set up Express and HTTP transport
const app = express();
app.use(express.json());

app.post('/mcp', async (req, res) => {
    // Create a new transport for each request to prevent request ID collisions
    const transport = new StreamableHTTPServerTransport({
        sessionIdGenerator: undefined,
        enableJsonResponse: true
    });
    res.on('close', () => {
        transport.close();
    });
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body); 
});

const port = parseInt(process.env.PORT || '8080');

app.listen(port, () => {
    console.log(`MCP Server running on http://0.0.0.0:${port}/mcp`);
});