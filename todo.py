from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/todos')
def showTodos():
    return 'This page shows all TODOs'

@app.route('/todo/add')
def addTodo():
    return 'This page lets me add a TODO'

@app.route('/todo/<int:todo_id>/edit')
def editTodo(todo_id):
    return 'This page lets me edit a TODO'

@app.route('/todo/<int:todo_id>/delete')
def deleteTodo(todo_id):
    return 'This page lets me delete a TODO'

@app.route('/todo/completed')
def showCompleted():
    return 'This page shows all completed TODOs'

if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)