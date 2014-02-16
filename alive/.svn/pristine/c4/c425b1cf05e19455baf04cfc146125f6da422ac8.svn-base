package com.example.demo;

import com.example.demo.utils.SMSHelper;

import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import android.view.MenuItem;

public class MainActivity extends Activity {

    SMSHelper smsHelper = new SMSHelper();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    // @Override
    // public boolean onKeyDown(int keyCode, KeyEvent event) {
    // if (keyCode == KeyEvent.KEYCODE_BACK) {
    // Log.d("tag", "keyCode == KeyEvent.KEYCODE_BACK");
    // return false;
    // } else {
    // return super.onKeyDown(keyCode, event);
    // }
    // }

    @Override
    public boolean onOptionsItemSelected(MenuItem menu) {
        switch (menu.getItemId()) {
            case R.id.action_settings:
                this.smsHelper.sendSMS(this);
                break;

            default:
                break;
        }

        return true;
    }
}
