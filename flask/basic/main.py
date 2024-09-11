from flask import Flask, redirect, url_for, render_template, request, session, flash
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = "secretKey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route("/home")
def home():
    return "<h1>Home</h1>"

#display all people
@app.route("/people/show")
def show_people():
        all_people = people.query.all()
        return render_template("people.html", values = all_people)

#add a person
@app.route("/people/add", methods=["GET", "POST"])
def add_person():
        if request.method == "POST":
                name = request.form["name"]
                email = request.form["email"]
                
                new_person = people(name, email)
                db.session.add(new_person)
                db.session.commit()
                
                flash("Person added successfully!")
                return redirect(url_for("show_people"))
        
        return render_template("add_person.html")

db = SQLAlchemy(app)

class people(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    
    def __init__ (self, name, email):
        self.name = name
        self.email = email

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        #adding a person to the database after creation
        person = people("Juan", "juanCedros@gmail.com")
        db.session.add(person)
        db.session.commit()
        
    app.run(debug=True)
    