
def test_login(app):
    app.session.login("administrator","root")
    assert app.session.is_logged_in_as("administrator")

def test_login_logout(app):
    app.session.logout()
    print("logged out")
