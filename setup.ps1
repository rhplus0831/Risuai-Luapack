<#
.SYNOPSIS
    Set up a self-contained embedded CPython (with lupa + pytest) under bin\python.

.DESCRIPTION
    Downloads the official CPython embeddable package and installs luapack's
    dependencies into it. The lupa wheel bundles Lua, so no C compiler / MSVC is
    required. After this runs, use .\luapack.cmd (or .\luapack.ps1) without any
    system Python.

    Re-run with -Force to rebuild from scratch.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File setup.ps1
#>
[CmdletBinding()]
param(
    [string]$PythonVersion = "3.13.1",
    [switch]$Force
)

$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$ProgressPreference = "SilentlyContinue"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$binPython = Join-Path $root "bin\python"
$py = Join-Path $binPython "python.exe"

$arch = switch ($env:PROCESSOR_ARCHITECTURE) {
    "AMD64" { "amd64" }
    "ARM64" { "arm64" }
    "x86"   { "win32" }
    default { "amd64" }
}

function Test-Ready {
    if (-not (Test-Path $py)) { return $false }
    & $py -c "import lupa; from lupa import lua54" 2>$null
    return ($LASTEXITCODE -eq 0)
}

if ((Test-Ready) -and (-not $Force)) {
    Write-Host "bin\python is already set up. Re-run with -Force to rebuild."
    exit 0
}

if ($Force -and (Test-Path $binPython)) {
    Remove-Item -Recurse -Force $binPython
}
New-Item -ItemType Directory -Force -Path $binPython | Out-Null

$tmp = Join-Path ([IO.Path]::GetTempPath()) ("luapack-" + [Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $tmp | Out-Null
try {
    # 1. Embeddable CPython
    $embedUrl = "https://www.python.org/ftp/python/$PythonVersion/python-$PythonVersion-embed-$arch.zip"
    $embedZip = Join-Path $tmp "python-embed.zip"
    Write-Host "Downloading $embedUrl"
    Invoke-WebRequest -Uri $embedUrl -OutFile $embedZip
    Expand-Archive -Path $embedZip -DestinationPath $binPython -Force

    # 2. Enable site-packages and put the repo root on sys.path.
    #    The embeddable ignores PYTHONPATH, so `import luapack` must come from
    #    the ._pth path-file (..\.. is the repo root, relative to python.exe).
    $pthFile = Get-ChildItem -Path $binPython -Filter "python*._pth" | Select-Object -First 1
    if ($null -eq $pthFile) { throw "._pth file not found in the embeddable package" }
    $lines = Get-Content $pthFile.FullName |
        ForEach-Object { $_ -replace '^\s*#\s*import\s+site', 'import site' }
    if ($lines -notcontains "Lib\site-packages") { $lines += "Lib\site-packages" }
    if ($lines -notcontains "..\..") { $lines += "..\.." }
    Set-Content -Path $pthFile.FullName -Value $lines -Encoding ascii

    # 3. Bootstrap pip
    $getpip = Join-Path $tmp "get-pip.py"
    Write-Host "Downloading get-pip.py"
    Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile $getpip
    & $py $getpip --no-warn-script-location
    if ($LASTEXITCODE -ne 0) { throw "pip bootstrap failed" }

    # 4. Install dependencies (lupa wheel bundles Lua; pytest for the harness)
    & $py -m pip install --no-warn-script-location -r (Join-Path $root "requirements.txt")
    if ($LASTEXITCODE -ne 0) { throw "pip install failed" }

    # 5. Verify
    & $py -c "import lupa; from lupa import lua54; print('lupa', lupa.__version__, '+ lua54 OK')"
    if ($LASTEXITCODE -ne 0) { throw "verification failed" }
}
finally {
    Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "Done. Embedded Python is ready at bin\python."
Write-Host "Try:  .\luapack.cmd build packs\example"
