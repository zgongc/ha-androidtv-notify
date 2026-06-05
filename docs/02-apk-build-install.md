# Guide 2 — Build & Install the APK

Build the `HANotify` APK from source and install it on your Android TV via ADB.

---

## Prerequisites

| Tool | Required Version | Check |
|------|-----------------|-------|
| Java JDK | 11 or higher | `java -version` |
| Android SDK | Build-Tools 34, Platform 34 | See below |

### Check Java

```powershell
java -version
```

Expected output (example):
```
openjdk version "21.0.6" 2025-01-21 LTS
```

### Android SDK

If you have **Android Studio** installed, the SDK is already on your machine:

```powershell
# Check default location (Windows)
dir "C:\Users\$env:USERNAME\AppData\Local\Android\Sdk"
```

If found, note the path — you'll need it in a moment.

If **not** installed, download Command Line Tools only:
```
https://developer.android.com/studio#command-tools
```

---

## Step 1: Set Up the Build Environment

Navigate to the `apk/` folder inside this repository:

```powershell
cd path\to\ha-androidtv-notify\apk
```

Create `local.properties` pointing to your Android SDK:

```powershell
# Windows (adjust path to your SDK location)
Set-Content local.properties "sdk.dir=C:\\Users\\YourUser\\AppData\\Local\\Android\\Sdk"
```

```bash
# Linux / macOS
echo "sdk.dir=$HOME/Android/Sdk" > local.properties
```

---

## Step 2: Build the APK

### Windows

```powershell
.\gradlew.bat assembleDebug
```

### Linux / macOS

```bash
chmod +x gradlew
./gradlew assembleDebug
```

First run downloads Gradle (~130 MB) and Android build tools automatically.

Successful output ends with:
```
BUILD SUCCESSFUL in Xs
```

The APK is at:
```
apk/app/build/outputs/apk/debug/app-debug.apk
```

---

## Step 3: Install on TV

```powershell
.\adb.exe -s 192.168.1.129:5555 install apk\app\build\outputs\apk\debug\app-debug.apk
```

Expected output:
```
Performing Streamed Install
Success
```

To reinstall after an update:
```powershell
.\adb.exe -s 192.168.1.129:5555 install -r apk\app\build\outputs\apk\debug\app-debug.apk
```

---

## Step 4: Launch the App Once

The app has no visible UI, but Android requires it to be launched at least once before it can receive broadcasts:

```powershell
.\adb.exe -s 192.168.1.129:5555 shell am start -n com.hanotify/.MainActivity
```

Verify it's no longer in stopped state:
```powershell
.\adb.exe -s 192.168.1.129:5555 shell dumpsys package com.hanotify | Select-String "stopped"
```

Expected: `stopped=false`

---

## Step 5: Test the Notification

```powershell
.\adb.exe -s 192.168.1.129:5555 shell am start -n com.hanotify/.MainActivity "&&" am startservice -n com.hanotify/.ToastService --es message "Hello from ADB!"
```

A toast message should appear on the TV screen.

---

## How It Works

The APK contains two components:

- **`NotifyReceiver`** — a `BroadcastReceiver` that listens for `com.hanotify.SHOW_TOAST` intents
- **`ToastService`** — a `Service` that runs on the main thread and calls `Toast.makeText()`

The broadcast receiver starts the service, which displays the toast. This two-step approach is required because `Toast` cannot be shown directly from a receiver on older Android versions.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `BUILD FAILED` — SDK not found | Check `local.properties` path |
| `BUILD FAILED` — no repositories | Ensure `build.gradle` has `google()` and `mavenCentral()` |
| `Install failed` | Make sure `adb devices` shows the TV |
| Toast doesn't appear | Launch `MainActivity` first to set `stopped=false` |
| Toast appears once then stops | The app was killed. Re-launch `MainActivity` |

---

Next: [Home Assistant Integration →](03-ha-integration.md)
