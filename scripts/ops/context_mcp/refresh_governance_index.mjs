import {
  GOVERNANCE_EXCLUDE,
  GOVERNANCE_INCLUDE,
  STATE_DIR,
  collectFiles,
  computeSignature,
  embedTexts,
  governanceCategory,
  inferPhasesFromPath,
  loadEmbeddingCache,
  mergeGovernancePhases,
  motorFromPath,
  phasesFromText,
  readText,
  repoPath,
  saveEmbeddingCache,
  saveIndex,
  splitMarkdownSections
} from "./shared.mjs";

const INDEX_PATH = repoPath("state/context_retrieval/governance_index.json");
const CACHE_NAMESPACE = "governance";
const CACHE_PATH = repoPath("state/context_retrieval/governance_embedding_cache.json");

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
    const inferredPhases = inferPhasesFromPath(file.relativePath, category);

    for (const section of sections) {
      const chunkText = section.text.trim();
      if (!chunkText) {
        continue;
      }
      chunks.push({
        id: `${file.relativePath}#${section.ordinal}`,
        relativePath: file.relativePath,
        category,
        motor,
        header: section.header,
        phases: mergeGovernancePhases(phasesFromText(chunkText), inferredPhases),
        text: chunkText
      });
    }
  }
  return chunks;
}

async function embedWithServerCompatibleCache(items) {
  const cache = loadEmbeddingCache(CACHE_NAMESPACE);
  const pending = [];
  for (const item of items) {
    if (cache[item.id]) {
      item.embedding = cache[item.id];
    } else {
      pending.push(item);
    }
  }

  for (let start = 0; start < pending.length; start += 32) {
    const batch = pending.slice(start, start + 32);
    const vectors = await embedTexts(batch.map((item) => item.text));
    batch.forEach((item, index) => {
      cache[item.id] = vectors[index];
      item.embedding = vectors[index];
    });
    saveEmbeddingCache(CACHE_NAMESPACE, cache);
    process.stdout.write(`\rEmbedded ${Math.min(start + batch.length, pending.length)}/${pending.length} new chunks`);
  }
  if (pending.length) {
    process.stdout.write("\n");
  }
  return items;
}

async function main() {
  const force = process.argv.includes("--force");
  if (force) {
    for (const filePath of [INDEX_PATH, CACHE_PATH]) {
      try {
        await import("node:fs").then((fs) => fs.rmSync(filePath, { force: true }));
      } catch {
        // rmSync with force should not fail for absent files; continue if it does.
      }
    }
  }

  const files = collectFiles(GOVERNANCE_INCLUDE, GOVERNANCE_EXCLUDE, fileAllowed);
  const signature = computeSignature(files, "governance_semantic_v1");
  const chunks = await embedWithServerCompatibleCache(buildGovernanceChunks(files));
  const index = {
    signature,
    generatedAt: new Date().toISOString(),
    include: GOVERNANCE_INCLUDE,
    exclude: GOVERNANCE_EXCLUDE,
    files: files.map((file) => file.relativePath),
    chunks
  };
  saveIndex(INDEX_PATH, index);
  console.log(JSON.stringify({
    indexPath: INDEX_PATH,
    fileCount: files.length,
    chunkCount: chunks.length,
    generatedAt: index.generatedAt,
    forced: force
  }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
