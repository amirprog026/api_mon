from flask_login import LoginManager, UserMixin
from .models import User

# Initialize Flask-Login
login_manager = LoginManager()

# This callback is used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.username == user_id)

# User class that inherits from UserMixin
class User(UserMixin, User):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.id=self.username
