$ErrorActionPreference='Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$vs=& 'C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe' -latest -products '*' -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
$vcvars=Join-Path $vs 'VC\Auxiliary\Build\vcvars64.bat'
$nvcc=Join-Path (Get-Location) 'tools\cuda\bin\nvcc.exe'
$command='call "'+$vcvars+'" && "'+$nvcc+'" -std=c++17 -O3 -arch=sm_89 -Xcompiler "/O2 /openmp /EHsc" src/image_cli.cpp src/edge.cpp src/cuda.cu -o build/edge_image.exe'
& cmd.exe /d /s /c $command
if($LASTEXITCODE -ne 0){throw 'Image CLI build failed'}
