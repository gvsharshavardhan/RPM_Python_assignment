import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from data_provider import *
import re


def report_errors(Issue_Heading, Issue_Description, Expected_Behaviour):
    with open("report.txt", 'a', encoding='utf-8') as f:
        f.write("a. Issue Heading: " + Issue_Heading + "\n")
        f.write("b. Issue Description: " + Issue_Description + "\n")
        f.write("c. Expected Behaviour: " + Expected_Behaviour + "\n")
        f.write("\n")
    return Issue_Heading


browserName = "chrome"

if browserName == "chrome":
    driver = webdriver.Chrome(ChromeDriverManager().install())
elif browserName == "firefox":
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
else:
    raise Exception("Driver is not found!!")

driver.implicitly_wait(5)
driver.get("https://rpmsoftware.com/hiring/2020/integration-test/form-edit.html")
print(driver.title)

# Employee Name
driver.find_element(By.ID, "FL:_ctl0:_ctl3").send_keys("Isabel Britt")
# Summary
driver.find_element(By.ID, "FL:_ctl1:_ctl4").send_keys("This is a test Employee Summary.")

# select department
sel_dept = Select(driver.find_element_by_xpath("//select[@name='FL:_ctl3:_ctl3']"))
sel_dept.select_by_visible_text("Management")

# Salary
driver.find_element(By.ID, "FL:_ctl4:_ctl3").send_keys("$50,000.00")

# Address
driver.find_element(By.ID, "FL_latTxt_5").send_keys("34.833850°")
driver.find_element(By.ID, "FL_longTxt_5").send_keys("106.748580°")

# select Work Location
sel_work_location = Select(driver.find_element_by_xpath("//select[@name='FL:_ctl6:_ctl3']"))
sel_work_location.select_by_visible_text("Headquarters")

# joining date
driver.find_element(By.ID, "FL:_ctl8:_ctl3").send_keys("04-01-2018")

# employee still active as "yes"
driver.find_element(By.ID, "FL__ctl3_9").click()

# Employee Cubicle needs
metrics = driver.find_elements_by_xpath("//select[contains(@class,'forMeasurement')]")

for metric in metrics:
    sel_option = Select(metric)
    sel_option.select_by_visible_text("in")

# enter width
driver.find_element(By.XPATH, "//input[contains(@class,'measurement')]").send_keys("21")

# enter length
driver.find_element(By.XPATH, "//input[contains(@class,'forMeasurement')]").send_keys("47")

# enter color
color_ele = driver.find_element(By.XPATH, "(//div[contains(text(),'Employee Details')]/ancestor::tbody//input)[last()]")
color_ele.send_keys("Brown")

car1_elements = driver.find_elements_by_xpath(
    "(//span[contains(text(),'Car Details')]/following-sibling::span//tr//input)[position( )>=1 and position( )<=6]")
car2_elements = driver.find_elements_by_xpath(
    "(//span[contains(text(),'Car Details')]/following-sibling::span//tr//input)[position( )>=7 and position( )<=12]")

for i in range(len(car1_elements)):
    car1_elements[i].send_keys(list(Car1_details.items())[i][1])
for i in range(len(car2_elements)):
    car2_elements[i].send_keys(list(Car2_details.items())[i][1])

time.sleep(1)

# click submit button
driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()

time.sleep(1)

# verify page url
url = driver.current_url
print(url)
assert url == URL, report_errors(
    "URL Mismatch", "URL is not as expected", "URL should be " + URL)

# verify the Employee name is displayed as a header on the page
assert len(driver.find_elements(By.XPATH, "//h1[text()='Isabel Britt']")) > 0, report_errors(
    "No header with employee name", "No header with employee name",
    "Employee name should be as a header at the top of the page")

# verify employee name
employee_name = driver.find_element_by_xpath("//span[contains(text(),'Employee Name')]/following-sibling::span").text
assert employee_name == Employee_Name, report_errors("Employee name mismatch", "Employee name is not as expected",
                                                     "Employee name should be " + Employee_Name)

# verify summary
summary = driver.find_element_by_xpath("//span[contains(text(),'Summary')]/following-sibling::span").text
assert Summary in summary, report_errors("Employee Summary Mismatch", "Employee Summary is not as expected",
                                         "Employee Summary should be " + Summary)

# verify department
department = driver.find_element_by_xpath("//span[contains(text(),'Department')]/following-sibling::span").text
assert department == Department, report_errors("Department name Mismatch", "Department name is not as expected",
                                               "Department name should be " + Department)

