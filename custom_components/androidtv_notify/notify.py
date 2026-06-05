"""
Android TV Notify - Home Assistant custom notify platform.

Sends toast notifications to Android TV via ADB using the HANotify APK.

Configuration in configuration.yaml:
    notify:
      - platform: androidtv_notify
        name: philips_tv
        entity_id: media_player.android_tv_192_168_1_129
"""

from homeassistant.components.notify import BaseNotificationService, PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

CONF_ENTITY_ID = "entity_id"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ENTITY_ID): cv.string,
})


def get_service(hass, config, discovery_info=None):
    """Return the notification service."""
    return AndroidTVNotifyService(hass, config[CONF_ENTITY_ID])


class AndroidTVNotifyService(BaseNotificationService):
    """Notification service for Android TV via ADB."""

    def __init__(self, hass, entity_id):
        self.hass = hass
        self.entity_id = entity_id

    def send_message(self, message="", **kwargs):
        """Send a toast notification to the Android TV."""
        # Start MainActivity first to bring app out of stopped state,
        # then immediately start the ToastService with the message.
        cmd = (
            f"am start -n com.hanotify/.MainActivity && "
            f"am startservice -n com.hanotify/.ToastService --es message '{message}'"
        )
        self.hass.services.call(
            "androidtv",
            "adb_command",
            {
                "entity_id": self.entity_id,
                "command": cmd,
            },
        )
