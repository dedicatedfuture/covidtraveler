package pageObjects;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

public class NewsPage {

	public WebDriver driver;
	
	public NewsPage(WebDriver driver) {
		this.driver = driver;
		PageFactory.initElements(driver, this);
	}
	
	@FindBy(linkText = "News")
	private WebElement newsBtn;
	
	@FindBy(css = "h2[class = 'news-header']")
	private WebElement newsHeader;
	
	@FindBy(css = "div[class = 'row1 rows'] h3 a")
	private WebElement newsLink;
	
	public WebElement getNewsBtn() {
		 return newsBtn;
	}
	
	public WebElement getNewsHeader() {
		 return newsHeader;
	}
	
	public WebElement getNewsLink() {
		 return newsLink;
	}
}
