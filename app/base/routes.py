# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask, flash, jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

import tensorflow as tf
from flask import abort
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
import pickle
import os
import json

from app import db, login_manager
from app.base import blueprint
from app.base.forms import CreateMataKuliahForm, LoginForm, CreateAccountForm
from app.base.models import MataKuliah, User, EdomModel


from app.base.util import verify_pass


@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/error-<error>')
def route_errors(error):
    return render_template('errors/{}.html'.format(error))

## Login & Registration


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('login/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template('login/login.html', form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/create_user', methods=['GET', 'POST'])
def create_user():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('login/register.html', msg='Username already registered', form=create_account_form)

        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('login/register.html', msg='Email already registered', form=create_account_form)

        # else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('login/register.html', msg='User created please <a href="/login">login</a>', form=create_account_form)

    else:
        return render_template('login/register.html', form=create_account_form)

# Data User


@blueprint.route('/DataUser')
def datauser():
    user = User.query.all()
    return render_template("DataUser.html", user=user)


@blueprint.route('/<int:id>/delete', methods=['GET', 'POST'])
def deleteuser(id):
    user = User.query.filter_by(id=id).first()
    if request.method == 'POST':
        if user:
            db.session.delete(user)
            db.session.commit()
            return redirect('/DataUser')
        abort(404)
     # return redirect('/')
    return render_template('delete.html')

# Data EDOM


@blueprint.route('/DataEdom')
def dataedom():
    edom = EdomModel.query.all()
    return render_template("DataEdom.html", edom=edom)

# Rekap


@blueprint.route('/Rekap')
def rekapedom():
    edom = EdomModel.query.all()

    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).all()
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).all()

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))

@blueprint.route('/Rekap01')
def rekapedom1():
    nama = 'David Bani Adam, S.H, M.H'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))

@blueprint.route('/Rekap02')
def rekapedom2():
    nama = 'Muhammad Fikri Hidayattullah, S.T., M.Kom.'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))

@blueprint.route('/Rekap03')
def rekapedom3():
    nama = 'Hendrawan Aprilia A, S.T.'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))

@blueprint.route('/Rekap04')
def rekapedom4():
    nama = 'Priyanto Tamami, S.Kom.'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))

@blueprint.route('/Rekap05')
def rekapedom5():
    nama = 'M. Nishom, M.Kom.'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))

@blueprint.route('/Rekap06')
def rekapedom6():
    nama = "Dwi Intan Af'idah, M.Kom."
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))

@blueprint.route('/Rekap07')
def rekapedom7():
    nama = 'Mirza Alim Mutasodirin, M.Kom'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))

@blueprint.route('/Rekap08')
def rekapedom8():
    nama = 'Ardi Susanto, S.Kom., M.Cs.'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))

@blueprint.route('/Rekap09')
def rekapedom9():
    nama = 'Riszki Wijayatun Pratiwi., M.CS.'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))


@blueprint.route('/Rekap10')
def rekapedom10():
    nama = 'Ary Herijanto, S.Kom, MMSi'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))


@blueprint.route('/Rekap11')
def rekapedom11():
    nama = 'Romi Muharyono, S.Ag.'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))

@blueprint.route('/Rekap12')
def rekapedom12():
    nama = 'Hepatika Zidny Ilmadina, S.Pd., M.Kom.'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))

@blueprint.route('/Rekap13')
def rekapedom13():
    nama = 'Sharfina Febbi Handayani, M.Kom.'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))

@blueprint.route('/Rekap14')
def rekapedom14():
    nama = 'Ginanjar Wiro Sasmito, M.Kom.'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))

@blueprint.route('/Rekap15')
def rekapedom15():
    nama = 'Taufiq Abidin, M.Kom.'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))


@blueprint.route('/Rekap16')
def rekapedom16():
    nama = 'Dega Surono Wibowo, S.T., M.Kom.'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))


@blueprint.route('/Rekap17')
def rekapedom17():
    nama = 'Dairoh, M.Sc.'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))


@blueprint.route('/Rekap18')
def rekapedom18():
    nama = 'Slamet Wiyono, S.Pd., M. Eng.'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))

@blueprint.route('/Rekap19')
def rekapedom19():
    nama = 'Muchammad Sofyan Firmansyah, S.S, M.A'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))


@blueprint.route('/Rekap20')
def rekapedom20():
    nama = 'Aris Setyawan, S.T'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))

