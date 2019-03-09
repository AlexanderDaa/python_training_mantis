from selenium.webdriver.support.select import Select
from model.project import Project


class ProjectHelper:
    def __init__(self, app):
        self.app = app

    def create_project(self,project):
        wd = self.app.wd
        self.open_projects_page()
        self.open_project_addform()
        self.fill_project_form(project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        #wd.implicitly_wait(5)
        wd.find_element_by_xpath("//a[contains(text(),'Proceed')]")
        wd.find_element_by_xpath("//a[contains(text(),'Proceed')]").click()
        wd.find_elements_by_name("Create New Project")
        #для обновления списка проектов
        wd.find_element_by_css_selector("tr.row-category > td > a").click()
        wd.find_element_by_css_selector("tr.row-category > td > a").click()
        #print("project added")

    def open_projects_page(self):
        wd = self.app.wd
        if not(wd.current_url.endswith("/manage_proj_page.php") and len(wd.find_elements_by_name("Create New Project")) > 0):
            wd.get("http://localhost/mantisbt-1.2.20/mantisbt-1.2.20/manage_proj_page.php")

    def open_project_addform(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()

    def fill_project_form(self, project):
        wd = self.app.wd
        # -----------------------------
        p_status_list = ["development","release", "stable", "obsolete"]
        if project.status not in p_status_list:
            project.status = "development"
        wd.find_element_by_css_selector("select[name=\"status\"]").click()
        Select(wd.find_element_by_css_selector("select[name=\"status\"]")).select_by_visible_text(project.status)
        #index = p_status_list.index(project.status)+1
        #wd.find_element_by_xpath("//option[%s]" % str(index)).click()
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
            wd.find_element_by_name("view_state").click()
            Select(wd.find_element_by_name("view_state")).select_by_visible_text("private")
            #wd.find_element_by_css_selector("select[name=\"view_state\"] > option[value=\"50\"]").click()
        # -----------------------------
        if not project.description:
            project.description = "no description"
        wd.find_element_by_name("description").click()
        wd.find_element_by_name("description").clear()
        wd.find_element_by_name("description").send_keys(project.description)

    def get_project_list(self):
        wd = self.app.wd
        self.open_projects_page()
        group_list = []
        for element in wd.find_elements_by_css_selector("a[href*='_id=']"):
            text = element.text
            id = element.get_attribute("href")
            id = (id.split('_id=')[1:])
            id = ''.join(id)
            group_list.append(Project(id=id, name=text))
        group_list = group_list[1:]
        #print(group_list)
        return list(group_list)

    def get_project_name_list(self):
        list = self.get_project_list()
        name_list = []
        for p in list:
            name_list.append(p.name)
        #print(name_list)
        return name_list

    def del_project(self,project):
        self.select_project(project)
        self.click_del_confdel_project()

    def select_project(self,project):
        wd = self.app.wd
        wd.find_element_by_xpath("//a[contains(text(),'%s')]" % project.name).click()

    def click_del_confdel_project(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value='Update Project']")
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_elements_by_xpath("//*[contains(text(), 'Are you sure')]")
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()

