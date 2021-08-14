"""This file contains setup for the database"""

from typing import Callable

from flask_sqlalchemy import SQLAlchemy
from flask import Flask


class MySQLAlchemy(SQLAlchemy):
    """implemented only for Pycharm purposes, to prevent warnings"""

    Column: Callable
    String: Callable
    Integer: Callable
    Float: Callable
    Boolean: Callable
    Text: Callable


db = MySQLAlchemy()


class CatPlant(db.Model):
    """Definition of the database for suitable plants for cats"""

    __tablename__ = "cat"
    id = db.Column(db.Integer, primary_key=True)
    latin_name = db.Column(db.String(100), unique=True)
    is_ok = db.Column(db.Boolean())
    source = db.Column(db.String(300))
    image_url = db.Column(db.String(150))


class DogPlant(db.Model):
    """Definition of the database for suitable plants for dogs"""

    __tablename__ = "dog"
    id = db.Column(db.Integer, primary_key=True)
    latin_name = db.Column(db.String(100), unique=True)
    is_ok = db.Column(db.Boolean())
    source = db.Column(db.String(300))
    image_url = db.Column(db.String(150))


# Create db with all tables
# db.create_all()