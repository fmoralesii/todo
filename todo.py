from flask import Flask, render_template, redirect, request
app = Flask(__name__)

from create_db import Todo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Behind the scenes there are multiple threads being used somewhere
# in SQLAlchemy/SQLite3 and I keep getting exceptions if one thread
# tries to access the 'session' object created in this thread. 
# Being new to Flask/SQLAlchemy I'm unsure if this is the best
# practice, but passing the thread check as False, seems to work ok.
engine = create_engine('sqlite:///todos.db?check_same_thread=False')
Session = sessionmaker(bind = engine)
session = Session()

# NOTE: Functions by default to allow GET, explicit naming only
# required when we want to implement more verbs than that.

# Show only TODOs not completed
@app.route('/')
@app.route('/todos')
def showTodos():
    todos = session.query(Todo).filter_by(isCompleted = 0).all()

    if not todos:
        return render_template('todo.html', todos = None)
    else:
        return render_template('todo.html', todos = todos)

# Add a new TODO
@app.route('/todo/add', methods = ['GET', 'POST'])
def addTodo():
    if request.method == 'GET':
        return render_template('addTodo.html')
    else:
        if request.form['todo']:
            todo = Todo()
            todo.name = request.form['todo']
            todo.isCompleted = False
            session.add(todo)
            session.commit()
            return redirect('/todos')
        else:
            # We should use Flask flash to show an error here
            return redirect('/todos')

# Edit a TODO
@app.route('/todo/<int:todo_id>/edit', methods = ['GET', 'POST'])
def editTodo(todo_id):
    todo = session.query(Todo).filter_by(id = todo_id).one()

    if request.method == 'GET':
        return render_template('editTodo.html', todo = todo)
    else:
        if request.form['todo']:
            todo.name = request.form['todo']
            session.add(todo)
            session.commit()
            return redirect('/todos')
        else:
            return redirect('/todos')


# Delete a TODO
@app.route('/todo/<int:todo_id>/delete', methods = ['GET', 'POST'])
def deleteTodo(todo_id):
    todo = session.query(Todo).filter_by(id = todo_id).one()
    
    if request.method == 'GET':
        return render_template('deleteTodo.html', todo = todo)
    else:
        session.delete(todo)
        session.commit()
        return redirect('/todos')

# Mark TODO as complete, then redirect to 'showTodos'
@app.route('/todo/<int:todo_id>/complete')
def completeTodo(todo_id):
    todo = session.query(Todo).filter_by(id = todo_id).one()
    todo.isCompleted = True
    session.add(todo)
    session.commit()
    return redirect('/todos')

# Show all completed TODOs
@app.route('/todo/completed')
def showCompleted():
    todos = session.query(Todo).filter_by(isCompleted = 1).all()
    if not todos:
        return render_template('completed.html', completed_todos = None)
    else:
        return render_template('completed.html', completed_todos = todos)

# "Run" our app using Flask's built in dev web server, listening
# on localhost port 5000
if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)