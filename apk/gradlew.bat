@echo off

:: HANotify APK - Gradle build script for Windows
:: Requires: Java 11+, Android SDK
::
:: First run setup:
::   1. PowerShell: Set-Content local.properties "sdk.dir=C:\\Users\\$env:USERNAME\\AppData\\Local\\Android\\Sdk"
::   2. Run this script: .\gradlew.bat assembleDebug

setlocal

:: Try GRADLE_HOME env variable first
if defined GRADLE_HOME (
    set GRADLE_CMD=%GRADLE_HOME%\bin\gradle.bat
    goto run
)

:: Try common install locations
if exist "%USERPROFILE%\.gradle\wrapper\dists\gradle-8.2-bin" (
    for /d %%i in ("%USERPROFILE%\.gradle\wrapper\dists\gradle-8.2-bin\*") do (
        if exist "%%i\gradle-8.2\bin\gradle.bat" (
            set GRADLE_CMD=%%i\gradle-8.2\bin\gradle.bat
            goto run
        )
    )
)

:: Try gradle-dist folder next to this script (manual download)
set SCRIPT_DIR=%~dp0
if exist "%SCRIPT_DIR%gradle-dist\gradle-8.2\bin\gradle.bat" (
    set GRADLE_CMD=%SCRIPT_DIR%gradle-dist\gradle-8.2\bin\gradle.bat
    goto run
)

:: Not found
echo.
echo ERROR: Gradle not found. Run the following in PowerShell to set up:
echo.
echo   Invoke-WebRequest -Uri "https://services.gradle.org/distributions/gradle-8.2-bin.zip" -OutFile "%SCRIPT_DIR%gradle.zip"
echo   Expand-Archive -Path "%SCRIPT_DIR%gradle.zip" -DestinationPath "%SCRIPT_DIR%gradle-dist"
echo.
exit /b 1

:run
"%GRADLE_CMD%" %*
