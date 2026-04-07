import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..", "..", "..");
const DEFAULT_STATE_DIR = path.join(REPO_ROOT, ".symdex");
const DEFAULT_SOURCE = "git+https://github.com/husnainpk/SymDex.git";

function parseArgs(argv) {
  const parsed = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      continue;
    }
    const key = token.slice(2);
    const next = argv[index + 1];
    if (!next || next.startsWith("--")) {
      parsed[key] = "true";
      continue;
    }
    parsed[key] = next;
    index += 1;
  }
  return parsed;
}

const argv = parseArgs(process.argv.slice(2));
const STATE_DIR = path.resolve(argv["state-dir"] || DEFAULT_STATE_DIR);
const SYMDEX_SOURCE = argv["symdex-source"] || DEFAULT_SOURCE;

function uniqueAttempts(values) {
  const attempts = [];
  const seen = new Set();
  for (const value of values) {
    if (!value) {
      continue;
    }
    const key = JSON.stringify(value);
    if (!seen.has(key)) {
      attempts.push(value);
      seen.add(key);
    }
  }
  return attempts;
}

function commandAttempts(args) {
  const symdexBin = argv["symdex-bin"] || process.env.SYMDEX_BIN || "symdex";
  const uvxBin = argv["uvx-bin"] || process.env.UVX_BIN || "uvx";
  return uniqueAttempts([
    { command: symdexBin, args },
    { command: "symdex", args },
    {
      command: uvxBin,
      args: ["--from", SYMDEX_SOURCE, "symdex", ...args],
    },
  ]);
}

function runCommand(args, { allowFailure = false } = {}) {
  const attempts = commandAttempts(args);
  const failures = [];

  for (const attempt of attempts) {
    const result = spawnSync(attempt.command, attempt.args, {
      cwd: REPO_ROOT,
      encoding: "utf8",
      timeout: 120000,
      windowsHide: true,
    });

    const stdout = (result.stdout || "").trim();
    const stderr = (result.stderr || "").trim();
    const rendered = `${attempt.command} ${attempt.args.join(" ")}`.trim();

    if (!result.error && result.status === 0) {
      return {
        ok: true,
        stdout,
        stderr,
        rendered,
      };
    }

    const message = result.error ? String(result.error.message || result.error) : stderr || stdout || `exit code ${result.status}`;
    failures.push(`${rendered} :: ${message}`);

    if (allowFailure) {
      return {
        ok: false,
        stdout,
        stderr,
        rendered,
        message,
      };
    }
  }

  throw new Error(`SymDex command failed: ${failures.join(" | ")}`);
}

function runJson(args, { allowFailure = false } = {}) {
  const result = runCommand(args, { allowFailure });
  if (!result.ok) {
    return result;
  }
  try {
    return {
      ...result,
      data: JSON.parse(extractJsonPayload(result.stdout || "{}")),
    };
  } catch (error) {
    if (allowFailure) {
      return {
        ok: false,
        stdout: result.stdout,
        stderr: result.stderr,
        rendered: result.rendered,
        message: `Invalid JSON from SymDex: ${String(error)}`,
      };
    }
    throw error;
  }
}

function extractJsonPayload(raw) {
  const trimmed = String(raw || "").trim();
  if (!trimmed) {
    return "{}";
  }
  try {
    JSON.parse(trimmed);
    return trimmed;
  } catch {}

  const lines = trimmed.split(/\r?\n/);
  for (let index = 0; index < lines.length; index += 1) {
    const candidate = lines.slice(index).join("\n").trim();
    if (!candidate.startsWith("{") && !candidate.startsWith("[")) {
      continue;
    }
    try {
      JSON.parse(candidate);
      return candidate;
    } catch {}
  }
  throw new Error("No JSON payload found in SymDex stdout");
}

function normalizePath(value) {
  return path.resolve(value).replace(/\\/g, "/").toLowerCase();
}

function isNoResult(message) {
  const normalized = String(message || "").toLowerCase();
  return normalized.includes("no symbols found") || normalized.includes("no callers found") || normalized.includes("no callees found");
}

