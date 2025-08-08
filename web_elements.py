import os


class Web_Elements:
    def __init__(self, browser, locator, value = None):
        self.browser = browser
        self.locator = locator
        self.value = value

    def click(self):
        self.browser.click_element(self.locator)

    def website(self):
        self.browser.open_available_browser(self.locator, maximized=True)

    def click_button(self):
        self.browser.click_button(self.locator)

    def input_text(self):
        self.browser.input_text(self.locator, self.value)

    def wait_untill_visible(self, timeout=10):
        self.browser.wait_until_element_is_visible(self.locator, timeout=timeout)

    def order_rebot(self):
        self.browser.click_element(self.locator)

    def download(self, target_file):
        self.browser.download(self.locator, target_file = target_file, overwrite=True)

    def select_from_list(self):
        self.browser.select_from_list_by_value(self.locator, self.value)

    def page_contain_element(self):
        self.browser.does_page_contain_element(self.locator)

    def until_page_contains_element(self, timeout=10):
        self.browser.wait_until_page_contains_element(self.locator, timeout=timeout)

    def get_element_attribute(self):
        return self.browser.get_element_attribute(self.locator, 'innerHTML')

    def capture_screenshoot(self,filename):
        self.browser.capture_element_screenshot('//div[@id="robot-preview-image"]', filename=filename)

