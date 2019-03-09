
import random
import string


def random_string(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def test_sign_up_new_account(app):
    username = random_string("user_",10)
    password = "test"
    email = username+"@localhost"
    app.james.ensure_user_exists(username, password)
    app.signup.new_user(username,email,password)
    #app.session.login(username,password)
    #assert app.session.is_logged_in_as(username )
    #app.session.logout()
    print(username+" - "+password)
    assert app.soap.can_login(username,password)