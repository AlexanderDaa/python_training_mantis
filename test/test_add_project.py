
from model.project import Project

def test_add_project(app):
    #app.projects.open_projects_page()
    #print("project page opened")
    app.projects.create_poject(Project(name="1qwer"))

