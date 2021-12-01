from selenium import webdriver
from Fixture.session import SessionHelper


class Application:

    def __init__(self, browser, url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
# Edge doesn't work
        elif browser == "ie":
            self.wd = webdriver.Edge()
        else:
            raise ValueError("Unrecognized Browser %s" % browser)
#        self.wd.implicitly_wait(10)
        self.session = SessionHelper(self)
        self.url = url

    def open_home_page(self):
        wd = self.wd
        if wd.current_url != self.url:
            wd.get(self.url)

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def clear_fixture(self):
        self.wd.quit()
