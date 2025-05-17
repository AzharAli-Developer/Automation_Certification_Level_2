import os
from RPA.PDF import PDF
from RPA.HTTP import HTTP
from RPA.Tables import  Tables
from RPA.Archive import Archive
from RPA.Browser.Selenium import Selenium


class Order_robots:
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    def __init__(self):
        self.pdf = PDF()
        self.http = HTTP()
        self.tables = Tables()
        self.archive = Archive()
        self.browser = Selenium()

    def open_order_website(self):
        """Open RobotSpareBin Industries website"""
        self.browser.open_available_browser('https://robotsparebinindustries.com', maximized=True)
        self.browser.wait_until_element_is_visible('//a[text()="Order your robot!"]',timeout=10)
        self.browser.click_element('//a[text()="Order your robot!"]')

    def download_order_file(self):
        """Download the  orders file"""
        order_file_path = os.path.join(os.getcwd(), 'output/orders.csv')
        self.http.download(url=' https://robotsparebinindustries.com/orders.csv', target_file=order_file_path, overwrite=True)

    def read_orders_file(self):
        """Read the orders file"""
        order_file_path = os.path.join(os.getcwd(), 'output/orders.csv')
        orders_data = self.tables.read_table_from_csv(path=order_file_path)
        return orders_data

    def fill_robot_form(self,row):
        """Fill robot form"""
        self.browser.wait_until_element_is_visible('//button[@class="btn btn-dark"][text()="OK"]')
        self.browser.click_element('//button[@class="btn btn-dark"][text()="OK"]')
        self.browser.select_from_list_by_value('//select[@id="head"]', f"{row['Head']}")
        self.browser.click_element(f'//label[@for="id-body-{row["Body"]}"]')
        self.browser.input_text('//input[contains(@class ,"form-control")  and  @type="number"]', f"{row['Legs']}")#if we are want to use multiple locators in one
        self.browser.input_text('//input[@id="address" and @type="text" and @class="form-control"]', f"{row['Address']}")
        while self.browser.does_page_contain_element('//button[@id="order"]'):
            self.browser.wait_until_page_contains_element('//button[@id="order"]', timeout=10)
            self.browser.click_button('//button[@id="order"]')

        #call receipt pdf.
        self.receipt_pdf(row['Order number'])
        #click order another button.
        self.browser.wait_until_element_is_visible('//button[@id="order-another"]', timeout=10)
        self.browser.click_button('//button[@id="order-another"]')

    def receipt_pdf(self,number):
        """create receipt pdf"""
        self.browser.wait_until_element_is_visible('//div[@id="receipt"]',timeout=10)
        html_content = self.browser.get_element_attribute('//div[@id="receipt"]','innerHTML')
        receipt_path =os.path.join(os.getcwd(), f'output/Receipt_pdf/Receipt{number}.pdf')
        self.pdf.html_to_pdf(html_content, receipt_path)
        #call robot screenshot method
        self.robot_screenshot(number)

    def robot_screenshot(self,number):
        """take robot screenshot"""
        self.browser.wait_until_element_is_visible('//div[@id="robot-preview-image"]')
        filename = os.path.join(os.getcwd(), f'output/Screenshoot/Robot{number}.png')
        self.browser.capture_element_screenshot('//div[@id="robot-preview-image"]', filename=filename)
        #call embed screenshot method
        self.embed_screenshot_to_receipt(number)

    def embed_screenshot_to_receipt(self, number):
        """take robot screenshot and append  receipt pdf file """
        receipt_pdf = os.path.join(os.getcwd(), f'output/Receipt_pdf/Receipt{number}.pdf')
        robot_screenshoot = os.path.join(os.getcwd(), f'output/Screenshoot/Robot{number}.png')
        list_of_files = [receipt_pdf, robot_screenshoot]
        self.pdf.add_files_to_pdf(files=list_of_files, target_document=receipt_pdf)

    def receipt_zip_file(self):
        """make zip file of receipt folder"""
        folder_path = os.path.join(os.getcwd(), 'output/Receipt_pdf')
        self.archive.archive_folder_with_zip(folder=folder_path, archive_name='Receipt.zip')

orders = Order_robots()
orders.open_order_website()
orders.download_order_file()
data = orders.read_orders_file()
for row in data:
    orders.fill_robot_form(row)
orders.receipt_zip_file()
