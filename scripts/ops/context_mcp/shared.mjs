import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
import dotenv from "dotenv";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const REPO_ROOT = path.resolve(__dirname, "..", "..", "..");
export const STATE_DIR = path.join(REPO_ROOT, "state", "context_retrieval");
const ENV_PATH = path.join(REPO_ROOT, ".env");

dotenv.config({ path: ENV_PATH });

export const GOVERNANCE_INCLUDE = [
  "dev/policies",
  "dev/guarantees",
  "dev/prompts",
  "dev/templates/initiative",
  "dev/ai/adapters",
  "dev/workflow.md",
  "doc/architecture"
];

export const GOVERNANCE_EXCLUDE = [
  "dev/records",
  "dev/records/legacy",
  ".roo",
  "legacy",
  "logs",
  "reports"
];

export const SYMDEX_INCLUDE = [
  "core",
  "integrations/MCP-Microsoft-Office/src",
  "scripts",
  "tests",
  "manifests"
];

export const SYMDEX_EXCLUDE = [
  "node_modules",
  ".venv",
  "__pycache__",
  ".git",
  "logs",
  "state",
  "sessions",
  "content",
  "dev",
  ".roo",
  "legacy"
];

export function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

export function readText(filePath) {
  return fs.readFileSync(filePath, "utf8");
}

export function writeJson(filePath, value) {
  ensureDir(path.dirname(filePath));
  fs.writeFileSync(filePath, JSON.stringify(value, null, 2), "utf8");
}

