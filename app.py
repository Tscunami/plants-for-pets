"""Main script to launch websites"""

from flask import Flask, render_template, request, redirect, url_for, flash

from helpers.setup_db import CatPlant, DogPlant, db
from static.data import SECRET_KEY


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/", methods=["GET", "POST"])
def home():
    """Route for Home Page"""

    return render_template("main_page.html")


@app.route("/animal/<a_name>/search/<name>", methods=["GET", "POST"])
def search(a_name: str, name: str):
    """Route for result page after search plant

    :param a_name: str, animal name
    :param name: str, plant name
    """

    animals = {
        "cat": CatPlant,
        "dog": DogPlant,
    }

    if a_name not in animals:
        return redirect(url_for("home"))

    all_names = [name.latin_name for name in animals[a_name].query.all()]
    error = None

    if animals[a_name].query.filter(animals[a_name].latin_name == name).first():
        plant = animals[a_name].query.filter(animals[a_name].latin_name == name).first()
        return render_template("animal.html", animal=a_name, plant=plant, names=all_names)

    flash("No results")
    return redirect(url_for("animal", name=a_name, error=error))


@app.route("/animal/<name>", methods=["GET", "POST"])
def animal(name: str):
    """Route for Home Page of each animal

    :param name: str, animal name
    """

    animals = {
        "cat": CatPlant,
        "dog": DogPlant,
    }

    if name not in animals:
        return redirect(url_for("home"))

    if request.method == "POST":
        plant_name = request.form["name-of-plant"]
        if plant_name:
            return redirect(url_for("search", a_name=name, name=plant_name))

    elif request.method == "GET":
        all_names = [plant_name.latin_name for plant_name in animals[name].query.all()]
        return render_template("animal.html", animal=name, names=all_names)


@app.route("/about")
def about():
    """Route for About Page"""

    return render_template("about.html")


@app.route("/contact")
def contact():
    """Route for Contact Page"""

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)

    # For checking if are all names valid
    # find_plants_with_wrong_information()

    # For adding new plants in the db
    # all_plants = find_all_plants()
    # add_plants(all_plants)
