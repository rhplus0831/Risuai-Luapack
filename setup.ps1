<#
.SYNOPSIS
    Set up self-contained tooling for luapack on Windows.

.DESCRIPTION
    Downloads the official CPython embeddable package and installs luapack's
    dependencies into it. The lupa wheel bundles Lua, so no C compiler / MSVC is
    required. After this runs, use .\luapack.cmd (or .\luapack.ps1) without any
    system Python.

    If git.exe is not available, downloads Portable Git for Windows under
    bin\git. Then clones or updates Refer\Risuai and overlays the local
    risu-docs contents into that checkout the first time it is cloned.

    Re-run with -Force to rebuild the embedded Python runtime from scratch.

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
$bin = Join-Path $root "bin"
$binPython = Join-Path $root "bin\python"
$py = Join-Path $binPython "python.exe"
$binGit = Join-Path $root "bin\git"
$referRoot = Join-Path $root "Refer"
$referRisuai = Join-Path $referRoot "Risuai"
$risuDocs = Join-Path $root "risu-docs"
$risuRepoUrl = "https://github.com/kwaroran/Risuai.git"

$arch = switch ($env:PROCESSOR_ARCHITECTURE) {
    "AMD64" { "amd64" }
    "ARM64" { "arm64" }
    "x86"   { "win32" }
    default { "amd64" }
}

function Test-PythonReady {
    if (-not (Test-Path $py)) { return $false }
    & $py -c "import lupa; from lupa import lua54" 2>$null
    return ($LASTEXITCODE -eq 0)
}

function Install-PythonRuntime {
    if ((Test-PythonReady) -and (-not $Force)) {
        Write-Host "bin\python is already set up. Re-run with -Force to rebuild."
        return
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
}

function Get-GitExe {
    $localCandidates = @(
        (Join-Path $binGit "cmd\git.exe"),
        (Join-Path $binGit "bin\git.exe"),
        (Join-Path $binGit "mingw64\bin\git.exe")
    )
    foreach ($candidate in $localCandidates) {
        if (Test-Path $candidate) { return $candidate }
    }

    $cmd = Get-Command "git.exe" -CommandType Application -ErrorAction SilentlyContinue
    if ($null -ne $cmd) { return $cmd.Source }

    return $null
}

function Install-Git {
    $existingGit = Get-GitExe
    if ($null -ne $existingGit) {
        Write-Host "git is already available at $existingGit."
        return $existingGit
    }

    if ($env:PROCESSOR_ARCHITECTURE -eq "ARM64") {
        $gitAssetPattern = "PortableGit-*-arm64.7z.exe"
    }
    elseif ($env:PROCESSOR_ARCHITECTURE -eq "x86") {
        $gitAssetPattern = "PortableGit-*-32-bit.7z.exe"
    }
    else {
        $gitAssetPattern = "PortableGit-*-64-bit.7z.exe"
    }

    New-Item -ItemType Directory -Force -Path $bin | Out-Null

    $tmp = Join-Path ([IO.Path]::GetTempPath()) ("luapack-git-" + [Guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Force -Path $tmp | Out-Null
    try {
        Write-Host "Finding latest Portable Git for Windows..."
        $release = Invoke-RestMethod -Uri "https://api.github.com/repos/git-for-windows/git/releases/latest" -Headers @{ "User-Agent" = "Risuai-Luapack setup.ps1" }
        $asset = $release.assets |
            Where-Object { $_.name -like $gitAssetPattern } |
            Sort-Object name -Descending |
            Select-Object -First 1
        if ($null -eq $asset) { throw "Portable Git asset not found for $env:PROCESSOR_ARCHITECTURE." }

        $gitArchive = Join-Path $tmp $asset.name
        Write-Host "Downloading $($asset.browser_download_url)"
        Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $gitArchive

        if (Test-Path $binGit) {
            Remove-Item -Recurse -Force $binGit
        }
        New-Item -ItemType Directory -Force -Path $binGit | Out-Null

        Write-Host "Installing Git under bin\git..."
        & $gitArchive -y "-o$binGit"
        if ($LASTEXITCODE -ne 0) { throw "Portable Git extraction failed" }
    }
    finally {
        Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
    }

    $installedGit = Get-GitExe
    if ($null -eq $installedGit) { throw "git.exe was not found after installing Portable Git." }
    return $installedGit
}

function Copy-RisuDocsIntoReference {
    if (-not (Test-Path $risuDocs)) {
        Write-Warning "risu-docs was not found; skipping local docs overlay."
        return
    }

    Write-Host "Copying risu-docs into Refer\Risuai..."
    Copy-Item -Path (Join-Path $risuDocs "*") -Destination $referRisuai -Recurse -Force
}

function Update-RisuaiReference {
    param(
        [Parameter(Mandatory = $true)]
        [string]$GitExe
    )

    New-Item -ItemType Directory -Force -Path $referRoot | Out-Null

    if (Test-Path $referRisuai) {
        if (-not (Test-Path (Join-Path $referRisuai ".git"))) {
            throw "Refer\Risuai exists, but it is not a Git checkout."
        }

        Write-Host "Updating Refer\Risuai..."
        & $GitExe -C $referRisuai pull --ff-only --autostash
        if ($LASTEXITCODE -ne 0) { throw "git pull failed for Refer\Risuai." }
        return
    }

    Write-Host "Cloning $risuRepoUrl into Refer\Risuai..."
    & $GitExe clone $risuRepoUrl $referRisuai
    if ($LASTEXITCODE -ne 0) { throw "git clone failed for Refer\Risuai." }

    Copy-RisuDocsIntoReference
}

Install-PythonRuntime
$git = Install-Git
Update-RisuaiReference -GitExe $git

Write-Host ""
Write-Host "Done. Embedded Python is ready at bin\python."
Write-Host "Git is available at $git."
Write-Host "RisuAI source is ready at Refer\Risuai."
Write-Host "Try:  .\luapack.cmd build packs\example"
