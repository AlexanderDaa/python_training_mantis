
from model.project import Project
import random
import string


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def test_add_project(app):
    name_list = app.projects.get_project_name_list()
    name = random_string("pr_", 10)
    while name in name_list:
        name = random_string("pr_", 10)
        print(name +" - name changed")
    print(name_list)
    print(name)
    status = random.choice(["development","release", "stable", "obsolete"])
    view_state = random.choice(["public","private"])
    print(status)
    print(view_state)
    app.projects.create_project(Project(name=name, status=status, view_state=view_state, description=random_string("", 10)))
    new_name_list = app.projects.get_project_name_list()
    assert len(name_list)+1 == len(new_name_list)

