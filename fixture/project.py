from selenium.webdriver.support.select import Select
from model.project import Project
from fixture.session import SessionHelper



class ProjectHelper:
    def __init__(self, app):
        self.app = app


    def create_poject(self,project):
        wd = self.app.wd

        self.open_projects_page()
        self.open_project_addform()
        self.fill_project_form(project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()

        wd.implicitly_wait(5)
        wd.find_element_by_css_selector("td.login-info-left")
        print("project added")

    def open_projects_page(self):
        wd = self.app.wd
        if not(wd.current_url.endswith("/manage_proj_page.php") and len(wd.find_elements_by_value("Create New Project")) > 0):
            wd.get("http://localhost/mantisbt-1.2.20/mantisbt-1.2.20/manage_proj_page.php")

    def open_project_addform(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()

    def fill_project_form(self, project):
        wd = self.app.wd

        # -----------------------------
        p_status_list = ["development","release", "stable", "obsolete"]
        if project.status not in p_status_list:
            project.status = "stable"
        wd.find_element_by_css_selector("select[name=\"status\"]").click()
        Select(wd.find_element_by_name("status")).select_by_visible_text(project.status)
        index = p_status_list.index(project.status)+1
        wd.find_element_by_xpath("//option[%s]" % str(index)).click()
        #-----------------------------
        if not project.name:
            project.name = "qqq1"
        wd.find_element_by_name("name").click()
        wd.find_element_by_name("name").clear()
        wd.find_element_by_name("name").send_keys(project.name)
        # -----------------------------
        if not project.inherit_global:
            wd.find_element_by_css_selector("input[name=\"inherit_global\"]").click()
        # -----------------------------
        if project.view_state == "private":
            #wd.find_element_by_name("view_state").click()
            #Select(wd.find_element_by_name("view_state")).select_by_visible_text("private")
            wd.find_element_by_css_selector("select[name=\"view_state\"] > option[value=\"50\"]").click()
        # -----------------------------

        if not project.description:
            project.description = "no description"
        wd.find_element_by_name("description").click()
        wd.find_element_by_name("description").clear()
        wd.find_element_by_name("description").send_keys(project.description)



#-------------------------------------------------------------------------------------------------------------
    def return_to_groups_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("groups").click()

    def create(self, group):
        wd = self.app.wd
        self.open_groups_page()
        # init group creation
        wd.find_element_by_name("new").click()
        # fill group form
        self.fill_group_form(group)
        # submit group creation
        wd.find_element_by_name("submit").click()
        self.return_to_groups_page()
        self.group_cache = None

    def change_first_group(self, group):
        self.change_group_by_index(index=0, group=group)

    def change_group_by_index(self, index, group):
        wd = self.app.wd
        self.open_groups_page()
        # select some group
        wd.find_elements_by_name("selected[]")[index].click()
        # click "edit group"
        wd.find_element_by_name("edit").click()
        # fill group form
        self.fill_group_form(group)
        # update
        wd.find_element_by_name("update").click()
        self.return_to_groups_page()
        self.group_cache = None

    def fill_group_form(self, group):
        wd = self.app.wd
        #for x in group.__dict__:
        #    if not getattr(group, x):
        #        setattr(group, x, "")

        if not group.name:
            group.name=""
        wd.find_element_by_name("group_name").clear()
        wd.find_element_by_name("group_name").send_keys(group.name)
        if group.header:
            wd.find_element_by_name("group_header").clear()
            wd.find_element_by_name("group_header").send_keys(group.header)
        if group.footer:
            wd.find_element_by_name("group_footer").clear()
            wd.find_element_by_name("group_footer").send_keys(group.footer)

    def open_groups_page(self):
        wd = self.app.wd
        if not(wd.current_url.endswith("/group.php") and len(wd.find_elements_by_name("new")) > 0):
            wd.find_element_by_link_text("groups").click()

    def delete_first_group(self):
        self.delete_group_by_index(0)

    def delete_group_by_index(self, index):
        wd = self.app.wd
        self.open_groups_page()
        # select
        wd.find_elements_by_name("selected[]")[index].click()
        # delete
        wd.find_element_by_name("delete").click()
        self.return_to_groups_page()
        self.group_cache = None


    def change_group_by_id(self, id, group):
        wd = self.app.wd
        self.open_groups_page()
        # select some group
        self.select_group_by_id(id)
        # click "edit group"
        wd.find_element_by_name("edit").click()
        # fill group form
        self.fill_group_form(group)
        # update
        wd.find_element_by_name("update").click()
        self.return_to_groups_page()
        self.group_cache = None


    def delete_group_by_id(self, id):
        wd = self.app.wd
        self.open_groups_page()
        # select
        self.select_group_by_id(id)
        #wd.find_elements_by_name("selected[]")[index].click()
        # delete
        wd.find_element_by_name("delete").click()
        self.return_to_groups_page()
        self.group_cache = None


    def select_group_by_id(self,id):
        wd= self.app.wd
        wd.find_element_by_css_selector("input[value='%s']" % id).click()

    def count(self):
        wd = self.app.wd
        self.open_groups_page()
        return len(wd.find_elements_by_name("selected[]"))

    group_cache = None

    def get_group_list(self):
        if self.group_cache is None:
            wd = self.app.wd
            self.open_groups_page()
            self.group_cache = []
            for element in wd.find_elements_by_css_selector("span.group"):
                text = element.text
                id = element.find_element_by_name("selected[]").get_attribute("value")
                self.group_cache.append(Group(name=text, id = id))
        return list(self.group_cache)



