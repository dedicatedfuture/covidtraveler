package pageObjects;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

import resources.Base;

public class ContactPage extends Base{
	
	public WebDriver driver;
	
	public ContactPage(WebDriver driver) {
		this.driver = driver;
		PageFactory.initElements(driver, this);
	}

	@FindBy(linkText = "Contact")
	private WebElement contactBtn;
	
	@FindBy(tagName = "h1")
	private WebElement contactUsHeader;
	
	@FindBy(linkText = "Bill Zerega")
	private WebElement billZeregaLink;
	
	@FindBy(linkText = "Arsi Pansheria")
	private WebElement arsiPansheriaLink;
	
	@FindBy(linkText = "Tom Shannon")
	private WebElement tomShannonLink;
	
	@FindBy(name = "name")
	private WebElement nameTxt;
	
	@FindBy(name = "email")
	private WebElement emailTxt;
	
	@FindBy(name = "body")
	private WebElement bodyTxt;
	
	@FindBy(css = "input[type = 'submit']")
	private WebElement submitBtn;
	
	public WebElement getContactBtn() {
		 return contactBtn;
	}
	
	public WebElement getContactUsHeader() {
		 return contactUsHeader;
	}
	
	public WebElement getArsiPansheriaLink() {
		 return arsiPansheriaLink;
	}
	
	public WebElement getBillZeregaLink() {
		 return billZeregaLink;
	}
	
	public WebElement geTomShannonLink() {
		 return tomShannonLink;
	}
	
	public WebElement getNameTxt() {
		 return nameTxt;
	}
	
	public WebElement getEmailTxt() {
		 return emailTxt;
	}
	
	public WebElement getBodyTxt() {
		 return bodyTxt;
	}
	
	public WebElement getSubmitBtn() {
		 return submitBtn;
	}
}
