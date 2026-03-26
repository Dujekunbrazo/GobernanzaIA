import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import {
  GOVERNANCE_EXCLUDE,
  GOVERNANCE_INCLUDE,
  collectFiles,
  computeSignature,
  cosineSimilarity,
  embedTexts,
  governanceCategory,
  loadEmbeddingCache,
  loadIndex,
  motorFromPath,
  phasesFromText,
  readText,
  repoPath,
  saveEmbeddingCache,
  saveIndex,
  scoreLexical,
  splitMarkdownSections,
  summarizeChunk
} from "./shared.mjs";

const INDEX_PATH = repoPath("state/context_retrieval/governance_index.json");

function fileAllowed(relativePath) {
  return relativePath.toLowerCase().endsWith(".md");
}

function buildGovernanceChunks(files) {
  const chunks = [];
  for (const file of files) {
    const text = readText(file.absolutePath);
    const sections = splitMarkdownSections(text);
    const category = governanceCategory(file.relativePath);
    const motor = motorFromPath(file.relativePath);
    for (const section of sections) {
      const chunkText = section.text.trim();
      if (!chunkText) {
        continue;
      }
      const phases = phasesFromText(chunkText);
      chunks.push({
        id: `${file.relativePath}#${section.ordinal}`,
        relativePath: file.relativePath,
        category,
        motor,
        header: section.header,
        phases,
        text: chunkText
      });
    }
  }
  return chunks;
}

async function embedWithCache(items) {
  const cache = loadEmbeddingCache("governance");
  const pending = [];
  for (const item of items) {
    const key = item.id;
    if (cache[key]) {
      item.embedding = cache[key];
    } else {
      pending.push(item);
    }
  }
  if (pending.length) {
    const vectors = await embedTexts(pending.map((item) => item.text));
    pending.forEach((item, index) => {
      cache[item.id] = vectors[index];
      item.embedding = vectors[index];
    });
    saveEmbeddingCache("governance", cache);
  }
  return items;
}

async function loadOrBuildIndex() {
  const files = collectFiles(GOVERNANCE_INCLUDE, GOVERNANCE_EXCLUDE, fileAllowed);
  const signature = computeSignature(files, "governance_semantic_v1");
  const current = loadIndex(INDEX_PATH);
  if (current && current.signature === signature) {
    return current;
  }
  const chunks = await embedWithCache(buildGovernanceChunks(files));
  const index = {
    signature,
    generatedAt: new Date().toISOString(),
    include: GOVERNANCE_INCLUDE,
    exclude: GOVERNANCE_EXCLUDE,
    files: files.map((file) => file.relativePath),
    chunks
  };
  saveIndex(INDEX_PATH, index);
  return index;
}

const server = new McpServer({
  name: "governance-retrieval",
  version: "0.1.0"
});

server.tool(
  "governance_search",
  {
    query: z.string().min(3),
    phase: z.string().regex(/^F[1-9]$/).optional(),
    document_type: z.string().optional(),
    motor: z.string().optional(),
    limit: z.number().int().min(1).max(10).default(5)
  },
  async ({ query, phase = "", document_type = "", motor = "", limit = 5 }) => {
    const index = await loadOrBuildIndex();
    const [queryVector] = await embedTexts([query]);
    const filtered = index.chunks.filter((chunk) => {
      if (phase && !chunk.phases.includes(phase) && chunk.category !== "workflow") {
        return false;
      }
      if (document_type && chunk.category !== document_type) {
        return false;
      }
      if (motor && chunk.motor && chunk.motor !== motor) {
        return false;
      }
      if (motor && !chunk.motor && chunk.category === "adapters") {
        return false;
      }
      return true;
    });

    const scored = filtered
      .map((chunk) => {
        const semantic = cosineSimilarity(queryVector, chunk.embedding);
        const lexical = scoreLexical(query, chunk.text, `${chunk.relativePath}\n${chunk.header}`);
        return {
          ...chunk,
          score: semantic * 0.8 + lexical * 0.2,
          semantic: Number(semantic.toFixed(4)),
          lexical: Number(lexical.toFixed(4))
        };
      })
      .sort((a, b) => b.score - a.score)
      .slice(0, limit)
      .map((chunk) => ({
        relativePath: chunk.relativePath,
        category: chunk.category,
        motor: chunk.motor || null,
        phases: chunk.phases,
        header: chunk.header,
        score: Number(chunk.score.toFixed(4)),
        semantic: chunk.semantic,
        lexical: chunk.lexical,
        snippet: summarizeChunk(chunk.text)
      }));

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(
            {
              query,
              filters: {
                phase: phase || null,
                document_type: document_type || null,
                motor: motor || null
              },
              scope: {
                include: index.include,
                exclude: index.exclude
              },
              results: scored
            },
            null,
            2
          )
        }
      ]
    };
  }
);

server.tool("governance_scope", {}, async () => {
  const index = await loadOrBuildIndex();
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(
          {
            include: index.include,
            exclude: index.exclude,
            fileCount: index.files.length,
            chunkCount: index.chunks.length
          },
          null,
          2
        )
      }
    ]
  };
});

const transport = new StdioServerTransport();
await server.connect(transport);
