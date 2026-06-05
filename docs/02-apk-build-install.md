# Guide 2 — Build & Install the APK

Build the `HANotify` APK from source and install it on your Android TV via ADB.

---

## Prerequisites

| Tool | Required Version | Check |
|------|-----------------|-------|
| Java JDK | 11 or higher | `java -version` |
| Android SDK | Build-Tools 34, Platform 34 | See below |
| ADB | any | See [Guide 1](01-tv-setup.md) |

### Add ADB to PATH (recommended, do once)

If `adb` is not on your PATH, add it so you don't need the full path every time:

**Windows (PowerShell — run once):**
```powershell
# Replace with your actual platform-tools path
[System.Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";D:\github\platform-tools", "User")
```

Then open a **new** PowerShell window — `adb` will work directly from any folder.

**Linux / macOS:**
```bash
echo 'export PATH="$PATH:$HOME/platform-tools"' >> ~/.bashrc
source ~/.bashrc
```

### Check Java

```powershell
java -version
```

### Android SDK

If you have **Android Studio** installed, the SDK is already on your machine:

```powershell
dir "C:\Users\$env:USERNAME\AppData\Local\Android\Sdk"
```

---

## Step 1: Create local.properties

Navigate to the `apk/` folder inside this repository and create the SDK path file:

**Windows (PowerShell):**
```powershell
cd D:\github\ha-androidtv-notify\apk
Set-Content local.properties "sdk.dir=C:\\Users\\$env:USERNAME\\AppData\\Local\\Android\\Sdk"
```

> `$env:USERNAME` expands automatically — no need to type your username.

**Linux / macOS:**
```bash
cd ~/ha-androidtv-notify/apk
echo "sdk.dir=$HOME/Android/Sdk" > local.properties
```

---

## Step 2: Download Gradle (first time only)

**Windows:**
```powershell
cd D:\github\ha-androidtv-notify\apk
Invoke-WebRequest -Uri "https://services.gradle.org/distributions/gradle-8.2-bin.zip" -OutFile "gradle.zip"
Expand-Archive -Path gradle.zip -DestinationPath gradle-dist
```

**Linux / macOS:**
```bash
cd ~/ha-androidtv-notify/apk
curl -L https://services.gradle.org/distributions/gradle-8.2-bin.zip -o gradle.zip
unzip gradle.zip -d gradle-dist
```

> After the first successful build, Gradle is cached in `~/.gradle` — you won't need to download it again.

---

## Step 3: Build the APK

From the `apk/` folder:

**Windows:**
```powershell
cd D:\github\ha-androidtv-notify\apk
.\gradlew.bat assembleDebug
```

**Linux / macOS:**
```bash
chmod +x gradlew
./gradlew assembleDebug
```

Successful output ends with:
```
BUILD SUCCESSFUL in Xs
```

Output APK location:
```
apk/app/build/outputs/apk/debug/app-debug.apk
```

---

## Step 4: Install on TV

From any folder (assuming adb is on PATH):

**First install:**
```powershell
adb -s 192.168.1.129:5555 install app\build\outputs\apk\debug\app-debug.apk
```

**Re-install / update (use `-r` flag):**
```powershell
adb -s 192.168.1.129:5555 install -r app\build\outputs\apk\debug\app-debug.apk
```

> Always use `-r` if the app is already installed, otherwise you'll get `INSTALL_FAILED_ALREADY_EXISTS`.

Expected output:
```
Performing Streamed Install
Success
```

---

## Step 5: Launch the App Once

Android blocks broadcasts to apps that have never been launched. Run this once after install:

```powershell
adb -s 192.168.1.129:5555 shell am start -n com.hanotify/.MainActivity
```

Verify the app is no longer in stopped state:
```powershell
adb -s 192.168.1.129:5555 shell dumpsys package com.hanotify | Select-String "stopped"
```

Expected: `stopped=false`

---

## Step 6: Test the Notification

```powershell
adb -s 192.168.1.129:5555 shell "am start -n com.hanotify/.MainActivity; sleep 1; am startservice -n com.hanotify/.ToastService --es message 'Hello!' --es title 'HA' --ei duration 1 --es fontsize 'large'"
```

A toast should appear on the TV screen.

---

## Supported Intent Extras

| Extra | Type | Values | Default | Description |
|-------|------|--------|---------|-------------|
| `message` | String | any | `"Home Assistant Notification"` | Notification body |
| `title` | String | any | — | Optional title (shown as `Title: message`) |
| `duration` | int | `0` / `1` | `1` | `0` = short (~2s), `1` = long (~3.5s) |
| `fontsize` | String | `small` / `medium` / `large` | `medium` | Toast text size |

---

## How It Works

- **`MainActivity`** — minimal no-UI activity, launched once to move app out of Android's "stopped" state
- **`NotifyReceiver`** — `BroadcastReceiver` listening for `com.hanotify.SHOW_TOAST` intents
- **`ToastService`** — `Service` that runs on the main thread and calls `Toast.makeText()`

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `adb` not found | Add platform-tools folder to PATH (see top of this guide) |
| `INSTALL_FAILED_ALREADY_EXISTS` | Add `-r` flag to the install command |
| `gradlew.bat` not found | Make sure you're in the `apk/` folder |
| `BUILD FAILED` — SDK not found | Check `local.properties`, re-run Step 1 |
| `BUILD FAILED` — Gradle not found | Run the Gradle download step (Step 2) |
| Toast doesn't appear after install | Run Step 5 — launch `MainActivity` once |

---

Next: [Home Assistant Integration →](03-ha-integration.md)
