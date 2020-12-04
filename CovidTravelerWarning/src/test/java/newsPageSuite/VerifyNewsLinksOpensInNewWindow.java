package newsPageSuite;

import java.io.IOException;

import org.openqa.selenium.WebDriver;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Test;
import pageObjects.NewsPage;
import resources.Base;

public class VerifyNewsLinksOpensInNewWindow extends Base {

	public WebDriver driver;
	
	@BeforeTest
	public void initialize() throws IOException {
		driver = initializeDriver();
		driver.get(properties.getProperty("homePageURL"));
	}
	
	@Test
	public void VerifyNewsLinkTest() throws InterruptedException {
		NewsPage newsPage = new NewsPage(driver);
		newsPage.getNewsBtn().click();
		newsPage.getNewsLink().click();
		driver.quit();
	}
}
