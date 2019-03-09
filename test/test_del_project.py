import string
from model.project import Project
import random


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def test_del_project(app):
    app.session.ensure_login(username=app.config['webadmin']["username"], password=app.config['webadmin']["password"])
    project_list = app.projects.get_project_list()
    if len(project_list) ==0:
        name = random_string("pr_", 10)
        while name in project_list:
            name = random_string("pr_", 10)
        #    print(name + " - name changed")
        app.projects.create_project(Project(name=name, description=random_string("", 10)))
        project_list = app.projects.get_project_list()
        #print(name+" - added for del")
    project_to_del = random.choice(project_list)
    app.projects.del_project(project_to_del)
    new_project_list = app.projects.get_project_list()
    assert len(project_list)-1 == len(new_project_list)
    #print(project_to_del)
    #print(len(project_list))
    #print(len(new_project_list))
    project_list.remove(project_to_del)
    #print(sorted(project_list, key=Project.id_or_max))
    #print(sorted(new_project_list, key=Project.id_or_max))
    assert sorted(project_list, key=Project.id_or_max) == sorted(new_project_list, key=Project.id_or_max)