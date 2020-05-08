from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class TodoLists(db.Model):
    __tablename__ = 'todo_lists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todos', backref='list', lazy=True)

    def __repr__(self):
        return f'<List: {self.id} {self.list_name}>'
    

class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todo_lists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo: {self.id} {self.description}>'


@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template(
        'index.html',
        lists=TodoLists.query.order_by('id').all(),
        active_list=TodoLists.query.get(list_id),
        todos=Todos.query.filter_by(list_id=list_id).order_by('id').all()
        )


@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.form.get('description')
        list_id = request.form.get('list-id')
        todo = Todos(
            description=description,
            list_id=list_id)
        db.session.add(todo)
        db.session.commit()
        list_id = todo.list_id
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return redirect(url_for('get_list_todos', list_id=list_id))


@app.route('/todos/<todo_id>/completed', methods=['POST'])
def set_completed(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todos.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('index'))


@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    error = False
    body = {}
    try:
        todo = Todos.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
        body['success'] = True
        body['id'] = todo_id
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route('/list/create', methods=['POST'])
def create_list():
    error = False
    body = {}
    try:
        name = request.form.get('list-name')
        # name = request.get_json()['name']
        todo_list = TodoLists(name=name)
        db.session.add(todo_list)
        db.session.commit()
        list_id = todo_list.id
        # body['name'] = todo_list.name
        # body['id'] = todo_list.id
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return redirect(url_for('get_list_todos', list_id=list_id))
        # return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)