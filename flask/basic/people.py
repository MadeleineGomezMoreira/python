from flask import Blueprint, render_template, request, flash, redirect, url_for
from main import db, people

people_page = Blueprint("people_page", __name__, static_folder="static", template_folder="templates")

#display all people
@people_page.route("/people")
def show_people():
        all_people = people.query.all()
        return render_template("people.html", people = all_people)

#add a person
@people_page.route("/add", methods=["GET", "POST"])
def add_person():
        if request.method == "POST":
                name = request.form["name"]
                email = request.form["email"]
                
                new_person = people(name, email)
                db.session.add(new_person)
                db.session.commit()
                
                flash("Person added successfully!")
                return redirect(url_for("people_page.show_people"))
        
        return render_template("add_person.html")
