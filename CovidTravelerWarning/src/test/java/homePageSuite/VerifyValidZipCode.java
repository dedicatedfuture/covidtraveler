package homePageSuite;

import java.io.IOException;

import org.openqa.selenium.JavascriptExecutor;
import org.testng.Assert;
import org.testng.annotations.AfterTest;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;


import pageObjects.HomePage;
import resources.Base;

public class VerifyValidZipCode extends Base {
	
	@BeforeTest
	public void initialize() throws IOException {
		driver = initializeDriver();
		driver.get(properties.getProperty("homePageURL"));
	}
	
	@AfterTest
	public void closeAll() {
		driver.close();
	}
	
	@Test(dataProvider = "getZipCode")
	public void VerifyValidZipCodeTest(String zipCode) throws InterruptedException {
		HomePage homePage = new HomePage(driver);
		homePage.getHomeBtn().click();
		Thread.sleep(2000);
		homePage.getZipCodeTxtBox().sendKeys(zipCode);
		Thread.sleep(3000);
		
		JavascriptExecutor js = (JavascriptExecutor) driver;
		js.executeScript("window.scrollBy(0,300)");
		
		homePage.getSubmitBtn().click();
		Assert.assertTrue(homePage.getPieChartImage().isDisplayed());
	}
	
	@DataProvider
	public String[] getZipCode() {
		String[] zipCode = new String[2];
		zipCode[0] = "19454";
		zipCode[1] = "33319";
		return zipCode;
	}
	

}
