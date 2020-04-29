from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///todoapp_development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Person ID: {self.id}, Name: {self.name}>'

db.create_all()

# @app.route('/')
# def index():
#     person = Users.query.first()
#     return f'Hello, {person.name}!'


if __name__ == '__main__':
    app.run(debug=True)