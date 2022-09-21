# -*- encoding: utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email, DataRequired

## login and registration


class LoginForm(FlaskForm):
    username = TextField('Username', id='username_login', validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login', validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = TextField('Username', id='username_create', validators=[DataRequired()])
    nama = TextField('Nama', id='nama_create', validators=[DataRequired()])
    email = TextField('Email', id='email_create', validators=[DataRequired(), Email()])
    semester = TextField('Semester', id='semester_create', validators=[DataRequired()])
    kelas = TextField('Kelas', id='kelas_create', validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_create', validators=[DataRequired()])


class CreateMataKuliahForm(FlaskForm):
    matakuliah = TextField('MataKuliah', id='matakuliah_create', validators=[DataRequired()])
    namadosen = TextField('NamaDosen', id='namadosen_create', validators=[DataRequired()])
    semester = TextField('Semester', id='semester_create', validators=[DataRequired()])
