@echo off
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║         THE FACTORY - Opening in PyCharm...                  ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Try multiple ways to find and launch PyCharm

REM Method 1: Check if pycharm64.exe is in PATH
where pycharm64.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Found PyCharm in PATH
    echo 🚀 Launching...
    start "" pycharm64.exe "%~dp0"
    goto :success
)

REM Method 2: Check if pycharm.exe is in PATH
where pycharm.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Found PyCharm in PATH
    echo 🚀 Launching...
    start "" pycharm.exe "%~dp0"
    goto :success
)

REM Method 3: JetBrains Toolbox scripts location
if exist "%LOCALAPPDATA%\JetBrains\Toolbox\scripts\pycharm.cmd" (
    echo ✅ Found PyCharm via JetBrains Toolbox
    echo 🚀 Launching...
    start "" "%LOCALAPPDATA%\JetBrains\Toolbox\scripts\pycharm.cmd" "%~dp0"
    goto :success
)

REM Method 4: Common installation paths
set PYCHARM_PATHS=^
"C:\Program Files\JetBrains\PyCharm Professional\bin\pycharm64.exe"^
 "C:\Program Files\JetBrains\PyCharm Community Edition\bin\pycharm64.exe"^
 "C:\Program Files (x86)\JetBrains\PyCharm Professional\bin\pycharm64.exe"^
 "C:\Program Files (x86)\JetBrains\PyCharm Community Edition\bin\pycharm64.exe"

for %%p in (%PYCHARM_PATHS%) do (
    if exist %%p (
        echo ✅ Found PyCharm at %%p
        echo 🚀 Launching...
        start "" %%p "%~dp0"
        goto :success
    )
)

REM If we get here, PyCharm was not found
echo.
echo ⚠️  PyCharm not found automatically.
echo.
echo 📌 To open manually:
echo    1. Open PyCharm
echo    2. File -^> Open
echo    3. Select: %~dp0
echo.
pause
goto :end

:success
echo.
echo ✅ PyCharm launched successfully!
echo.
echo 📋 Next steps in PyCharm:
echo    1. Wait for PyCharm to load the project
echo    2. Open Terminal in PyCharm (View -^> Tool Windows -^> Terminal)
echo    3. Run: python setup.py
echo    4. After setup: factory.bat "Build a todo app"
echo.
timeout /t 3 >nul

:end
