param(
    [string]$RepoRoot = ".",
    [ValidateSet("fast", "moderate", "full")]
    [string]$Mode = "full",
    [switch]$Recreate,
    [switch]$SkipVerify,
    [switch]$RestartMcp
)

$ErrorActionPreference = "Stop"

function Get-McpCommandPath {
    param([string]$ResolvedRepoRoot)

    $mcpConfigPath = Join-Path $ResolvedRepoRoot ".mcp.json"
    if (-not (Test-Path $mcpConfigPath)) {
        throw "Missing MCP config: $mcpConfigPath"
    }

    $config = Get-Content $mcpConfigPath -Raw | ConvertFrom-Json
    $server = $config.mcpServers.'codebase-memory-mcp'
    if ($null -eq $server) {
        throw ".mcp.json does not declare codebase-memory-mcp"
    }

    $command = [string]$server.command
    if ([string]::IsNullOrWhiteSpace($command)) {
        throw "codebase-memory-mcp has no command configured"
    }

    if ([System.IO.Path]::IsPathRooted($command)) {
        if (-not (Test-Path $command)) {
            throw "Configured codebase-memory-mcp binary does not exist: $command"
        }
        return [System.IO.Path]::GetFullPath($command)
    }

    $resolved = (Get-Command $command -ErrorAction SilentlyContinue)
    if ($null -eq $resolved) {
        throw "Could not resolve codebase-memory-mcp command from PATH: $command"
    }
    return $resolved.Source
}

function Convert-ToCodebaseProjectName {
    param([string]$ResolvedRepoRoot)

    return (($ResolvedRepoRoot -replace ":", "") -replace "[\\/]+", "-").Trim("-")
}

function Restart-CodebaseMemoryMcpServer {
    param([string]$BinaryPath)

    $processes = @(
        Get-CimInstance Win32_Process | Where-Object {
            $_.Name -eq ([System.IO.Path]::GetFileName($BinaryPath)) -and
            $_.CommandLine -like "*$BinaryPath*"
        }
    )

    if ($processes.Count -eq 0) {
        Write-Host "MCP restart: no codebase-memory MCP process found."
        return
    }

    Write-Host "MCP restart: stopping codebase-memory MCP process(es)..."
    foreach ($process in $processes) {
        Write-Host " - PID $($process.ProcessId)"
        Stop-Process -Id $process.ProcessId -Force
    }
    Write-Host "MCP restart: stopped. The client should relaunch it on next tool use."
}

function Invoke-CodebaseCli {
    param(
        [string]$BinaryPath,
        [string]$Tool,
        [object]$Payload = $null
    )

    $raw = if ($null -eq $Payload) {
        python -c "import subprocess, sys; r=subprocess.run([sys.argv[1], 'cli', sys.argv[2]], capture_output=True, text=True); print((r.stdout or '') + (('\n' + r.stderr) if r.stderr else ''))" $BinaryPath $Tool | Out-String
    } else {
        $json = $Payload | ConvertTo-Json -Depth 10 -Compress
        $previousPayload = $env:CODEBASE_MEMORY_PAYLOAD
        $env:CODEBASE_MEMORY_PAYLOAD = $json
        try {
            python -c "import os, subprocess, sys; args=[sys.argv[1], 'cli', sys.argv[2]]; payload=os.environ.get('CODEBASE_MEMORY_PAYLOAD'); args.append(payload) if payload else None; r=subprocess.run(args, capture_output=True, text=True); print((r.stdout or '') + (('\n' + r.stderr) if r.stderr else ''))" $BinaryPath $Tool | Out-String
        }
        finally {
            if ($null -eq $previousPayload) {
                Remove-Item Env:CODEBASE_MEMORY_PAYLOAD -ErrorAction SilentlyContinue
            }
            else {
                $env:CODEBASE_MEMORY_PAYLOAD = $previousPayload
            }
        }
    }
    $raw = $raw.Trim()
    if ([string]::IsNullOrWhiteSpace($raw)) {
        throw "Empty response from codebase-memory-mcp cli $Tool"
    }

    $jsonLine = $raw -split "\r?\n" | Where-Object {
        $_.Trim().StartsWith("{") -and $_.Trim().EndsWith("}")
    } | Select-Object -First 1

    if ([string]::IsNullOrWhiteSpace($jsonLine)) {
        throw "Could not isolate JSON response from codebase-memory-mcp cli ${Tool}: $raw"
    }

    $textPayload = [string](($jsonLine | python -c "import json, sys; env=json.loads(sys.stdin.read()); print(env['content'][0]['text'])") | Out-String).Trim()
    if ([string]::IsNullOrWhiteSpace($textPayload)) {
        throw "Missing text payload from codebase-memory-mcp cli $Tool"
    }

    return $textPayload
}

$resolvedRepoRoot = [System.IO.Path]::GetFullPath((Resolve-Path $RepoRoot).Path)
$binaryPath = Get-McpCommandPath -ResolvedRepoRoot $resolvedRepoRoot
$projectName = Convert-ToCodebaseProjectName -ResolvedRepoRoot $resolvedRepoRoot

Write-Host "Codebase-memory refresh"
Write-Host "-----------------------"
Write-Host "Repo root: $resolvedRepoRoot"
Write-Host "Binary: $binaryPath"
Write-Host "Target project: $projectName"
Write-Host "Mode: $Mode"
Write-Host "Recreate: $($Recreate.IsPresent)"

$projectsBeforeJson = Invoke-CodebaseCli -BinaryPath $binaryPath -Tool "list_projects"
$projectExistsBefore = $projectsBeforeJson -match [regex]::Escape($projectName)

if ($Recreate -and $projectExistsBefore) {
    Write-Host "Deleting existing project before reindex..."
    $deleteJson = Invoke-CodebaseCli -BinaryPath $binaryPath -Tool "delete_project" -Payload @{ project = $projectName }
    Write-Host "Delete response: $deleteJson"
}

Write-Host "Indexing repository..."
$indexJson = Invoke-CodebaseCli -BinaryPath $binaryPath -Tool "index_repository" -Payload @{
    repo_path = $resolvedRepoRoot
    mode = $Mode
}
Write-Host "Index response: $indexJson"

if (-not $SkipVerify) {
    $projectsAfterJson = Invoke-CodebaseCli -BinaryPath $binaryPath -Tool "list_projects"
    $projectExistsAfter = $projectsAfterJson -match [regex]::Escape($projectName)
    if (-not $projectExistsAfter) {
        throw "Project not present after indexing: $projectName"
    }

    $statusJson = Invoke-CodebaseCli -BinaryPath $binaryPath -Tool "index_status" -Payload @{ project = $projectName }

    Write-Host "Final verification:"
    Write-Host "Projects response: $projectsAfterJson"
    Write-Host "Index status response: $statusJson"
}

if ($RestartMcp) {
    Restart-CodebaseMemoryMcpServer -BinaryPath $binaryPath
}
else {
    Write-Host "MCP restart: skipped. Use -RestartMcp only if the active MCP session remains stale."
}

Write-Host "Completed."