let cachedRepoName = null;

function selectRepo(entries) {
  const expectedRoot = normalizePath(REPO_ROOT);
  const matches = entries
    .filter((entry) => normalizePath(entry.root_path || "") === expectedRoot)
    .sort((left, right) => {
      const leftTime = Date.parse(String(left.last_indexed || "").replace(" ", "T")) || 0;
      const rightTime = Date.parse(String(right.last_indexed || "").replace(" ", "T")) || 0;
      return rightTime - leftTime;
    });
  return matches[0] || null;
}

function resolveRepoName() {
  if (cachedRepoName) {
    return cachedRepoName;
  }

  let repos = runJson(["repos", "--json", "--state-dir", STATE_DIR]).data.repos || [];
  let selected = selectRepo(repos);

  if (!selected) {
    runCommand(["index", REPO_ROOT, "--state-dir", STATE_DIR]);
    repos = runJson(["repos", "--json", "--state-dir", STATE_DIR]).data.repos || [];
    selected = selectRepo(repos);
  }

  if (!selected) {
    throw new Error(`SymDex repo not indexed for ${REPO_ROOT}`);
  }

  cachedRepoName = selected.name;
  return cachedRepoName;
}

function repoRelativePath(relativePath) {
  const normalized = String(relativePath || "").replace(/\\/g, "/").replace(/^\/+/, "");
  if (!normalized) {
    throw new Error("relative_path is required");
  }
  return normalized;
}

function readSnippet(relativePath, startByte, endByte) {
  const normalized = repoRelativePath(relativePath);
  const absolutePath = path.join(REPO_ROOT, normalized);
  if (!fs.existsSync(absolutePath)) {
    throw new Error(`Missing file in repo: ${normalized}`);
  }

  const buffer = fs.readFileSync(absolutePath);
  const text = buffer.toString("utf8");
  const safeStart = Math.max(0, Number(startByte || 0));
  const safeEnd = Math.max(safeStart, Number(endByte || safeStart));
  const prefix = buffer.slice(0, safeStart).toString("utf8");
  const body = buffer.slice(safeStart, safeEnd).toString("utf8");
  const startLine = prefix.length ? prefix.split(/\r?\n/).length : 1;
  const snippetLineCount = body ? body.split(/\r?\n/).length : 1;
  const endLine = startLine + snippetLineCount - 1;
  const lines = text.split(/\r?\n/);
  const windowStart = Math.max(1, startLine - 3);
  const windowEnd = Math.min(lines.length, endLine + 3);
  const snippet = lines.slice(windowStart - 1, windowEnd).join("\n");

  return {
    relativePath: normalized,
    startLine,
    endLine,
    snippetWindowStart: windowStart,
    snippetWindowEnd: windowEnd,
    snippet,
  };
}

function render(payload) {
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(payload, null, 2),
      },
    ],
  };
}

const server = new McpServer({
  name: "symdex-code",
  version: "1.0.0",
});

server.tool(
  "search_symbols",
  {
    query: z.string().min(1),
    kind: z.string().optional(),
    limit: z.number().int().min(1).max(20).default(8),
  },
  async ({ query, kind = "", limit = 8 }) => {
    const repo = resolveRepoName();
    const response = runJson(
      [
        "search",
        query,
        "--repo",
        repo,
        "--limit",
        String(limit),
        "--json",
        "--state-dir",
        STATE_DIR,
      ],
      { allowFailure: true }
    );
    const symbols = response.ok
      ? (response.data.symbols || []).filter((item) => !kind || item.kind === kind)
      : [];
    return render({
      query,
      repo,
      warning: response.ok || isNoResult(response.message) ? null : response.message,
      results: symbols,
    });
  }
);