@blueprint.route('/Rekap21')
def rekapedom21():
    nama = 'Rosid Mustofa, M.Kom'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)
    rekap_edom1 = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)
    edom_sentiment1 = []
    for total_sentiment1, _ in rekap_edom1:
        edom_sentiment1.append(total_sentiment)

    return render_template("Rekap.html", edom=edom, rekap_edom=json.dumps(edom_sentiment), rekap_edom1=json.dumps(edom_sentiment))



#Rekap Dosen
@blueprint.route('/RekapDosen')
def rekapdosen():
    nama = 'Taufiq Abidin, M.Kom.'
    edom = EdomModel.query.filter(EdomModel.nama == nama)
    rekap_edom = db.session.query(db.func.sum(EdomModel.amount), EdomModel.sentiment).group_by(
        EdomModel.sentiment).order_by(EdomModel.sentiment).filter(EdomModel.nama == nama)

    edom_sentiment = []
    for total_sentiment, _ in rekap_edom:
        edom_sentiment.append(total_sentiment)

    return render_template("RekapDosen.html", edom=edom, rekap_edom=json.dumps(edom_sentiment))


@blueprint.route('/<int:id>/deleteedom', methods=['GET', 'POST'])
def delete(id):
    edom = EdomModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if edom:
            db.session.delete(edom)
            db.session.commit()
            return redirect('/DataEdom')
        abort(404)
     # return redirect('/')
    return render_template('deleteedom.html')

# Data Mata Kuliah


@blueprint.route('/Maktul', methods=['POST', "GET"])
def maktul():
    if request.method == 'POST':
        matakuliah = request.form['matakuliah']
        dosenpengampu = request.form['dosenpengampu']
        semester = request.form['semester']
        mk = MataKuliah(
            matakuliah=matakuliah,
            namadosen=dosenpengampu,
            semester=semester
        )
        db.session.add(mk)
        db.session.commit()

    return render_template('Maktul.html')


app = Flask(__name__)
IMAGE_FOLDER = os.path.join('static', 'img_pool')
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

with open('app/base/tokenizer1.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)


def init():
    global model, graph
    graph = tf.Graph()


@blueprint.route('/sentiment_prediction', methods=['POST', "GET"])
def sent_anly_prediction():
    if request.method == 'POST':
        edom1 = EdomModel.query.all()
        text = request.form['review']
        amount = 1

        sentiment_classes = ['Baik', 'Cukup', 'Kurang', 'Sangat Baik']
        max_len = 50
        # Transforms text to a sequence of integers using a tokenizer object
        xt = tokenizer.texts_to_sequences([text])
        # Pad sequences to the same length
        xt = pad_sequences(xt, padding='post', maxlen=max_len)
        graph = tf.Graph()

        with graph.as_default():
            # load the pre-trained Keras model
            model = load_model('app/base/best_model.h5')
            yt = model.predict(xt).argmax(axis=1)
            probability = model.predict(xt)[0][0]
            sentiment = sentiment_classes[yt[0]]

            if sentiment == 'Kurang':
                img_filename = os.path.join(
                    app.config['UPLOAD_FOLDER'], 'merah.png')
            elif sentiment == 'Cukup':
                img_filename = os.path.join(
                    app.config['UPLOAD_FOLDER'], 'kuning.png')
            elif sentiment == 'Baik':
                img_filename = os.path.join(
                    app.config['UPLOAD_FOLDER'], 'hijau.png')
            else:
                img_filename = os.path.join(
                    app.config['UPLOAD_FOLDER'], 'biru.png')
        nim = request.form['nim']
        nama = request.form['nama']
        semester = request.form['semester']
        review = request.form['review']
        slug = nim + nama
        edom = EdomModel(
            nim=nim,
            nama=nama,
            semester=semester,
            review=review,
            sentiment=sentiment,
            probability=probability,
            amount=amount,
            slug=slug
        )
        user = EdomModel.query.filter_by(slug=slug).first()
        if user:
            return render_template('Analysis.html', msg='Maaf Anda Sudah Memberikan Review Kepada Dosen ini!')

        db.session.add(edom)
        db.session.commit()

    return render_template('Analysis.html', text=text, sentiment=sentiment, probability=probability, amount=amount, slug=slug, image=img_filename, edom1=edom1, msg='Evaluasi Berhasil Terkirim!')


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'


# Errors


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
