@echo off
title MyUTHM DB Sync Tool
echo ===========================================================
echo               MYUTHM DATABASE SYNC TOOL
echo ===========================================================

:: Set AyDB Path
set ADB_PATH=C:\Users\User\AppData\Local\Android\Sdk\platform-tools\adb.exe

:: 1. Check ADB Engine
if not exist "%ADB_PATH%" (
    echo [ERROR] adb.exe not found at:
    echo %ADB_PATH%
    echo -----------------------------------------------------------
    pause
    exit /b
)

echo [INFO] Connecting to emulator...
"%ADB_PATH%" devices
echo -----------------------------------------------------------

:: 2. Pull Database from Sandbox to Assets Folder
"%ADB_PATH%" shell "run-as com.example.uthm chmod 666 /data/data/com.example.uthm/databases/MyUTHM.db" 2>nul
"%ADB_PATH%" exec-out "run-as com.example.uthm cat /data/data/com.example.uthm/databases/MyUTHM.db" > assets\MyUTHM.db

:: 3. Validate File Size
for %%I in (assets\MyUTHM.db) do if %%~zI lss 100 (
    echo [FAIL] Sync failed! Database is empty.
    echo [TIPS] 1. Ensure your emulator is booted and running.
    echo        2. Ensure your app is running in [DEBUG] mode.
    echo -----------------------------------------------------------
    pause
    exit /b
)

echo [SUCCESS] Database pulled successfully!
echo [PATH]    Saved to assets\MyUTHM.db
echo ===========================================================
pause