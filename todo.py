from flask import Flask, render_template, redirect, request, jsonify, flash
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

# NOTE: Functions by default allow GET, explicit naming only
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
        todo = Todo()
        todo.name = request.form['todo']
        todo.isCompleted = False

        session.add(todo)
        session.commit()
        flash(todo.name + ' added to TODO list')
        return redirect('/todos')


# Edit a TODO
@app.route('/todo/<int:todo_id>/edit', methods = ['GET', 'POST'])
def editTodo(todo_id):
    todo = session.query(Todo).filter_by(id = todo_id).one()

    if request.method == 'GET':
        return render_template('editTodo.html', todo = todo)
    else:
        todo.name = request.form['todo']

        session.add(todo)
        session.commit()
        flash('Successfully editied ' + todo.name + ' TODO')
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
        flash('Successfully deleted ' + todo.name + ' TODO')
        return redirect('/todos')

# Mark TODO as complete, then redirect to 'showTodos'
@app.route('/todo/<int:todo_id>/complete')
def completeTodo(todo_id):
    todo = session.query(Todo).filter_by(id = todo_id).one()

    todo.isCompleted = True
    session.add(todo)
    session.commit()
    flash(todo.name + ' marked as complete')
    return redirect('/todos')

# Show all completed TODOs
@app.route('/todo/completed')
def showCompleted():
    todos = session.query(Todo).filter_by(isCompleted = 1).all()

    if not todos:
        return render_template('completed.html', completed_todos = None)
    else:
        return render_template('completed.html', completed_todos = todos)

# API endpoints for JSON
@app.route('/todo/completed/JSON')
def showCompletedJSON():
    todos = session.query(Todo).filter_by(isCompleted = 1).all()

    return jsonify(TODOs = [todo.serialize for todo in todos])

@app.route('/todo/pending/JSON')
def showPendingJSON():
    todos = session.query(Todo).filter_by(isCompleted = 0).all()

    return jsonify(TODOs = [todo.serialize for todo in todos])

@app.route('/todo/<int:todo_id>/JSON')
def showTodoJSON(todo_id):
    try:
        # If we get a bad ID, we'll get an exception. In that case
        # catch it, and render empty JSON to the user
        todo = session.query(Todo).filter_by(id = todo_id).one()
    except:
        return jsonify(TODOs = [])
   
    return jsonify(TODOs = todo.serialize)

# "Run" our app using Flask's built in dev web server, listening
# on localhost port 5000
# NOTE: This is NOT for production use, see Flask docs for that
if __name__ == "__main__":
    app.secret_key = 'use_a_better_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)