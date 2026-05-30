@echo off
rem luapack launcher: runs the bundled embedded Python (see setup.ps1).
setlocal
set "PYEXE=%~dp0bin\python\python.exe"
if not exist "%PYEXE%" (
    echo Embedded Python not found. Run setup.ps1 first:
    echo   powershell -ExecutionPolicy Bypass -File "%~dp0setup.ps1"
    exit /b 1
)
"%PYEXE%" -m luapack %*
