import path from "node:path";
import { fileURLToPath } from "node:url";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const transport = new StdioClientTransport({
  command: "node",
  args: [path.join(__dirname, "governance_retrieval_server.mjs")]
});

const client = new Client({
  name: "governance-context-smoke",
  version: "0.1.0"
});

await client.connect(transport);
const tools = await client.listTools();
const result = await client.callTool({
  name: "governance_scope",
  arguments: {}
});
await client.close();

console.log(
  JSON.stringify(
    {
      tools: tools.tools.map((tool) => tool.name),
      result: result.content
    },
    null,
    2
  )
);
