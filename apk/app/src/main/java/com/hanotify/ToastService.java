package com.hanotify;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.text.Html;
import android.widget.Toast;

/**
 * Service that displays a Toast on the main thread.
 *
 * Supported extras (all optional):
 *   message      (String)  — notification body
 *   title        (String)  — prepended in bold if provided
 *   duration     (int)     — 0 = SHORT (~2s), 1 = LONG (~3.5s), default 1
 *   fontsize     (String)  — "small", "medium" (default), "large"
 */
public class ToastService extends Service {

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        String message = "Home Assistant Notification";
        String title = null;
        int duration = Toast.LENGTH_LONG;
        float textSize = 16f; // medium default (sp)

        if (intent != null) {
            if (intent.hasExtra("message")) {
                message = intent.getStringExtra("message");
            }
            if (intent.hasExtra("title")) {
                title = intent.getStringExtra("title");
            }
            if (intent.hasExtra("duration")) {
                int d = intent.getIntExtra("duration", 1);
                duration = (d == 0) ? Toast.LENGTH_SHORT : Toast.LENGTH_LONG;
            }
            if (intent.hasExtra("fontsize")) {
                String fs = intent.getStringExtra("fontsize");
                if ("small".equals(fs)) textSize = 12f;
                else if ("large".equals(fs)) textSize = 22f;
                else textSize = 16f; // medium
            }
        }

        // Build display text — title in bold if provided
        String display;
        if (title != null && !title.isEmpty()) {
            display = title + ": " + message;
        } else {
            display = message;
        }

        Toast toast = Toast.makeText(this, display, duration);

        // Apply font size to the default toast TextView
        try {
            android.view.View view = toast.getView();
            if (view != null) {
                android.widget.TextView tv = view.findViewById(android.R.id.message);
                if (tv != null) tv.setTextSize(textSize);
            }
        } catch (Exception ignored) {
            // Some TV firmwares restrict view access — fall back to default size
        }

        toast.show();
        stopSelf();
        return START_NOT_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
