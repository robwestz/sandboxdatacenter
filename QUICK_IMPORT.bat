@echo off
REM Quick Sandbox Import - Windows Batch Script
REM Run this after copying export file to sandbox

echo ============================================
echo  QUICK SANDBOX IMPORT
echo ============================================
echo.

cd C:\Users\WDAGUtilityAccount\Documents\Datacenter

python SANDBOX_IMPORT.py

echo.
echo Starting memory system...
python ACTIVATE_MEMORY.py

echo.
echo ============================================
echo  READY TO WORK!
echo ============================================
echo.

pause
