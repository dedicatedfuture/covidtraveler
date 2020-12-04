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

public class VerifyInvalidZipCode extends Base {
	
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
	public void VerifyInvalidZipCodeTest(String zipCode) throws InterruptedException {
		HomePage homePage = new HomePage(driver);
		homePage.getHomeBtn().click();
		homePage.getZipCodeTxtBox().sendKeys(zipCode);
		
		JavascriptExecutor js = (JavascriptExecutor) driver;
		js.executeScript("window.scrollBy(0,300)");
		
		homePage.getSubmitBtn().click();
		Assert.assertEquals(homePage.getErrorMsg().getText(), "Something went wrong :");
		Thread.sleep(1000);
	}
	
	@DataProvider
	public String[] getZipCode() {
		String[] zipCode = new String[3];
		zipCode[0] = "3345";
		zipCode[1] = "asdfgf";
		zipCode[2] = "123abc";
		return zipCode;
	}
	

}
