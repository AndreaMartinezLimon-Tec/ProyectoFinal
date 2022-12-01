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

class JugueteForm(FlaskForm):
    nombre = StringField('nombre', validators=[DataRequired()])
    costo = IntegerField('costo', validators=[DataRequired()])
    cantidad = StringField('cantidad', validators=[DataRequired()])
    proveedor_id = StringField('proveedor_id', validators=[DataRequired()])
    enviar = SubmitField('enviar')

class ImageForm(FlaskForm):
    type = StringField('type', validators=[DataRequired()])
    imagen = FileField('imagen', validators=[DataRequired()])
    juguete_id = SelectField('juguete_id',choices=[],coerce=int,validators=[DataRequired()])
    enviar = SubmitField('enviar')