package resources;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;
import java.util.concurrent.TimeUnit;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.ie.InternetExplorerDriver;

public class Base {
	
		public WebDriver driver;
		public Properties properties;
		
		public WebDriver initializeDriver() throws IOException {
			
			String userDir = System.getProperty("user.dir");
			properties = new Properties();
			FileInputStream fis = new FileInputStream(userDir + "\\src\\main\\java\\resources\\UserData.properties");
			properties.load(fis);
			
			String browserName = properties.getProperty("browser");
			
			if(browserName.contains("chrome")) {
				System.setProperty("webdriver.chrome.driver", userDir + "\\drivers\\chromedriver.exe");
				driver = new ChromeDriver();
			}
			else if(browserName.contains("firefox")) {
				System.setProperty("webdriver.gecko.driver", userDir + "\\drivers\\geckodriver.exe");
				driver = new FirefoxDriver();
			}
			else if(browserName.contains("ie")) {
				System.setProperty("webdriver.ie.driver", userDir + "\\drivers\\IEDriverServer.exe");
				driver = new InternetExplorerDriver();
			}
			driver.manage().window().maximize();
			driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
			return driver;
		}
}
