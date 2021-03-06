package homePageSuite;

import java.io.IOException;

import org.openqa.selenium.WebDriver;
import org.testng.Assert;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Test;

import pageObjects.HomePage;
import resources.Base;

public class VerifyHomePageUI extends Base {
	
	public WebDriver driver;
	
	@BeforeTest
	public void initialize() throws IOException {
		driver = initializeDriver();
		driver.get(properties.getProperty("homePageURL"));
	}
	
	@Test
	public void VerifyHomePageUITest() {
		HomePage homePage = new HomePage(driver);
		homePage.getHomeBtn().click();
		Assert.assertEquals("Welcome to COVID Traveler Warning",homePage.getHeadingOne().getText());
		//Assert.assertEquals(" to COVID Traveler Warning",homePage.getHeadingOne().getText());
		Assert.assertTrue(homePage.getZipCodeTxtBox().isDisplayed());
		Assert.assertTrue(homePage.getSubmitBtn().isDisplayed());
		driver.close();
	}

}
