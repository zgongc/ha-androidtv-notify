# HA Android TV Notify

Send toast notifications from Home Assistant to Android TV using ADB.

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2026.6+-blue)
![Android TV](https://img.shields.io/badge/Android%20TV-7.0+-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Overview

This project provides:
- A small Android APK that listens for ADB broadcast intents and shows toast notifications on screen
- A Home Assistant custom component (`notify.your_tv`) that wraps the ADB command into a clean notify service

**Result:** Call `notify.philips_tv` from any HA automation and a message pops up on your TV screen — no cloud, no third-party app, fully local.

## Quick Start

| Step | Guide |
|------|-------|
| 1 | [TV Setup — Developer Mode & ADB](docs/01-tv-setup.md) |
| 2 | [Build & Install the APK](docs/02-apk-build-install.md) |
| 3 | [Home Assistant Integration](docs/03-ha-integration.md) |

## Tested Environment

| Component | Version |
|-----------|---------|
| Home Assistant | 2026.6.0 |
| TV Model | Philips 49PUS7503/12 |
| Android TV | 7.x |
| Java | OpenJDK 21 |
| Gradle | 8.2 |
| Android SDK | Build-Tools 34 |

## Requirements

- Home Assistant with **Android Debug Bridge** integration installed
- Android TV with ADB debugging enabled
- Java JDK 11+ on your build machine
- Android SDK (Build-Tools 34, Platform 34)

## Usage

Once set up, send a notification from any automation:

```yaml
action: notify.philips_tv
data:
  message: "Front door opened!"
```

Or test from Developer Tools → Actions:

```yaml
action: notify.philips_tv
data:
  message: "Hello from Home Assistant!"
```

## License

MIT
