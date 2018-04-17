package com.example.harliedharma.android_test_coverage_sample;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;

public class MainActivity extends AppCompatActivity {
    public static final String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Log.v(TAG, String.valueOf(calculateSquareArea(2.0)));
        Log.v(TAG, String.valueOf(calculateCircleArea(7.0)));
    }

    public double calculateSquareArea(double x) {
        return x * x;
    }

    public double calculateCircleArea(double r) {
        return Math.PI * r * r;
    }
}
