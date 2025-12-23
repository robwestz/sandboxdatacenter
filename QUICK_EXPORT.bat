@echo off
REM Quick Sandbox Export - Windows Batch Script
REM Place this on Desktop for one-click backup

echo ============================================
echo  QUICK SANDBOX EXPORT
echo ============================================
echo.

cd C:\Users\WDAGUtilityAccount\Documents\Datacenter

python SANDBOX_EXPORT.py

echo.
echo ============================================
echo  DONE! File is on Desktop
echo  Copy to host before closing sandbox!
echo ============================================
echo.

pause
