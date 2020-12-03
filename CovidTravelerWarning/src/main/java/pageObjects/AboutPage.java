package pageObjects;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

public class AboutPage {

	public WebDriver driver;

	public AboutPage(WebDriver driver) {
		this.driver = driver;
		PageFactory.initElements(driver, this);
	}

	@FindBy(linkText = "About")
	private WebElement aboutBtn;
	
	@FindBy(css = "p[class = 'aboutP']")
	private WebElement aboutParagraph;
	
	public WebElement getAboutBtn() {
		 return aboutBtn;
	}
	
	public WebElement getAboutParagraph() {
		 return aboutParagraph;
	}
}
