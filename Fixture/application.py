from selenium import webdriver
from Fixture.session import SessionHelper
from Fixture.project import ProjectHelper
from Fixture.james import JamesHelper
from Fixture.mail import MailHelper
from Fixture.signup import SignupHelper
from Fixture.soap import SoapHelper


class Application:

    def __init__(self, browser, config):
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
        self.project = ProjectHelper(self)
        self.james = JamesHelper(self)
        self.config = config
        self.mail = MailHelper(self)
        self.signup = SignupHelper(self)
        self.url = config['web']['testUrl']
        self.soap = SoapHelper(self)

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
