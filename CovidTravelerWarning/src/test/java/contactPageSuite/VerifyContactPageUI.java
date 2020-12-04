package contactPageSuite;

import java.io.IOException;

import org.openqa.selenium.WebDriver;
import org.testng.Assert;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Test;

import pageObjects.ContactPage;
import resources.Base;

public class VerifyContactPageUI extends Base {

	public WebDriver driver;
	
	@BeforeTest
	public void initialize() throws IOException {
		driver = initializeDriver();
		driver.get(properties.getProperty("homePageURL"));
	}
	
	@Test
	public void VerifyContactPageUITest() {
		ContactPage contactPage = new ContactPage(driver);
		contactPage.getContactBtn().click();
		Assert.assertEquals("Contact Us", contactPage.getContactUsHeader().getText());
		Assert.assertEquals("Bill Zerega", contactPage.getBillZeregaLink().getText());
		Assert.assertEquals("Arsi Pansheria", contactPage.getArsiPansheriaLink().getText());
		Assert.assertEquals("Tom Shannon", contactPage.geTomShannonLink().getText());
		Assert.assertTrue(contactPage.getNameTxt().isDisplayed());
		Assert.assertTrue(contactPage.getEmailTxt().isDisplayed());
		Assert.assertTrue(contactPage.getBodyTxt().isDisplayed());
		driver.close();
	}
}
