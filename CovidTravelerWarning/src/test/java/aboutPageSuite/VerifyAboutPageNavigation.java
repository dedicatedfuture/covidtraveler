package aboutPageSuite;

import java.io.IOException;

import org.openqa.selenium.WebDriver;
import org.testng.Assert;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Test;

import pageObjects.AboutPage;
import resources.Base;

public class VerifyAboutPageNavigation extends Base {

	public WebDriver driver;
	
	@BeforeTest
	public void initialize() throws IOException {
		driver = initializeDriver();
		driver.get(properties.getProperty("homePageURL"));
	}
	
	@Test
	public void VerifyAboutPageNavigationTest() {
		AboutPage aboutPage = new AboutPage(driver);
		aboutPage.getAboutBtn().click();
		Assert.assertTrue(aboutPage.getAboutParagraph().getText().contains("Most people infected with the COVID-19 virus"));
		driver.close();
	}
}
