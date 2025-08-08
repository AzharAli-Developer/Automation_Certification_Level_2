from RPA.HTTP import HTTP
from web_elements import Web_Elements


class Browser:
    def __init__(self, browser):
        self.browser = browser
        self.http = HTTP()

        #open website
        self.open = Web_Elements(self.browser, 'https://robotsparebinindustries.com')
        self.order = Web_Elements(self.browser, '//a[text()="Order your robot!"]')

        #open order website
        self.website = Web_Elements(self.http, 'https://robotsparebinindustries.com/orders.csv')

        # receipt_pdf
        self.receipt = Web_Elements(self.browser, '//div[@id="receipt"]')

        # robot_screenshot
        self.robot_preview = Web_Elements(self.browser, '//div[@id="robot-preview-image"]')

class Form:
    def __init__(self, browser, row):
        self.browser = browser
        self.row = row

        # fill_robot_form
        self.ok = Web_Elements(self.browser, '//button[@class="btn btn-dark"][text()="OK"]')
        self.head = Web_Elements(self.browser, '//select[@id="head"]', f"{self.row['Head']}")
        self.body = Web_Elements(self.browser, f'//label[@for="id-body-{self.row["Body"]}"]')
        self.legs = Web_Elements(self.browser, '//input[contains(@class ,"form-control")  and  @type="number"]', f"{self.row['Legs']}")
        self.address = Web_Elements(self.browser, '//input[@id="address" and @type="text" and @class="form-control"]', f"{self.row['Address']}")
        self.order = Web_Elements(self.browser, '//button[@id="order"]')
        self.another_order = Web_Elements(self.browser, '//button[@id="order-another"]')