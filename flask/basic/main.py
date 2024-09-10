from flask import Flask, redirect, url_for, render_template, request, session, flash
from people import people_page
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.register_blueprint(people_page, url_prefix="/people")
app.secret_key = "secretKey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route("/home")
def home():
    return "<h1>Home</h1>"

db = SQLAlchemy(app)

class people(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    
    def __init__ (self, name, email):
        self.name = name
        self.email = email


person = people(1, "Juan", "juanCedros@gmail.com")
db.session.add(person)
db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    