param(
    [string]$RepoRoot = ".",
    [string]$StateDir = ".symdex",
    [switch]$SkipBackup,
    [switch]$SkipVerify,
    [switch]$SkipMcpRestart
)

$ErrorActionPreference = "Stop"

function Get-CommandPath {
    param([string]$Name)

    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($null -eq $cmd) {
        throw "Required command not found in PATH: $Name"
    }
    return $cmd.Source
}

function Get-RepoName {
    param([string]$ResolvedRepoRoot)

    $repoLeaf = Split-Path -Leaf $ResolvedRepoRoot
    $branch = (git -C $ResolvedRepoRoot rev-parse --abbrev-ref HEAD).Trim()
    if (-not $branch) {
        throw "Could not resolve current git branch."
    }
    if ($branch -eq "HEAD") {
        $branch = "detached-" + (git -C $ResolvedRepoRoot rev-parse --short HEAD).Trim()
    }

    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($ResolvedRepoRoot.ToLowerInvariant())
        $hash = [System.BitConverter]::ToString($sha.ComputeHash($bytes)).Replace("-", "").ToLowerInvariant()
    }
    finally {
        $sha.Dispose()
    }

    $safeBranch = ($branch -replace "[^a-zA-Z0-9._-]", "-").Trim("-")
    if (-not $safeBranch) {
        $safeBranch = "branch"
    }
    return "$repoLeaf-$safeBranch-$($hash.Substring(0, 8))"
}

function Resolve-RegistryEntryRoot {
    param(
        [string]$EntryRoot,
        [string]$ResolvedRepoRoot
    )

    if ([string]::IsNullOrWhiteSpace($EntryRoot)) {
        return $ResolvedRepoRoot
    }
    if ([System.IO.Path]::IsPathRooted($EntryRoot)) {
        return [System.IO.Path]::GetFullPath($EntryRoot)
    }
    return [System.IO.Path]::GetFullPath((Join-Path $ResolvedRepoRoot $EntryRoot))
}

function Restart-SymDexMcpServer {
    param(
        [string]$ResolvedRepoRoot,
        [string]$ResolvedStateDir
    )

    $processes = @(
        Get-CimInstance Win32_Process | Where-Object {
            $_.Name -eq "node.exe" -and
            $_.CommandLine -like "*symdex_code_server.mjs*" -and
            (
                $_.CommandLine -like "*$ResolvedRepoRoot*" -or
                $_.CommandLine -like "*$ResolvedStateDir*"
            )
        }
    )

    if ($processes.Count -eq 0) {
        Write-Host "MCP restart: no SymDex MCP process found for this repo."
        return
    }

    Write-Host "MCP restart: stopping SymDex MCP process(es) for this repo..."
    foreach ($process in $processes) {
        Write-Host " - PID $($process.ProcessId)"
        Stop-Process -Id $process.ProcessId -Force
    }
    Write-Host "MCP restart: stopped. The client should relaunch it on next tool use."
}

$resolvedRepoRoot = [System.IO.Path]::GetFullPath((Resolve-Path $RepoRoot).Path)
$resolvedStateDir = [System.IO.Path]::GetFullPath((Join-Path $resolvedRepoRoot $StateDir))
$registryJsonPath = Join-Path $resolvedStateDir "registry.json"
$registryDbPath = Join-Path $resolvedStateDir "registry.db"

if (-not (Test-Path $resolvedStateDir)) {
    throw "Missing SymDex state dir: $resolvedStateDir"
}

Get-CommandPath "git" | Out-Null
Get-CommandPath "symdex" | Out-Null
Get-CommandPath "python" | Out-Null

$repoName = Get-RepoName -ResolvedRepoRoot $resolvedRepoRoot
$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"

Write-Host "SymDex refresh"
Write-Host "--------------"
Write-Host "Repo root: $resolvedRepoRoot"
Write-Host "State dir: $resolvedStateDir"
Write-Host "Target repo: $repoName"

if (-not $SkipBackup) {
    if (Test-Path $registryJsonPath) {
        Copy-Item $registryJsonPath "$registryJsonPath.bak_$timestamp" -Force
    }
    if (Test-Path $registryDbPath) {
        Copy-Item $registryDbPath "$registryDbPath.bak_$timestamp" -Force
    }
    Write-Host "Backups: created for registry.json and registry.db"
}

Write-Host "Indexing current branch..."
symdex index $resolvedRepoRoot --state-dir $resolvedStateDir --repo $repoName

if (-not (Test-Path $registryJsonPath)) {
    throw "SymDex did not create registry.json at $registryJsonPath"
}
if (-not (Test-Path $registryDbPath)) {
    throw "SymDex did not create registry.db at $registryDbPath"
}

$registry = Get-Content $registryJsonPath -Raw | ConvertFrom-Json
if ($null -eq $registry) {
    throw "Failed to parse registry.json"
}

$entriesToRemove = @()
foreach ($entry in $registry) {
    $entryRoot = Resolve-RegistryEntryRoot -EntryRoot ([string]$entry.root_path) -ResolvedRepoRoot $resolvedRepoRoot
    if ($entryRoot -eq $resolvedRepoRoot -and $entry.name -ne $repoName) {
        $entriesToRemove += $entry
    }
}

if ($entriesToRemove.Count -gt 0) {
    $filteredRegistry = @(
        foreach ($entry in $registry) {
            $entryRoot = Resolve-RegistryEntryRoot -EntryRoot ([string]$entry.root_path) -ResolvedRepoRoot $resolvedRepoRoot
            if (-not ($entryRoot -eq $resolvedRepoRoot -and $entry.name -ne $repoName)) {
                $entry
            }
        }
    )
    $filteredRegistry | ConvertTo-Json -Depth 5 | Set-Content $registryJsonPath -Encoding UTF8

    foreach ($entry in $entriesToRemove) {
        $dbPath = [string]$entry.db_path
        if (-not [string]::IsNullOrWhiteSpace($dbPath)) {
            $relativeDb = $dbPath -replace "^[.][/\\]", ""
            $resolvedDb = [System.IO.Path]::GetFullPath((Join-Path $resolvedRepoRoot $relativeDb))
            foreach ($suffix in @("", "-wal", "-shm")) {
                $candidate = "$resolvedDb$suffix"
                if (Test-Path $candidate) {
                    Remove-Item $candidate -Force
                }
            }
        }
    }

    @'
import sqlite3
import sys

db_path = sys.argv[1]
names = sys.argv[2:]

conn = sqlite3.connect(db_path)
try:
    cur = conn.cursor()
    for name in names:
        cur.execute("DELETE FROM repos WHERE name = ?", (name,))
    conn.commit()
finally:
    conn.close()
'@ | python - $registryDbPath @($entriesToRemove | ForEach-Object { $_.name })

    Write-Host "Pruned stale entries for this repo root:"
    $entriesToRemove | ForEach-Object { Write-Host " - $($_.name)" }
}
else {
    Write-Host "Pruned stale entries for this repo root: none"
}

if (-not $SkipVerify) {
    Write-Host "Final verification:"
    symdex repos --state-dir $resolvedStateDir
}

if (-not $SkipMcpRestart) {
    Restart-SymDexMcpServer -ResolvedRepoRoot $resolvedRepoRoot -ResolvedStateDir $resolvedStateDir
}
else {
    Write-Host "MCP restart: skipped by -SkipMcpRestart."
}

Write-Host "Completed."
