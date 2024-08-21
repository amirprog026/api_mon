from flask_login import LoginManager, UserMixin
from .models import User

# Initialize Flask-Login
login_manager = LoginManager()

# This callback is used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == user_id)

# User class that inherits from UserMixin
class User(UserMixin, User):
    pass
