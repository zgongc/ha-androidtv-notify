# Guide 1 — TV Setup: Developer Mode & ADB

Enable ADB debugging on your Android TV and establish a connection from your PC.

---

## Step 1: Enable Developer Mode

1. On your TV go to **Settings → About**
2. Navigate to **Build** and press it **7 times** in a row
3. You should see: `"Developer mode enabled"`

> On some Philips TVs the path is **Settings → Device Preferences → About → Build**

---

## Step 2: Enable USB Debugging

1. Go to **Settings → Developer options**
2. Turn on **USB debugging**

> Some Philips Android TV models do not show a separate "Network debugging" or "ADB over network" toggle. This is fine — network ADB can be activated via command line in the next steps.

---

## Step 3: Find the TV's IP Address

Go to **Settings → Network** on the TV and note the IP address.

Example: `192.168.1.129`

Alternatively, check your router's DHCP table.

---

## Step 4: Install ADB on Your PC

### Windows

Download Android SDK Platform Tools:
```
https://developer.android.com/tools/releases/platform-tools
```

Extract the ZIP (e.g. to `D:\platform-tools`), then open PowerShell in that folder.

### Linux / macOS

```bash
sudo apt install adb
# or
brew install android-platform-tools
```

---

## Step 5: Connect via ADB

```powershell
.\adb.exe connect 192.168.1.129:5555
```

**A dialog will appear on the TV screen: "Allow USB debugging?" → select Allow.**

Successful output:
```
connected to 192.168.1.129:5555
```

If it says `already connected`, you're good to go.

---

## Step 6: Verify the Connection

```powershell
.\adb.exe -s 192.168.1.129:5555 shell echo "hello"
```

Expected output: `hello`

---

## Useful ADB Commands

```powershell
# Send HOME key (basic connectivity test)
.\adb.exe -s 192.168.1.129:5555 shell input keyevent 3

# List installed third-party packages
.\adb.exe -s 192.168.1.129:5555 shell pm list packages -3

# Launch an activity
.\adb.exe -s 192.168.1.129:5555 shell am start -n com.hanotify/.MainActivity

# Start the toast service directly
.\adb.exe -s 192.168.1.129:5555 shell am startservice -n com.hanotify/.ToastService --es message 'Test'

# Send a broadcast intent
.\adb.exe -s 192.168.1.129:5555 shell "am broadcast -a com.hanotify.SHOW_TOAST --es message 'Test'"

# Check if package is installed and running
.\adb.exe -s 192.168.1.129:5555 shell dumpsys package com.hanotify | grep stopped
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `connection refused` | Make sure USB debugging is enabled on the TV |
| `unauthorized` | Accept the dialog that appears on the TV screen |
| Connection drops | Reboot the TV, then reconnect |
| Philips TV won't connect over wired | Initial ADB auth on some Philips TVs only works over Wi-Fi. Connect TV to Wi-Fi first, authorize, then switch back to wired |
| `already connected` but commands fail | Run `adb disconnect` then reconnect |

---

Next: [Build & Install the APK →](02-apk-build-install.md)
