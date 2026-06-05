# Guide 3 — Home Assistant Integration

Install the custom component and set up automations to send notifications to your TV.

---

## Prerequisites

- **Android Debug Bridge** integration installed in HA (Settings → Integrations → Android Debug Bridge)
- TV entity visible in HA (e.g. `media_player.android_tv_192_168_1_129`)
- APK installed on TV ([Guide 2](02-apk-build-install.md))

---

## Step 1: Install the Custom Component

Copy the `custom_components/androidtv_notify/` folder to your HA config directory:

```
/config/custom_components/androidtv_notify/
    __init__.py
    manifest.json
    notify.py
```

### Using HA Terminal add-on

```bash
mkdir -p /config/custom_components/androidtv_notify
```

Then use File Editor to create the three files (contents in the source folder).

### Using FTP / SSH / Samba

Copy the folder directly to `/config/custom_components/`.

---

## Step 2: Add to configuration.yaml

```yaml
notify:
  - platform: androidtv_notify
    name: philips_tv
    entity_id: media_player.android_tv_192_168_1_129
```

Replace `media_player.android_tv_192_168_1_129` with your actual TV entity ID.

> **Tip:** Find your entity ID under Settings → Integrations → Android Debug Bridge → your device.

---

## Step 3: Restart Home Assistant

Settings → System → Restart

After restart, verify the service exists:

**Developer Tools → Actions** — search for `notify.philips_tv`

---

## Step 4: Test

```yaml
action: notify.philips_tv
data:
  message: "Hello from Home Assistant!"
```

Click **Perform action** — a toast should appear on the TV.

---

## Step 5: Create an Automation

Example — notify when front door opens (TV must be on):

```yaml
alias: Front Door TV Notification
description: ""
triggers:
  - trigger: state
    entity_id:
      - binary_sensor.front_door
    to: "on"
conditions:
  - condition: state
    entity_id: media_player.android_tv_192_168_1_129
    state: "on"
actions:
  - action: notify.philips_tv
    data:
      message: "Front door opened!"
mode: single
```

The condition `state: "on"` ensures the notification is only sent when the TV is actually on, avoiding ADB errors when the TV is off.

---

## Multiple TVs

You can add multiple TVs by repeating the `notify` block with different names:

```yaml
notify:
  - platform: androidtv_notify
    name: living_room_tv
    entity_id: media_player.android_tv_192_168_1_129

  - platform: androidtv_notify
    name: bedroom_tv
    entity_id: media_player.android_tv_192_168_1_200
```

Each gets its own notify service: `notify.living_room_tv`, `notify.bedroom_tv`.

---

## How It Works

The custom component is a thin wrapper. When `notify.philips_tv` is called, it runs this ADB shell command via the `androidtv.adb_command` action:

```
am start -n com.hanotify/.MainActivity && am startservice -n com.hanotify/.ToastService --es message 'YOUR MESSAGE'
```

This ensures the app is in the foreground before the service is started, preventing Android's background service restrictions from blocking the toast.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `notify.philips_tv` not found | Check `configuration.yaml` syntax, restart HA |
| Service found but no toast | Make sure APK is installed and `MainActivity` was launched once |
| Works once then stops | TV killed the app. Add a `am start` before `am startservice` — already handled by the component |
| Error in HA logs | Check Settings → System → Logs, filter by `androidtv_notify` |

---

← [Back to APK Build](02-apk-build-install.md) | [Back to README](../README.md)
