$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$script = Join-Path $repoRoot "scripts/ops/context_mcp/refresh_governance_index.mjs"

Write-Host "Governance retrieval refresh"
Write-Host "----------------------------"
Write-Host "Repo root: $repoRoot"

Push-Location $repoRoot
try {
  node $script --force
  Write-Host "Completed. Restart the MCP/session if the active governance_search server still serves old snippets."
} finally {
  Pop-Location
}