server.tool(
  "semantic_search",
  {
    query: z.string().min(1),
    limit: z.number().int().min(1).max(20).default(8),
  },
  async ({ query, limit = 8 }) => {
    const repo = resolveRepoName();
    const response = runJson(
      [
        "semantic",
        query,
        "--repo",
        repo,
        "--limit",
        String(limit),
        "--json",
        "--state-dir",
        STATE_DIR,
      ],
      { allowFailure: true }
    );

    if (response.ok) {
      return render({
        query,
        repo,
        mode: "semantic",
        results: response.data.results || response.data.symbols || [],
        roi: response.data.roi || null,
        roi_summary: response.data.roi_summary || null,
      });
    }

    const fallback = runJson(
      [
        "search",
        query,
        "--repo",
        repo,
        "--limit",
        String(limit),
        "--json",
        "--state-dir",
        STATE_DIR,
      ],
      { allowFailure: true }
    );
    return render({
      query,
      repo,
      mode: "fallback_search_symbols",
      warning: response.message,
      results: fallback.ok ? fallback.data.symbols || [] : [],
    });
  }
);

server.tool(
  "search_text",
  {
    query: z.string().min(1),
    path_pattern: z.string().optional(),
    limit: z.number().int().min(1).max(50).default(10),
  },
  async ({ query, path_pattern = "", limit = 10 }) => {
    const repo = resolveRepoName();
    const args = ["text", query, "--repo", repo, "--json", "--state-dir", STATE_DIR];
    if (path_pattern) {
      args.splice(4, 0, "--pattern", path_pattern);
    }
    const response = runJson(args, { allowFailure: true });
    return render({
      query,
      repo,
      pathPattern: path_pattern || null,
      warning: response.ok || isNoResult(response.message) ? null : response.message,
      results: response.ok ? (response.data.matches || []).slice(0, limit) : [],
      roi: response.ok ? response.data.roi || null : null,
      roi_summary: response.ok ? response.data.roi_summary || null : null,
    });
  }
);

server.tool(
  "get_symbol",
  {
    symbol_name: z.string().min(1),
    relative_path: z.string().optional(),
  },
  async ({ symbol_name, relative_path = "" }) => {
    const repo = resolveRepoName();
    const exact = runJson(
      ["find", symbol_name, "--repo", repo, "--json", "--state-dir", STATE_DIR],
      { allowFailure: true }
    );
    let symbols = exact.ok ? exact.data.symbols || [] : [];
    if (!symbols.length) {
      const fallback = runJson([
        "search",
        symbol_name,
        "--repo",
        repo,
        "--limit",
        "10",
        "--json",
        "--state-dir",
        STATE_DIR,
      ]);
      symbols = fallback.data.symbols || [];
    }

    const filtered = relative_path
      ? symbols.filter((item) => item.file === repoRelativePath(relative_path))
      : symbols;
    const selected = filtered[0];
    if (!selected) {
      throw new Error(
        `Symbol not found: ${symbol_name}${relative_path ? ` in ${repoRelativePath(relative_path)}` : ""}`
      );
    }

    return render({
      repo,
      symbol: selected,
      location: readSnippet(selected.file, selected.start_byte, selected.end_byte),
    });
  }
);

server.tool(
  "get_symbols",
  {
    relative_path: z.string().min(1),
  },
  async ({ relative_path }) => {
    const repo = resolveRepoName();
    const normalized = repoRelativePath(relative_path);
    const response = runJson([
      "outline",
      normalized,
      "--repo",
      repo,
      "--json",
      "--state-dir",
      STATE_DIR,
    ]);
    return render({
      repo,
      relativePath: normalized,
      symbols: response.data.symbols || [],
    });
  }
);

server.tool(
  "get_file_outline",
  {
    relative_path: z.string().min(1),
  },
  async ({ relative_path }) => {
    const repo = resolveRepoName();
    const normalized = repoRelativePath(relative_path);
    const response = runJson([
      "outline",
      normalized,
      "--repo",
      repo,
      "--json",
      "--state-dir",
      STATE_DIR,
    ]);
    const symbols = response.data.symbols || [];
    const countsByKind = symbols.reduce((accumulator, item) => {
      const kind = item.kind || "unknown";
      accumulator[kind] = (accumulator[kind] || 0) + 1;
      return accumulator;
    }, {});
    return render({
      repo,
      relativePath: normalized,
      symbolCount: symbols.length,
      countsByKind,
      symbols,
    });
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
