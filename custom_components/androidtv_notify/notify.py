"""
Android TV Notify — Home Assistant custom notify platform.

Sends toast notifications to Android TV via ADB using the HANotify APK.

Configuration in configuration.yaml:

    notify:
      - platform: androidtv_notify
        name: philips_tv
        entity_id: media_player.android_tv_192_168_1_129
        duration: 1          # 0=short (~2s), 1=long (~3.5s)
        fontsize: medium     # small | medium | large

Usage:

    action: notify.philips_tv
    data:
      message: "Motion detected!"
      title: "Front Door"
      data:
        duration: 0
        fontsize: large
"""

from homeassistant.components.notify import BaseNotificationService, PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

CONF_ENTITY_ID = "entity_id"
CONF_DURATION  = "duration"
CONF_FONTSIZE  = "fontsize"

FONTSIZES = ["small", "medium", "large"]

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ENTITY_ID):                  cv.string,
    vol.Optional(CONF_DURATION, default=1):        vol.In([0, 1]),
    vol.Optional(CONF_FONTSIZE, default="medium"): vol.In(FONTSIZES),
})


def get_service(hass, config, discovery_info=None):
    """Return the notification service."""
    return AndroidTVNotifyService(hass, config)


class AndroidTVNotifyService(BaseNotificationService):
    """Notification service for Android TV via ADB."""

    def __init__(self, hass, config):
        self.hass             = hass
        self.entity_id        = config[CONF_ENTITY_ID]
        self.default_duration = config[CONF_DURATION]
        self.default_fontsize = config[CONF_FONTSIZE]

    def send_message(self, message="", **kwargs):
        """Send a toast notification to the Android TV."""
        # data is a nested dict — HA passes it as-is if it's a valid dict
        # If None or invalid (e.g. "platform specific"), fall back to empty dict
        raw_data = kwargs.get("data")
        data     = raw_data if isinstance(raw_data, dict) else {}

        title    = kwargs.get("title") or ""
        duration = data.get("duration", self.default_duration)
        fontsize = data.get("fontsize", self.default_fontsize)

        # Fallback to defaults if invalid
        if duration not in (0, 1):
            duration = self.default_duration
        if fontsize not in FONTSIZES:
            fontsize = self.default_fontsize

        # Escape single quotes in user-supplied strings
        message = str(message).replace("'", "\\'")
        title   = str(title).replace("'", "\\'")

        extras = f"--es message '{message}' --ei duration {duration} --es fontsize '{fontsize}'"
        if title:
            extras += f" --es title '{title}'"

        cmd = (
            f"am start -n com.hanotify/.MainActivity; sleep 1; "
            f"am startservice -n com.hanotify/.ToastService {extras}"
        )

        self.hass.services.call(
            "androidtv",
            "adb_command",
            {"entity_id": self.entity_id, "command": cmd},
        )
