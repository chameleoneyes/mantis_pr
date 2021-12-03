from suds.client import Client
from suds import WebFault
from suds.sudsobject import asdict
import os.path
import jsonpickle
import xmltodict
from Model.project import Project




class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client("https://www.mantisbt.org/bugs/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def list_of_projects(self):
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        username = self.app.config["webadmin"]["username"]
        password = self.app.config["webadmin"]["password"]
        #try:
        data = client.service.mc_projects_get_user_accessible(username, password)
        return self.list_of_project_parser(data)

    def list_of_project_parser(self, data):
        list = []
        for item in data:
           i = Project(None, None, None, None)
           s = item[1]
           i.name = s
           s = str(item[2])
           l = s.split('\n')
           s = l[2]
           index_s = s.find('\"')
           index_e = s.rfind('\"', index_s + 1)
           index_s = index_s + 1
           s = s[index_s:index_e]
           i.status = s
           s = str(item[4])
           l = s.split('\n')
           s = l[2]
           index_s = s.find('\"')
           index_e = s.rfind('\"', index_s + 1)
           index_s = index_s + 1
           s = s[index_s:index_e]
           i.view_state = s
           s = str(item[7])
           i.description = s
           list.append(i)
        return list




