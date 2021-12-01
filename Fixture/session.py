
class SessionHelper:

    def __init__(self, app):
        self.app = app

    def login(self, login, pwd):
        wd = self.app.wd
        self.app.open_home_page()
        wd.find_element_by_name("username").clear()
        wd.find_element_by_name("username").send_keys(login)
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(pwd)
        wd.find_element_by_xpath("//input[@value='Login']").click()

    def ensure_login(self, login, pwd):
        wd = self.app.wd
        if self.is_logged_in():
            if self.is_logged_in_as(login):
                return
            else:
                self.logout()
        self.login(login, pwd)

    def logout(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Logout").click()

    def ensure_logout(self):
        wd = self.app.wd
        if self.is_logged_in():
            self.logout()

    def is_logged_in(self):
        wd = self.app.wd
        return len(wd.find_elements_by_link_text("Logout")) > 0

    def is_logged_in_as(self, login):
        wd = self.app.wd
        return self.get_logged_user() == login

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_css_selector("td.login-info-left span").text
