from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
import os
from RPA.Tables import  Tables


class Order_robots_from_RobotSpareBin:
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """

    def __init__(self):
        self.browser = Selenium()
        self.http = HTTP()
        self.tables = Tables()

    def open_robot_order_websoite(self):
        self.browser.open_available_browser('https://robotsparebinindustries.com')

    def download_robot_order_file(self):
        order_file_path = os.path.join(os.getcwd(), 'output/orders.csv')
        self.http.download(url=' https://robotsparebinindustries.com/orders.csv', target_file=order_file_path, overwrite=True)

    def read_orders_file(self):
        order_file_path = os.path.join(os.getcwd(), 'output/orders.csv')
        orders_data = self.tables.read_table_from_csv(path=order_file_path)
        return orders_data

    def fill_robot_form(self,row):
        self.browser.wait_until_element_is_visible('//a[text()="Order your robot!"]',timeout=10)
        self.browser.click_element('//a[text()="Order your robot!"]')
        self.browser.wait_until_element_is_visible('//button[@class="btn btn-dark"][text()="OK"]')
        self.browser.click_element('//button[@class="btn btn-dark"][text()="OK"]')
        ...






orders = Order_robots_from_RobotSpareBin()
orders.open_robot_order_websoite()
orders.download_robot_order_file()
robot_data = orders.read_orders_file()
for row in robot_data:
    orders.fill_robot_form(row)


