
from suds.client import Client
from suds import WebFault


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self,username,password):
        client = Client("http://localhost/mantisbt-1.2.20/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username,password)
            return True
        except WebFault:
            return False


    def get_soap_project_list(self,username,password):
        client = Client("http://localhost/mantisbt-1.2.20/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        soap_list = []
        try:
            projects = client.service.mc_projects_get_user_accessible(username, password)
            for p in projects:
                soap_list.append(p.name)
            #print("list list list list list")
            return soap_list
        except WebFault:
            #print("WebFault WebFault WebFault WebFault WebFault")
            return False
