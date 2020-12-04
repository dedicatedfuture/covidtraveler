package contactPageSuite;

import java.io.IOException;

import org.openqa.selenium.WebDriver;
import org.testng.Assert;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Test;

import pageObjects.ContactPage;
import resources.Base;

public class VerifyContactPageNavigation extends Base {

	public WebDriver driver;
	
	@BeforeTest
	public void initialize() throws IOException {
		driver = initializeDriver();
		driver.get(properties.getProperty("homePageURL"));
	}
	
	@Test
	public void VerifyContactPageNavigationTest() {
		ContactPage contactPage = new ContactPage(driver);
		contactPage.getContactBtn().click();
		Assert.assertEquals("Contact Us", contactPage.getContactUsHeader().getText());
		driver.close();
	}
}
