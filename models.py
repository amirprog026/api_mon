from peewee import *
from werkzeug.security import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
import datetime
db = SqliteDatabase('api_gateway.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(primary_key=True,unique=True)
    password_hash = CharField()
    is_active=BooleanField(default=True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class API(BaseModel):
    ID=AutoField(primary_key=True)
    user = ForeignKeyField(User, backref='apis')
    name = CharField()
    endpoint = CharField(unique=True)
    method = CharField()
    description = TextField(null=True)
    
    def to_dict(self):
        return model_to_dict(self)
    
class ACL(BaseModel):
    user=ForeignKeyField(User)
    API_ID=ForeignKeyField(API)
    created_at=DateTimeField(default=datetime.datetime.now())

class Doc(BaseModel):
    api=ForeignKeyField(API)
    html_doc=TextField(default="<p>put your doc here</p>")
    
