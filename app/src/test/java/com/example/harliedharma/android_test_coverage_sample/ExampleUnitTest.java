package com.example.harliedharma.android_test_coverage_sample;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Example local unit test, which will execute on the development machine (host).
 *
 * @see <a href="http://d.android.com/tools/testing">Testing documentation</a>
 */
public class ExampleUnitTest {
    @Test
    public void addition_isCorrect() throws Exception {
        assertEquals(4, 2 + 2);
    }

    @Test
    public void test_Area() throws Exception {
        assertEquals( 100.0, new MainActivity().calculateSquareArea(10.0), 1e-7 );
        assertEquals(Math.PI * 5.0 * 5.0, new MainActivity().calculateCircleArea(5.0), 1e-7);
    }
}