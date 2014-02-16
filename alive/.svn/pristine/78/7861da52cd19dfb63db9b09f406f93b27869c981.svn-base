
package com.example.demo.utils;

import android.app.Activity;
import android.app.PendingIntent;
import android.content.Intent;
import android.telephony.SmsManager;
import android.widget.Toast;

public class SMSHelper {
    SmsManager smsManager;

    public boolean sendSMS(Activity activity) {
        if (smsManager == null) {
            smsManager = SmsManager.getDefault();
        }

        PendingIntent pendingIntent = PendingIntent.getActivity(activity, 0,
                new Intent(), 0);
        smsManager.sendTextMessage("+8618601065423", null, "test message",
                pendingIntent, null);

        Toast.makeText(activity, "·¢ËÍ³É¹¦", Toast.LENGTH_LONG).show();
        return true;
    }
}
