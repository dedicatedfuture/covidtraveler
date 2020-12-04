package newsPageSuite;

import java.io.IOException;

import org.openqa.selenium.WebDriver;
import org.testng.Assert;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Test;
import pageObjects.NewsPage;
import resources.Base;

public class VerifyNewsPageNavigation extends Base {

	public WebDriver driver;
	
	@BeforeTest
	public void initialize() throws IOException {
		driver = initializeDriver();
		driver.get(properties.getProperty("homePageURL"));
	}
	
	@Test
	public void VerifyNewsPageNavigationTest() {
		NewsPage newsPage = new NewsPage(driver);
		newsPage.getNewsBtn().click();
		Assert.assertEquals("Coronavirus News from CDC", newsPage.getNewsHeader().getText());
		driver.close();
	}
}
