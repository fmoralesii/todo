from flask import Flask, render_template
app = Flask(__name__)

# Show only TODOs not completed
@app.route('/')
@app.route('/todos')
def showTodos():
    #return 'This page shows all TODOs'
    dummyData = [
        {'name' : 'Pickup kids', 'completed' : False},
        {'name' : 'Walk dog', 'completed' : False}
    ]
    return render_template('todo.html', todos = dummyData)

@app.route('/todo/add')
def addTodo():
    return render_template('addTodo.html')

@app.route('/todo/<int:todo_id>/edit')
def editTodo(todo_id):
    return render_template('editTodo.html', todo_id = todo_id)

@app.route('/todo/<int:todo_id>/delete')
def deleteTodo(todo_id):
    return render_template('deleteTodo.html', todo_id = todo_id)

@app.route('/todo/completed')
def showCompleted():
    return render_template('completed.html', completed_todos = None)

if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)