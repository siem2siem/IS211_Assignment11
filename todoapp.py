#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS211 Assignment11 - todoapp.py - Tested in Python 3.6.3 :: Anaconda, Inc."""

from flask import Flask, render_template, request, redirect
import pickle, re

app = Flask(__name__)
todoapp = []
status = ""
emailvalidate = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class Task:
    def __init__(self, task, email, priority):
        self.task = task
        self.email = email
        self.priority = priority

@app.route('/')
def index():
    return render_template('index.html', todoapp=todoapp, status=status)

@app.route('/submit', methods=['POST'])
def submit():
    global status
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']

    if task == "":
        status = "Please enter a task.  Task cannot be blank."
        return redirect("/")
    else:
        status = ""
    if not re.search(emailvalidate, email):
        status = "Please enter a valid email address.  Example: abc@def.com"
        return redirect("/")
    else:
        status = ""

    if priority != "High" and priority != "Medium" and priority != "Low":
        status = "You must select a priority from the drop down menu.  Select Low, Medium or High."
        return redirect("/")
    else:
        status = ""
    mytask = Task(task, email, priority)
    todoapp.append(mytask)
    return redirect("/")

@app.route('/clear', methods=['POST'])
def clear():
    del todoapp[:]
    return redirect("/")

@app.route('/delete', methods=['POST'])
def delete():
    delete_index = int(request.form['index'])
    del todoapp[delete_index]
    return redirect("/")

@app.route('/save', methods=['POST'])
def save():
    pickle.dump(todoapp, open('ToDoList.txt', 'wb'))
    return redirect("/")
	
if __name__ == '__main__':
    app.run()