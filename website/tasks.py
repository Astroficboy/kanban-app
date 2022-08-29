from flask import flash, Blueprint, request, render_template
from flask_login import login_required, current_user
from .models import User, Task, Task_list, Task_status
from . import db

tasks = Blueprint('tasks', __name__)

@tasks.route('/myboard', methods=['GET', 'POST', 'PUT', 'DELETE'])
def list_name():
    if request.method == 'POST':
        list_name = request.form.get('listName')
        note_heading = request.form.get('noteHeading')
        description = request.form.get('note') 
        date = request.form.get('date')
        if len(list_name) < 1:
            flash('List name too short. Must be atleast 2 letters.', category='error')
        else:
            new_list = Task(list_name=list_name, note_heading=note_heading, description=description, date=date, user_id=current_user.id)
            db.session.add(new_list)
            db.session.commit()
            flash('List added.', category='success')
    return render_template("lists.html", user=current_user)
