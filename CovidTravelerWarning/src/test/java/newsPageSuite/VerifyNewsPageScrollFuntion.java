package newsPageSuite;

import java.io.IOException;

import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Test;
import pageObjects.NewsPage;
import resources.Base;

public class VerifyNewsPageScrollFuntion extends Base {

	public WebDriver driver;
	
	@BeforeTest
	public void initialize() throws IOException {
		driver = initializeDriver();
		driver.get(properties.getProperty("homePageURL"));
	}
	
	@Test
	public void VerifyNewsPageScrollFuntionTest() throws InterruptedException {
		NewsPage newsPage = new NewsPage(driver);
		newsPage.getNewsBtn().click();
		
		JavascriptExecutor js = (JavascriptExecutor) driver;
		js.executeScript("window.scrollBy(0,4000)");
		Thread.sleep(1000);
		js.executeScript("window.scrollBy(0,-4000)");
		Thread.sleep(1000);
		
		driver.close();
	}
}
