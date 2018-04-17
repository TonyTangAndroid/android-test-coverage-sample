package com.example.core;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;

public class CoreActivity extends AppCompatActivity {
    public static final String TAG = "CoreActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_core);
        Log.v(TAG, String.valueOf(calculateRectArea(2.0, 3.0)));
        Log.v(TAG, String.valueOf(calculateTriangleArea(5.0, 2.0)));
    }

    public double calculateRectArea(double x, double y) {
        return x * y;
    }

    public double calculateTriangleArea(double a, double t) {
        return a * t * 0.5;
    }
}
