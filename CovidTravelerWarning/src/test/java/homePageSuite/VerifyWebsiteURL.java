package homePageSuite;

import java.io.IOException;
import org.openqa.selenium.WebDriver;
import org.testng.Assert;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Test;

import resources.Base;

public class VerifyWebsiteURL extends Base {
	
	public WebDriver driver;
	
	@BeforeTest
	public void initialize() throws IOException {
		driver = initializeDriver();
	}
	
	@Test
	public void VerifyWebsiteURLTest() throws IOException {
		
		driver.get(properties.getProperty("homePageURL"));
		String websiteTitle = driver.getTitle();
		Assert.assertEquals("Covid Traveler Warning", websiteTitle);
		driver.close();
	}

}
