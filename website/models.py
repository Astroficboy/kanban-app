from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Enum
import enum

class Task_status(enum.Enum):
    TODO = 1
    DOING = 2
    DONE = 3
    Not_defined = 4

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class Task_list(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    created_on = db.Column(db.DateTime(timezone=True), default=func.now())

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    task_list_id = db.Column(db.Integer, db.ForeignKey(Task_list.id))
    title = db.Column(db.String(200))
    description = db.Column(db.String(1000))
    status = db.Column(db.Enum(Task_status))
    start_date = db.Column(db.DateTime(timezone=True), default=func.now())
    end_date = db.Column(db.DateTime(timezone=True), default=func.now())




    

    
