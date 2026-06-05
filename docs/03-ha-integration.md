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

Using HA Terminal add-on:

```bash
mkdir -p /config/custom_components/androidtv_notify
```

Then use File Editor to create the three files (contents in the source folder).

---

## Step 2: Add to configuration.yaml

Minimal setup:

```yaml
notify:
  - platform: androidtv_notify
    name: philips_tv
    entity_id: media_player.android_tv_192_168_1_129
```

Full setup with all default options:

```yaml
notify:
  - platform: androidtv_notify
    name: philips_tv
    entity_id: media_player.android_tv_192_168_1_129
    duration: 1        # 0=short (~2s), 1=long (~3.5s). Default: 1
    fontsize: medium   # small | medium | large. Default: medium
```

---

## Configuration Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `entity_id` | ✅ | — | HA entity ID of the Android TV media player |
| `name` | ✅ | — | Name of the notify service (`notify.NAME`) |
| `duration` | ❌ | `1` | Toast display duration: `0` = short (~2s), `1` = long (~3.5s) |
| `fontsize` | ❌ | `medium` | Text size: `small`, `medium`, `large` |

---

## Step 3: Restart Home Assistant

Settings → System → Restart

After restart, verify the service exists under **Developer Tools → Actions** — search for `notify.philips_tv`.

---

## Step 4: Test

> **Note:** The "Fill example data" button in Developer Tools will generate `data: platform specific` which causes a validation error. Always write the YAML manually as shown above.


Basic test:

```yaml
action: notify.philips_tv
data:
  message: "Hello from Home Assistant!"
```

With all options:

```yaml
action: notify.philips_tv
data:
  title: "Front Door"
  message: "Motion detected!"
  data:
    duration: 0
    fontsize: large
```

---

## Per-Message Override

All options from the configuration can be overridden per notification via the `data` field:

```yaml
action: notify.philips_tv
data:
  title: "Security Alert"
  message: "Motion detected at front door!"
  data:
    duration: 1       # 0=short, 1=long
    fontsize: large   # small | medium | large
```

---

## Automation Examples

### Door open notification (TV must be on)

```yaml
alias: Front Door TV Notification
triggers:
  - trigger: state
    entity_id: binary_sensor.front_door
    to: "on"
conditions:
  - condition: state
    entity_id: media_player.android_tv_192_168_1_129
    state: "on"
actions:
  - action: notify.philips_tv
    data:
      title: "Door"
      message: "Front door opened!"
      data:
        fontsize: large
        duration: 1
mode: single
```

### Motion alert with large text

```yaml
actions:
  - action: notify.philips_tv
    data:
      title: "Camera"
      message: "Motion in backyard!"
      data:
        fontsize: large
        duration: 1
```

### Quick info, small text

```yaml
actions:
  - action: notify.philips_tv
    data:
      message: "Washing machine done."
      data:
        fontsize: small
        duration: 0
```

---

## Multiple TVs

```yaml
notify:
  - platform: androidtv_notify
    name: living_room_tv
    entity_id: media_player.android_tv_192_168_1_129

  - platform: androidtv_notify
    name: bedroom_tv
    entity_id: media_player.android_tv_192_168_1_200
    fontsize: large
    duration: 1
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `notify.philips_tv` not found | Check `configuration.yaml` syntax, restart HA |
| Service found but no toast | Make sure APK is installed and `MainActivity` was launched once |
| Toast shows but ignores fontsize | Some TV firmwares restrict Toast view access — falls back to default size |
| Single quotes in message break command | Already handled — single quotes are escaped automatically |

---

← [Back to APK Build](02-apk-build-install.md) | [Back to README](../README.md)
