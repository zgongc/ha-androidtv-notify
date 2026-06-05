# HA Android TV Notify

Send toast notifications from Home Assistant to Android TV using ADB — no cloud, no third-party app, fully local.

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2026.6+-blue)
![Android TV](https://img.shields.io/badge/Android%20TV-7.0+-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Overview

This project provides:
- A small Android APK (`HANotify`) that listens for ADB intents and shows toast notifications on screen
- A Home Assistant custom component that exposes a `notify.your_tv` service

**Result:** Call `notify.philips_tv` from any HA automation and a message pops up on your TV screen.

```yaml
action: notify.philips_tv
data:
  title: "Front Door"
  message: "Motion detected!"
  data:
    duration: 1
    fontsize: large
```

---

## Supported Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `title` | any string | — | Optional title prepended to message |
| `message` | any string | — | Notification body text |
| `duration` | `0` / `1` | `1` | `0` = short (~2s), `1` = long (~3.5s) |
| `fontsize` | `small` / `medium` / `large` | `medium` | Toast text size |

---

## Quick Start

| Step | Guide |
|------|-------|
| 1 | [TV Setup — Developer Mode & ADB](docs/01-tv-setup.md) |
| 2 | [Build & Install the APK](docs/02-apk-build-install.md) |
| 3 | [Home Assistant Integration](docs/03-ha-integration.md) |

---

## Tested Environment

| Component | Version |
|-----------|---------|
| Home Assistant | 2026.6.0 |
| TV Model | Philips 49PUS7503/12 |
| Android TV | 7.x |
| Java | OpenJDK 21 |
| Gradle | 8.2 |
| Android SDK | Build-Tools 34, Platform 34 |

---

## Requirements

- Home Assistant with **Android Debug Bridge** integration
- Android TV with ADB debugging enabled
- Java JDK 11+ (for building the APK)
- Android SDK Build-Tools 34

---

## License

MIT
