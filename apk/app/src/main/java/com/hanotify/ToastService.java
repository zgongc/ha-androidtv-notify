package com.hanotify;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.widget.Toast;

/**
 * Foreground-safe service that displays a Toast on the main thread.
 * Toast.makeText() requires a running Looper — running inside a Service
 * guarantees this, whereas a BroadcastReceiver cannot show toasts reliably
 * on older Android TV versions.
 */
public class ToastService extends Service {

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        String message = "Home Assistant Notification";
        if (intent != null && intent.hasExtra("message")) {
            message = intent.getStringExtra("message");
        }

        Toast.makeText(this, message, Toast.LENGTH_LONG).show();
        stopSelf();
        return START_NOT_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
