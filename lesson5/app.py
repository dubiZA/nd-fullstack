from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo: {self.id} {self.description}>'


db.create_all()

@app.route('/')
def index():
    return render_template('index.html', data=Todos.query.all())


@app.route('/todos/create', methods=['POST'])
def create_todo():
    description = request.get_json()['description']
    todo = Todos(description=description)
    db.session.add(todo)
    db.session.commit()

    return jsonify({
        'description': todo.description
    })


if __name__ == '__main__':
    app.run(debug=True)