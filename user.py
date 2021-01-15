from flask_login import UserMixin, LoginManager
login_manager = LoginManager()


class User(UserMixin):
    def __init__(self,fname, sname, surname, email, password):
        self.fname=fname
        self.sname=sname
        self.surname=surname
        self.password = password
        self.email = email
        self.is_active = True
        self.is_admin = False
        self.is_user_authenticated = True

    def get_id(self):
        return self.email
    
    def is_authenticated(self):
        return self.is_user_authenticated

    @property
    def is_active(self):
        return True

