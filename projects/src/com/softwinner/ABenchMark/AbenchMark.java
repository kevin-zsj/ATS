package com.softwinner.ABenchMark;

import com.android.uiautomator.core.UiObject;
import com.android.uiautomator.core.UiObjectNotFoundException;
import com.android.uiautomator.core.UiSelector;
import com.android.uiautomator.testrunner.UiAutomatorTestCase;

public class AbenchMark extends UiAutomatorTestCase {

	public void testAntutu() throws UiObjectNotFoundException{
		sleep(5000);
		UiObject Test = new UiObject(new UiSelector().resourceId("com.antutu.ABenchMark:id/start_test_text"));
		Test.click();
		sleep(1000);
	}
	
	/*
	 * set up open the AbenchMark
	 */
	@Override
	public void setUp() throws Exception {
		super.setUp();
		getUiDevice().pressHome();
		Runtime.getRuntime()
				.exec("am start -n com.antutu.ABenchMark/.ABenchMarkStart");
	}

	/*
	 * tear Down close the AbenchMark
	 */

//	@Override
//	public void tearDown() throws Exception {
//		super.tearDown();
//		Process p = Runtime.getRuntime().exec(
//				"am force-stop com.antutu.ABenchMark");
//		p.waitFor();
//	}
}
