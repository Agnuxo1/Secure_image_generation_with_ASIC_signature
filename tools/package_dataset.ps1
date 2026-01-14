param(
    [string]$OutFile = "dataset.tar.gz"
)

# Package dataset directories into a compressed tar.gz archive (PowerShell)
$dirs = @("Originals", "proofs")
$existing = $dirs | Where-Object { Test-Path $_ }
if (-not $existing) {
    Write-Error "No dataset directories found."
    exit 1
}

$tmp = Join-Path $env:TEMP ([System.IO.Path]::GetRandomFileName())
New-Item -ItemType Directory -Path $tmp | Out-Null

foreach ($d in $existing) {
    Copy-Item -Path $d -Destination (Join-Path $tmp $d) -Recurse -Force
}

# Use tar (Windows 10+ includes tar) or fallback to Compress-Archive (zip)
if (Get-Command tar -ErrorAction SilentlyContinue) {
    Push-Location $tmp
    tar -czf (Resolve-Path $OutFile) *
    Pop-Location
    Move-Item -Force (Join-Path $tmp $OutFile) .\$OutFile
    Write-Output "Created $OutFile"
} else {
    $zipOut = [System.IO.Path]::ChangeExtension($OutFile, ".zip")
    Compress-Archive -Path (Join-Path $tmp "*") -DestinationPath $zipOut -Force
    Write-Output "tar not available: created $zipOut instead"
}

# Generate SHA256 checksum
if (Get-Command Get-FileHash -ErrorAction SilentlyContinue) {
    Get-FileHash -Algorithm SHA256 .\$OutFile | Format-List
}

Remove-Item -Recurse -Force $tmp
