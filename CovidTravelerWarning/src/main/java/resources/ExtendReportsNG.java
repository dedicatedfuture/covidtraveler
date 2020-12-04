package resources;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.reporter.ExtentSparkReporter;

public class ExtendReportsNG {

	static ExtentReports extent;
	public static ExtentReports getReportObject() {
		
		String path = System.getProperty("user.dir") + "\\reports/index.html";
		ExtentSparkReporter reporter = new ExtentSparkReporter(path);
		reporter.config().setReportName("Covid Travel Warning");
		reporter.config().setDocumentTitle("Covid Travel Warning Test Report");
		
		 extent = new ExtentReports();
		 extent.attachReporter(reporter);
		 extent.setSystemInfo("Tester", "Team 3");
		 
		 return extent;
	}
}
