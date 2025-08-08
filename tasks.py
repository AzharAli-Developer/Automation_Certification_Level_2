import os
from RPA.PDF import PDF
from locators import Form
from locators import Browser
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
        self.selenium = Selenium()
        self.tables = Tables()
        self.archive = Archive()
        self.browser = Browser(self.selenium)

    def open_order_website(self):
        """Open RobotSpareBin Industries website"""
        self.browser.open.website()
        self.browser.order.wait_untill_visible()
        self.browser.order.order_rebot()

    def download_order_file(self):
        """Download the  orders file"""
        file_path = os.path.join(os.getcwd(), 'output/orders.csv')
        self.browser.website.download(file_path)

    def read_orders_file(self):
        """Read the orders file"""
        file_path = os.path.join(os.getcwd(), 'output/orders.csv')
        orders_data = self.tables.read_table_from_csv(path=file_path)
        return orders_data

    def fill_robot_form(self,row):
        """Fill robot form"""
        form = Form(self.selenium, row)
        form.ok.wait_untill_visible()
        form.ok.click()
        form.head.select_from_list()
        form.body.click()
        form.legs.input_text()
        form.address.input_text()
        form.order.page_contain_element()
        form.order.until_page_contains_element()
        form.order.click_button()

        #call receipt pdf.
        self.receipt_pdf(row['Order number'])

        #click order another button.
        form.another_order.wait_untill_visible()
        form.another_order.click()

    def receipt_pdf(self,number):
        """create receipt pdf"""
        self.browser.receipt.wait_untill_visible()
        html_content = self.browser.receipt.get_element_attribute()
        receipt_path =os.path.join(os.getcwd(), f'output/Receipt_pdf/Receipt{number}.pdf')
        self.pdf.html_to_pdf(html_content, receipt_path)

        #call robot screenshot method
        self.robot_screenshot(number)

    def robot_screenshot(self,number):
        """take robot screenshot"""
        self.browser.robot_preview.wait_untill_visible()
        filename = os.path.join(os.getcwd(), f'output/Screenshoot/Robot{number}.png')
        self.browser.robot_preview.capture_screenshoot(filename)

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
