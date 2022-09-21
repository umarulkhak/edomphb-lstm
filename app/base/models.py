# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import LargeBinary, Column, Integer, String

from app import db, login_manager

from app.base.util import hash_pass


class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    nama = Column(String)
    email = Column(String, unique=True)
    semester = Column(String)
    kelas = Column(String)
    password = Column(LargeBinary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None

# Mata Kuliah Table


class MataKuliah(db.Model):

    __tablename__ = 'MataKuliah'

    id = Column(Integer, primary_key=True)
    matakuliah = Column(String, unique=True)
    namadosen = Column(String, unique=True)
    semester = Column(String, unique=True)


class EdomModel(db.Model):
    __tablename__ = "edom"

    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String())
    nama = db.Column(db.String())
    semester = db.Column(db.String())
    review = db.Column(db.String())
    sentiment = db.Column(db.String())
    probability = db.Column(db.String())
    amount = db.Column(db.Integer, nullable=False)
    slug = db.Column(db.String())

    def __init__(self, nim, nama, semester, review, sentiment, probability, amount, slug):
        self.nim = nim
        self.nama = nama
        self.semester = semester
        self.review = review
        self.sentiment = sentiment
        self.probability = probability
        self.amount = amount
        self.slug = slug

    def __repr__(self):
        return f"{self.nama}:{self.nama}"
