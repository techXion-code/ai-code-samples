import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { readFileSync } from "node:fs";

const greetHtml = readFileSync("hello.html", "utf8");


// Create an MCP server
const server = new McpServer({
  name: "demo-app",
  version: "1.0.0",
});
   
server.registerResource(
    "greet-widget",
    "ui://widget/hello.html",
    {},
    async () => ({
      contents: [
        {
          uri: "ui://widget/hello.html",
          mimeType: "text/html+skybridge",
          text: greetHtml,
          _meta: { "openai/widgetPrefersBorder": true },
        },
      ],
    })
  );

server.registerTool(
  "greet_user",
  {
    title: "greet",
    description: "Greeting from ChatGPT app SDK.",
    inputSchema: { name: z.string().describe("Name of the user to greet") },
    _meta: {
        "openai/outputTemplate": "ui://widget/hello.html",
        "openai/toolInvocation/invoking": "greet the user with a friendly message",
        "openai/toolInvocation/invoked": "greeted the user with a friendly message",
      },
  },
  async (args) => {
    const title = args?.name?.trim?.() ?? "there";

    return {
      content: [{ type: "text", text: `Opening your UI greeting, ${title}!` }],
      // NOTE: ChatGPT maps 'structuredContent' to 'toolOutput'
      structuredContent: {
        name: title,
        message: `Hello, ${title}! Welcome to the app.`,
      },
    };
  }
);

export { server };
