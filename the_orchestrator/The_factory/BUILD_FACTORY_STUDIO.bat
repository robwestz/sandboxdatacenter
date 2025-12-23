@echo off
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║       THE FACTORY - Building Factory Studio GUI Project       ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Check if venv exists, if not run setup
if not exist "venv\" (
    echo 📦 Virtual environment not found. Running setup first...
    echo.
    python setup.py
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ❌ Setup failed. Trying with py launcher...
        py setup.py
    )
    echo.
    echo ✅ Setup complete!
    echo.
)

echo 🚀 Starting Factory Studio build...
echo.
echo Specification: projects\factory_studio\project_spec.md
echo Output: projects\factory_studio\output\
echo.
echo This will take approximately 4-5 hours and use up to 200 agents.
echo.
pause

REM Run the build
if exist "venv\Scripts\python.exe" (
    venv\Scripts\python.exe run_factory.py --project projects\factory_studio
) else (
    python run_factory.py --project projects\factory_studio
    if %ERRORLEVEL% NEQ 0 (
        py run_factory.py --project projects\factory_studio
    )
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo Build process initiated! Check the output above for progress.
echo ═══════════════════════════════════════════════════════════════
echo.
pause
