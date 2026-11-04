$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$tectonic = Join-Path $root 'tools/tectonic/tectonic.exe'
if (!(Test-Path $tectonic)) { $tectonic = (Get-Command tectonic -ErrorAction Stop).Source }
Push-Location (Join-Path $root 'paper')
try {
    & $tectonic --keep-logs --keep-intermediates main.tex
    if ($LASTEXITCODE -ne 0) { throw 'LaTeX compilation failed' }
} finally { Pop-Location }
