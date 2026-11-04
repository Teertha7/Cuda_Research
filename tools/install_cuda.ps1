$ErrorActionPreference = 'Stop'
$manifest = Get-Content "$PSScriptRoot/downloads/redistrib_12.9.0.json" -Raw | ConvertFrom-Json
foreach ($component in @('cuda_nvcc','cuda_cudart','cuda_cccl')) {
  $entry = $manifest.$component.'windows-x86_64'
  $archive = Join-Path "$PSScriptRoot/downloads" ([IO.Path]::GetFileName($entry.relative_path))
  if (!(Test-Path $archive)) { Invoke-WebRequest ("https://developer.download.nvidia.com/compute/cuda/redist/" + $entry.relative_path) -OutFile $archive }
  if ((Get-FileHash $archive -Algorithm SHA256).Hash.ToLower() -ne $entry.sha256) { throw 'Checksum mismatch' }
  Expand-Archive -LiteralPath $archive -DestinationPath "$PSScriptRoot/downloads" -Force
  $expanded = Join-Path "$PSScriptRoot/downloads" ([IO.Path]::GetFileNameWithoutExtension($archive))
  New-Item -ItemType Directory -Force "$PSScriptRoot/cuda" | Out-Null
  Copy-Item "$expanded/*" "$PSScriptRoot/cuda" -Recurse -Force
}
& "$PSScriptRoot/cuda/bin/nvcc.exe" --version
