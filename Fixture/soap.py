from suds.client import Client
from suds import WebFault
import os.path
import jsonpickle


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
        client = Client("https://www.mantisbt.org/bugs/api/soap/mantisconnect.php?wsdl")
        username = self.app.config["webadmin"]["username"]
        password = self.app.config["webadmin"]["password"]
        #try:
        data = client.service.mc_projects_get_user_accessible(username, password)
        print(data)
            #file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data/projects.json")
            #with open(file, "w") as f:
             #   jsonpickle.set_encoder_options("json", indent=2)
              #  f.write(jsonpickle.encode(data))
        return data
        #except WebFault:
         #   return False

