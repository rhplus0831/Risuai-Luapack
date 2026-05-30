# luapack launcher: runs the bundled embedded Python (see setup.ps1).
$pyexe = Join-Path $PSScriptRoot "bin\python\python.exe"
if (-not (Test-Path $pyexe)) {
    Write-Host "Embedded Python not found. Run setup.ps1 first:"
    Write-Host "  powershell -ExecutionPolicy Bypass -File `"$(Join-Path $PSScriptRoot 'setup.ps1')`""
    exit 1
}
& $pyexe -m luapack @args
exit $LASTEXITCODE
