$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
Set-Location $root
New-Item -ItemType Directory -Force build | Out-Null
$vswhere='C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe'
$vs=& $vswhere -latest -products '*' -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
if (!$vs -and (Test-Path 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat')) {$vs='C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools'}
if (!$vs) {throw 'Install Visual Studio C++ Build Tools'}
$vcvars=Join-Path $vs 'VC\Auxiliary\Build\vcvars64.bat'
$nvcc=Join-Path $root 'tools\cuda\bin\nvcc.exe'
if (!(Test-Path $nvcc)) {$nvcc=(Get-Command nvcc -ErrorAction Stop).Source}
$command='call "'+$vcvars+'" && "'+$nvcc+'" -std=c++17 -O3 -arch=sm_89 -Xcompiler "/O2 /openmp /EHsc" src/main.cpp src/edge.cpp src/cuda.cu -o build/edge.exe'
& cmd.exe /d /s /c $command
if($LASTEXITCODE -ne 0){throw 'Build failed'}