# verify salary
salary = driver.find_element_by_xpath("//span[contains(text(),'Salary')]/following-sibling::span").text
assert salary == Salary, report_errors("Salary amount Mismatch", "Salary amount is not as expected",
                                       "Salary amount should be " + Salary)

# verify Address
address = driver.find_element_by_xpath("//span[contains(text(),'Address')]/following-sibling::span").text
assert Address_Lat in address, report_errors("Address Mismatch", "Address is not as expected(Latitude coordinates)",
                                             "Latitude coordinates should be " + Address_Lat)
assert Address_Long in address, report_errors("Address Mismatch", "Address is not as expected(Longitude coordinates)",
                                              "Longitude coordinates should be " + Address_Lat)

# verify latitude and longitude patterns
address = driver.find_element_by_xpath("//span[contains(text(),'Address')]/following-sibling::span").text
coordinates = re.findall("[0-9]{1,3}.[0-9]{6}°", address)
assert len(coordinates) == 2, report_errors("Coordinates pattern Mismatch", "Coordinates pattern is not as expected",
                                            "Coordinates pattern should be 'xxx.xxxxxx°' ")

# verify Map is a link
map = driver.find_element_by_xpath("//*[text()='Map']").tag_name
assert map.lower() == "a", report_errors("Map is not a hyperlink", "Map is not a hyperlink",
                                         "Map should be a hyperlink")
map_attr = driver.find_element_by_xpath("//*[text()='Map']").get_attribute("href")
assert map_attr is not None, report_errors("Map is not a hyperlink", "Map is not a hyperlink",
                                           "Map should be a hyperlink")

# verify Is the employee still active
is_active = driver.find_element_by_xpath(
    "//span[contains(text(),'Is the employee still active?')]/following-sibling::span").text
assert is_active.lower() == "yes", report_errors("Employee active status Mismatch",
                                                 "Employee active status is not as expected",
                                                 "Employee active status should be 'Yes'")

# verify Employee Cubicle needs
employee_details = driver.find_elements_by_xpath(
    "(//div[contains(text(),'Employee Details')]/ancestor::tr//following-sibling::tr//div["
    "@class='TableCell--input-container'])[position()>1 and position()<5]")
for i in range(len(employee_details)):
    assert employee_details[i].text == list(Employee_Cubicle_needs.items())[i][1], report_errors(
        "{} Mismatch".format(list(Employee_Cubicle_needs.items())[i][0]),
        "{} is not as expected".format(list(Employee_Cubicle_needs.items())[i][0]),
        "{} should be {}".format(list(Employee_Cubicle_needs.items())[i][0], list(Employee_Cubicle_needs.items())[i][1])
    )

# verify Car 1 Details
car1_details = driver.find_elements_by_xpath(
    "//span[contains(text(),'Car Details')]/..//tr[2]//div[@class='TableCell--input-container']")
for i in range(len(car1_details)):
    assert car1_details[i].text == list(Car1_details.items())[i][1], report_errors(
        "Car 1 {} Mismatch".format(list(Car1_details.items())[i][0]),
        "Car 1  {} is not as expected".format(list(Car1_details.items())[i][0]),
        "Car 1  {} should be {}".format(list(Car1_details.items())[i][0],
                                        list(Car1_details.items())[i][1])
    )

# verify Car 2 Details
car2_details = driver.find_elements_by_xpath(
    "//span[contains(text(),'Car Details')]/..//tr[3]//div[@class='TableCell--input-container']")

for i in range(len(car2_details)):
    assert car2_details[i].text == list(Car2_details.items())[i][1], report_errors(
        "Car 2 {} Mismatch".format(list(Car2_details.items())[i][0]),
        "Car 2  {} is not as expected".format(list(Car2_details.items())[i][0]),
        "Car 2  {} should be {}".format(list(Car2_details.items())[i][0],
                                        list(Car2_details.items())[i][1])
    )

# verify Date of Joining
date_of_Joining = driver.find_element_by_xpath(
    "//span[contains(text(),'Date of Joining')]/following-sibling::span").text
assert date_of_Joining == Date_of_Joining, report_errors("Date of Joining Mismatch",
                                                         "Date of Joining is not as expected",
                                                         "Date of Joining should be " + Date_of_Joining + " but "
                                                                                                          "displayed "
                                                                                                          "as " +
                                                         date_of_Joining)

driver.quit()
