"""There are methods, which edits records in the database"""

import re

from flask_sqlalchemy import SQLAlchemy
import requests

from helpers.color_terminal import BColors


def add_plants(all_names: list, db: SQLAlchemy, table_name: SQLAlchemy.Model) -> None:
    """Inserts list of plants names to the db

    :param all_names: list, all names for insertion in the db
    :param db: SQLAlchemy, db, where to store plants
    :param table_name: SQLAlchemy.Model, name of a table in db, where to insert plants
    """

    for name in all_names:
        if not is_in_db(name):
            new_plant = table_name(
                latin_name=name,
                is_ok=True,
                source="https://www.aspca.org/pet-care/animal-poison-control/cats-plant-list",
                image_url=get_image_url(name),
            )
            db.session.add(new_plant)
            db.session.commit()
    print("All plants added.")


def is_in_db(name: str, table_name: SQLAlchemy.Model) -> bool:
    """Checks wheter a name of a plant is already in the database

    :param name: str, name of a plant
    :param table_name: SQLAlchemy.Model, name of a table in db
    :return: bool, True if a plant is already in the db
    """

    if table_name.query.filter(table_name.latin_name == name).first():
        print(f"{BColors.WARNING}Error --- {name} --- is already in the db.{BColors.ENDC}")
        return True
    print(f"{BColors.OKBLUE}Success --- {name} --- added to the database.{BColors.ENDC}")
    return False


def get_image_url(name: str) -> str:
    """searches for the image url of the given plant

    :param name: str, name of plant to be searched
    :return: url: str, a plant image url on wikipedia.org
    """

    # Search by full name
    response = requests.get(
        f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={name}"
    ).text

    # Get URL from given json response
    url = str(re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', response))
    url = url.replace("['", "")
    url = url.replace("']", "")

    # If no image found try to find using only first word from name
    if url == "[]":
        n_name = name.split(" ")[0]
        response = requests.get(
            f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&"
            f"format=json&piprop=original&titles={n_name}"
        ).text

        # Get URL from given json response
        url = str(re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', response))
        url = url.replace("['", "")
        url = url.replace("']", "")

    # If no image found try to find using only first word from name and adding _(plant)
    if url == "[]":
        n_name = name.split(" ")[0]
        response = requests.get(
            f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&"
            f"format=json&piprop=original&titles={n_name}_(plant)"
        ).text
        # Get URL from given json response
        url = str(re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', response))
        url = url.replace("['", "")
        url = url.replace("']", "")

    return url


def find_plants_with_wrong_information(table_name: SQLAlchemy.Model) -> None:
    """checks each plant in the db and finds those, which has no image url or possibly wrong names"""

    # Load up all names from the db
    # all_names = [name.latin_name for name in DogPlant.query.all()]

    all_names = [name.latin_name for name in table_name.query.filter(table_name.image_url == "[]").all()]

    for name in all_names:
        print(name)

    # for name in all_names:
    #     url = get_image_url(name)

    # If is url string containing [], prints his name
    # if url == '[]':
    #     print(name)
