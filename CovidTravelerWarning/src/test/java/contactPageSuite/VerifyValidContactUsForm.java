package contactPageSuite;

import java.io.IOException;

import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Test;

import pageObjects.ContactPage;
import resources.Base;

public class VerifyValidContactUsForm extends Base {

	public WebDriver driver;
	
	@BeforeTest
	public void initialize() throws IOException {
		driver = initializeDriver();
		driver.get(properties.getProperty("homePageURL"));
	}
	
	@Test
	public void VerifyValidContactUsFormTest() throws InterruptedException {
		ContactPage contactPage = new ContactPage(driver);
		contactPage.getContactBtn().click();
		Thread.sleep(3000);
		contactPage.getNameTxt().sendKeys("Joe");
		contactPage.getEmailTxt().sendKeys("abc@gmail.com");
		contactPage.getBodyTxt().sendKeys("Good Job");
		
		JavascriptExecutor js = (JavascriptExecutor) driver;
		js.executeScript("window.scrollBy(0,500)");
		contactPage.getSubmitBtn().click();
		driver.close();
	}
}
