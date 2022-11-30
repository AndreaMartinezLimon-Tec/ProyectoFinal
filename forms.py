from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FileField, SelectField,IntegerField
from flask import Flask, render_template, redirect, url_for
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    #nombre = StringField('nombre', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    #telefono = StringField('telefono', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    #admin = BooleanField('admin')
    enviar = SubmitField('enviar')

class UserFormRegistro(FlaskForm):
    nombre = StringField('nombre', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    telefono = StringField('telefono', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    enviar = SubmitField('enviar')

class ProveedorForm(FlaskForm):
    nombre = StringField('nombre', validators=[DataRequired()])
    telefono = StringField('telefono', validators=[DataRequired()])
    marca = StringField('marca', validators=[DataRequired()])
    enviar = SubmitField('enviar')
    
class UserFormObtener(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    nombre = StringField('nombre', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    telefono = StringField('telefono', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    enviar = SubmitField('enviar')
