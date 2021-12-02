from Model.project import Project
from selenium.webdriver.support.ui import Select
import random
import string
import re


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def create_project(self, project):
        wd = self.app.wd
        if project is not None:
            wd.get("http://localhost/mantisbt-1.2.20/manage_proj_create_page.php")
            wd.find_element_by_name("name").click()
            wd.find_element_by_name("name").clear()
            wd.find_element_by_name("name").send_keys(project.name)
            wd.find_element_by_name("status").click()
            wd.find_element_by_xpath("//option[@value='%s']" % project.status).click()
            wd.find_element_by_name("view_state").click()
            Select(wd.find_element_by_name("view_state")).select_by_value(project.view_state)
           # wd.find_element_by_xpath(
           #     "(.//*[normalize-space(text()) and normalize-space(.)='View Status'])[1]/following::option[2]").click()
            wd.find_element_by_name("description").click()
            wd.find_element_by_name("description").clear()
            wd.find_element_by_name("description").send_keys(project.description)
            wd.find_element_by_xpath("//input[@value='Add Project']").click()

    def generate_project_data(self):
        name = self.random_string(prefix="name", maxlen=100)
        description = self.random_string(prefix="", maxlen=100)
        status_values = ['10', '30', '50', '70']
        status = random.choice(status_values)
        view_st_values = ['10', '50']
        view_state = random.choice(view_st_values)
        project = Project(name=name, status=status, view_state=view_state, description=description)
        return project

    def random_string(self, prefix, maxlen):
        symbols = string.ascii_letters + string.digits + " " * 10
        s = "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])
        s = s.strip()
        s = re.sub('\s+', ' ', s)
        return prefix + s

    def get_project_from_hp(self):
        wd = self.app.wd
        wd.get("http://localhost/mantisbt-1.2.20/manage_proj_page.php")
        wd.refresh()
    #    if self.pr_cache is None:
        pr_cache = []
        i = 1
        for elements in wd.find_elements_by_xpath('/html/body/table[3]/tbody/tr'):
           # row = wd.find_element_by_xpath('/html/body/table[3]/tbody/tr[%s]' % str(i))
           if i >= 3:
               cells = elements.find_elements_by_tag_name("td")
               name = cells[0].text
               status = cells[1].text
               view_state = cells[3].text
               description = cells[4].text
               pr_cache.append(Project(name=name, status=status, view_state=view_state, description=description))
           i = i + 1
        return list(pr_cache)
