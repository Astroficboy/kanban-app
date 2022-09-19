from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Task, Task_list, Task_status
#import json
from datetime import datetime, timedelta
from . import db
#import pandas as pd
#import matplotlib.pyplot as plt


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    task_list = Task_list.query.filter_by(user_id = current_user.id).distinct(Task_list.name).group_by(Task_list.name)
    tasks = Task.query.filter_by(user_id = current_user.id)
    user = User.query.filter_by(id = current_user.id).first()
    tasks_by_lists = {}
    for t in tasks:
        l = t.task_list_id
        tasks = None
        # tasks = tasks_by_lists[l]
        if not l in tasks_by_lists.keys():
            tasks = []
            tasks_by_lists[l] = tasks
        else:
            tasks = tasks_by_lists[l]
        tasks.append(t)
    
    return(render_template('lists.html', task_list=task_list, user=user, tasks_by_lists=tasks_by_lists))


@views.route('/create_list', methods=['GET', 'POST'])
def create_list():
    user = User.query.filter_by(id = current_user.id).first()
    list_name = request.form.get('listName')
    update_task_list = Task_list(name=list_name, user_id = current_user.id)
    if list_name is not None:
        db.session.add(update_task_list)    
        db.session.commit()
    if request.method == 'POST':
        flash('New list added.', category='success')
        return((redirect(url_for('views.home'))))
    return(render_template('create_list.html', user=user))
    

@views.route('/create_task', methods=['GET', 'POST'])
def create_task():
    user = User.query.filter_by(id = current_user.id).first()
    tasks_title = request.form.get('taskName')
    description = request.form.get('description')
    list_id = request.args.get('list_id')
    status = request.form.get('status')
    __status__= Task_status.Not_defined
    if request.method == 'POST':
        for s in Task_status:
            if s.name==status:
                __status__=status
        if description is None:
            description = None
        update_task = Task(task_list_id=list_id, user_id=current_user.id, title=tasks_title, 
        description=description, status=__status__, end_date=datetime.now().date()+timedelta(2), 
        completed_on_date=datetime.now().date()+timedelta(2))
        if tasks_title is not None:
            db.session.add(update_task)    
            db.session.commit()
            flash('New task added.', category='success')
        return((redirect(url_for('views.home'))))
    return(render_template('create_task.html', user=user, list_id=list_id))


@views.route('/delete_list', methods=['POST', 'GET'])
def delete_list():
    user = User.query.filter_by(id = current_user.id).first()
    list_id = request.args.get('list_id')
    Task_list.query.filter_by(id=list_id).delete()
    Task.query.filter_by(id=list_id).delete()
    db.session.commit()
    if request.method == 'POST':
        flash('List deleted.', category='success')
        return((redirect(url_for('views.home'))))
    return(render_template('delete_list.html', user=user))

    
@views.route('/delete_task', methods=['POST', 'GET'])
def delete_task():
    user = User.query.filter_by(id = current_user.id).first()
    task_id = request.args.get('task_id')
    Task.query.filter_by(id=task_id).delete()
    db.session.commit()
    if request.method == 'POST':
        flash('Task deleted.', category='success')
        return((redirect(url_for('views.home'))))
    return(render_template('delete_task.html', user=user))

@views.route('/edit_task', methods=['POST', 'GET'])
def change_status():
    user = User.query.filter_by(id = current_user.id).first()
    lists = Task_list.query.filter_by(user_id = current_user.id)
    task_id = request.args.get('task_id')
    changed_status = request.form.get('status')
    changed_list = request.form.get('changed_list')
    changed_list_id = 0
    for list_name in lists:
        if list_name.name == changed_list:
            changed_list_id = list_name.id
    get_task = Task.query.filter_by(id = task_id)
    get_task.update(dict(status = changed_status, task_list_id = changed_list_id))
    if changed_status == "DONE":
        get_task.update(dict(status = changed_status, task_list_id = changed_list_id, completed_on_date=datetime.now().date()))
    #get_task.update(dict(task_list_id = task_list_id))
    db.session.commit()
    if request.method == 'POST':
        flash('Task updated.', category='success')
        return((redirect(url_for('views.home'))))
    return(render_template('edit_task.html', user=user, task_id=task_id, lists=lists))

@views.route('/summary', methods=['GET'])
def summary():
    user = User.query.filter_by(id = current_user.id).first()
    tasks = Task.query.filter_by(user_id = current_user.id)
    lists = Task_list.query.filter_by(user_id = current_user.id)
    completed_tasks = []
    lists_with_completed_tasks = []
    tasks_on_time = []
    for task in tasks:
        if task.status == "DONE":
            completed_tasks.append(task)
        if task.completed_on_date !="NULL" and task.end_date > task.completed_on_date :
            tasks_on_time.append(task)
    for task in tasks:
        for list in lists:
            if task.task_list_id == list.id:
                lists_with_completed_tasks.append(list.name)
    return(render_template('summary.html', user=user, tasks = completed_tasks, tasks_on_time=tasks_on_time, lists = lists, lists_with_completed_tasks=lists_with_completed_tasks))