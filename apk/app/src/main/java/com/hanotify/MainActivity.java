package com.hanotify;

import android.app.Activity;
import android.os.Bundle;

/**
 * Minimal activity with no UI.
 * Launched once to bring the app out of Android's "stopped" state,
 * which would otherwise block broadcast delivery.
 */
public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        finish(); // Close immediately — no UI needed
    }
}
