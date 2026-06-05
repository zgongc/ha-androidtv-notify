package com.hanotify;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

/**
 * Receives the com.hanotify.SHOW_TOAST broadcast and delegates
 * to ToastService so the toast can run on the main thread.
 *
 * Trigger via ADB:
 *   adb shell am broadcast -a com.hanotify.SHOW_TOAST --es message 'Hello!'
 */
public class NotifyReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        String message = intent.getStringExtra("message");
        if (message == null) message = "Home Assistant Notification";

        Intent service = new Intent(context, ToastService.class);
        service.putExtra("message", message);
        context.startService(service);
    }
}