export function readJson(filePath, fallback = null) {
  if (!fs.existsSync(filePath)) {
    return fallback;
  }
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

export function sha256(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

export function repoPath(relativePath) {
  return path.join(REPO_ROOT, relativePath);
}

export function isExcluded(relativePath, excludedParts) {
  const normalized = relativePath.replace(/\\/g, "/");
  return excludedParts.some((part) => normalized === part || normalized.startsWith(`${part}/`) || normalized.includes(`/${part}/`));
}

export function collectFiles(includes, excludes, extensionFilter = null) {
  const files = [];
  for (const relativeEntry of includes) {
    const absoluteEntry = repoPath(relativeEntry);
    if (!fs.existsSync(absoluteEntry)) {
      continue;
    }
    const stat = fs.statSync(absoluteEntry);
    if (stat.isFile()) {
      const rel = relativeEntry.replace(/\\/g, "/");
      if (!isExcluded(rel, excludes) && (!extensionFilter || extensionFilter(rel))) {
        files.push({
          absolutePath: absoluteEntry,
          relativePath: rel,
          size: stat.size,
          mtimeMs: stat.mtimeMs
        });
      }
      continue;
    }
    walkDir(absoluteEntry, relativeEntry.replace(/\\/g, "/"), excludes, extensionFilter, files);
  }
  return files.sort((a, b) => a.relativePath.localeCompare(b.relativePath));
}

function walkDir(absoluteDir, relativeDir, excludes, extensionFilter, files) {
  for (const entry of fs.readdirSync(absoluteDir, { withFileTypes: true })) {
    const absolutePath = path.join(absoluteDir, entry.name);
    const relativePath = `${relativeDir}/${entry.name}`.replace(/\\/g, "/");
    if (isExcluded(relativePath, excludes)) {
      continue;
    }
    if (entry.isDirectory()) {
      walkDir(absolutePath, relativePath, excludes, extensionFilter, files);
      continue;
    }
    if (extensionFilter && !extensionFilter(relativePath)) {
      continue;
    }
    const stat = fs.statSync(absolutePath);
    files.push({
      absolutePath,
      relativePath,
      size: stat.size,
      mtimeMs: stat.mtimeMs
    });
  }
}

export function splitMarkdownSections(text, maxChars = 2200) {
  const lines = text.split(/\r?\n/);
  const sections = [];
  let currentHeader = "root";
  let current = [];
  for (const line of lines) {
    if (/^#{1,6}\s+/.test(line) && current.length) {
      sections.push({ header: currentHeader, text: current.join("\n").trim() });
      currentHeader = line.trim();
      current = [line];
      continue;
    }
    if (/^#{1,6}\s+/.test(line)) {
      currentHeader = line.trim();
    }
    current.push(line);
  }
  if (current.length) {
    sections.push({ header: currentHeader, text: current.join("\n").trim() });
  }

  return sections.flatMap((section) => splitLargeText(section.text, maxChars).map((chunk, index) => ({
    header: section.header,
    text: chunk,
    ordinal: index + 1
  })));
}

export function splitCodeChunks(text, maxLines = 140, overlap = 20) {
  const lines = text.split(/\r?\n/);
  const chunks = [];
  let start = 0;
  while (start < lines.length) {
    const end = Math.min(lines.length, start + maxLines);
    chunks.push({
      startLine: start + 1,
      endLine: end,
      text: lines.slice(start, end).join("\n")
    });
    if (end === lines.length) {
      break;
    }
    start = Math.max(end - overlap, start + 1);
  }
  return chunks;
}

function splitLargeText(text, maxChars) {
  if (text.length <= maxChars) {
    return [text];
  }
  const chunks = [];
  let cursor = 0;
  while (cursor < text.length) {
    const windowEnd = Math.min(text.length, cursor + maxChars);
    let splitAt = text.lastIndexOf("\n\n", windowEnd);
    if (splitAt <= cursor + Math.floor(maxChars * 0.5)) {
      splitAt = windowEnd;
    }
    chunks.push(text.slice(cursor, splitAt).trim());
    cursor = splitAt;
  }
  return chunks.filter(Boolean);
}

export function cosineSimilarity(a, b) {
  let dot = 0;
  let normA = 0;
  let normB = 0;
  for (let i = 0; i < a.length; i += 1) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  return dot / ((Math.sqrt(normA) * Math.sqrt(normB)) || 1);
}

export async function embedTexts(texts, { model = "text-embedding-3-small" } = {}) {
  const openAiKey = (process.env.OPENAI_API_KEY || "").trim();
  if (openAiKey) {
    const batches = [];
    for (let i = 0; i < texts.length; i += 32) {
      batches.push(texts.slice(i, i + 32));
    }
    const vectors = [];
    for (const batch of batches) {
      const response = await fetch("https://api.openai.com/v1/embeddings", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${openAiKey}`
        },
        body: JSON.stringify({
          model,
          input: batch
        })
      });
      if (!response.ok) {
        const body = await response.text();
        throw new Error(`OpenAI embeddings failed: ${response.status} ${body}`);
      }
      const payload = await response.json();
      for (const item of payload.data) {
        vectors.push(item.embedding);
      }
    }
    return vectors;
  }

  const geminiKey = (process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY || "").trim();
  if (!geminiKey) {
    throw new Error("No embedding API key available. Set OPENAI_API_KEY or GOOGLE_API_KEY/GEMINI_API_KEY.");
  }
  const vectors = [];
  for (const text of texts) {
    const response = await fetch("https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-goog-api-key": geminiKey
      },
      body: JSON.stringify({
        model: "models/gemini-embedding-001",
        taskType: "SEMANTIC_SIMILARITY",
        outputDimensionality: 768,
        content: {
          parts: [{ text }]
        }
      })
    });
    if (!response.ok) {
      const body = await response.text();
      throw new Error(`Gemini embeddings failed: ${response.status} ${body}`);
    }
    const payload = await response.json();
    const raw = payload?.embedding?.values;
    if (!Array.isArray(raw) || !raw.length) {
      throw new Error("Gemini embeddings returned no vector.");
    }
    vectors.push(normalizeVector(raw));
  }
  return vectors;
}

function normalizeVector(vector) {
  let norm = 0;
  for (const value of vector) {
    norm += value * value;
  }
  const divisor = Math.sqrt(norm) || 1;
  return vector.map((value) => value / divisor);
}

export function loadEmbeddingCache(namespace) {
  return readJson(path.join(STATE_DIR, `${namespace}_embedding_cache.json`), {});
}

export function saveEmbeddingCache(namespace, cache) {
  writeJson(path.join(STATE_DIR, `${namespace}_embedding_cache.json`), cache);
}

export async function embedWithCache(items, namespace) {
  const cache = loadEmbeddingCache(namespace);
  const missing = [];
  for (const item of items) {
    const key = sha256(item.text);
    item.embeddingKey = key;
    if (!cache[key]) {
      missing.push(item);
    }
  }
  if (missing.length) {
    const vectors = await embedTexts(missing.map((item) => item.text));
    missing.forEach((item, index) => {
      cache[item.embeddingKey] = vectors[index];
    });
    saveEmbeddingCache(namespace, cache);
  }
  items.forEach((item) => {
    item.embedding = cache[item.embeddingKey];
  });
  return items;
}

export function loadIndex(indexPath) {
  return readJson(indexPath, null);
}

export function saveIndex(indexPath, index) {
  writeJson(indexPath, index);
}

export function computeSignature(files, extra = "") {
  const parts = files.map((file) => `${file.relativePath}:${file.size}:${Math.floor(file.mtimeMs)}`);
  return sha256(parts.join("|") + extra);
}

export function normalizeQueryTokens(query) {
  return new Set(
    (query.toLowerCase().match(/[a-z0-9_./-]+/g) || []).filter((token) => token.length >= 2)
  );
}

export function scoreLexical(query, content, extra = "") {
  const tokens = normalizeQueryTokens(query);
  if (!tokens.size) {
    return 0;
  }
  const haystack = `${content}\n${extra}`.toLowerCase();
  let hits = 0;
  for (const token of tokens) {
    if (haystack.includes(token)) {
      hits += token.length > 6 ? 2 : 1;
    }
  }
  return hits / (tokens.size * 2);
}

export function summarizeChunk(text, limit = 700) {
  if (text.length <= limit) {
    return text;
  }
  return `${text.slice(0, limit)}\n...`;
}

export function governanceCategory(relativePath) {
  const normalized = relativePath.replace(/\\/g, "/");
  if (normalized === "dev/workflow.md") {
    return "workflow";
  }
  const parts = normalized.split("/");
  return parts[1] || parts[0];
}

export function phasesFromText(text) {
  return Array.from(new Set((text.match(/\bF[1-9]\b/g) || []).sort()));
}

export function motorFromPath(relativePath) {
  const normalized = relativePath.replace(/\\/g, "/");
  if (normalized.startsWith("dev/ai/adapters/")) {
    return path.basename(normalized, path.extname(normalized));
  }
  return "";
}
