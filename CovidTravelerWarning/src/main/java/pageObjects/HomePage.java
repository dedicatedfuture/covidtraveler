package pageObjects;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

public class HomePage {

	public WebDriver driver;

	public HomePage(WebDriver driver) {
		this.driver = driver;
		PageFactory.initElements(driver, this);
	}

	@FindBy(linkText = "Home")
	private WebElement homeBtn;
	
	@FindBy(css = "h1[class = 'headings']")
	private WebElement headingOne;
	
	@FindBy(name = "zipCode")
	private WebElement zipCodeTxtBox;
	
	@FindBy(css = "input[type='submit']")
	private WebElement submitBtn;
	
	@FindBy(tagName = "img")
	private WebElement pieChartImage;
	
	@FindBy(css = "h2[class = 'headings']")
	private WebElement errorMsg;
	
	public WebElement getHomeBtn() {
		 return homeBtn;
	}
	
	public WebElement getHeadingOne() {
		 return headingOne;
	}
	
	public WebElement getZipCodeTxtBox() {
		 return zipCodeTxtBox;
	}
	
	public WebElement getSubmitBtn() {
		 return submitBtn;
	}
	
	public WebElement getPieChartImage() {
		 return pieChartImage;
	}
	
	public WebElement getErrorMsg() {
		 return errorMsg;
	}
}
