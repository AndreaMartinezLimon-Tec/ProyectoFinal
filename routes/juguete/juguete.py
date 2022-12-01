from flask import Blueprint, request, Flask, request, url_for, render_template, redirect, jsonify, make_response
from sqlalchemy import exc
from models import Proveedor,Juguete,Juguete_Imagen
from app import db, bcrypt
from auth import tokenCheck
from forms import JugueteForm
import pdfkit
from fpdf import FPDF
config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
appjuguete = Blueprint('appjuguete',__name__,template_folder="template")

@appjuguete.route('/agregarjuguetes', methods=['POST','GET'])
@tokenCheck
def registro(usuario):
    mensaje = "Registro de juguetes"
    jugueteForma = JugueteForm()
    if request.method == "POST":
        if jugueteForma.validate_on_submit():
            juguete = {"nombre":jugueteForma.nombre.data, "costo":jugueteForma.costo.data,"cantidad": jugueteForma.cantidad.data,"proveedor_id": jugueteForma.proveedor_id.data}
            jugueteExist = Juguete.query.filter_by(nombre=juguete['nombre']).first()
            proveedorExist= Proveedor.query.filter_by(id=juguete['proveedor_id']).first()
            if not jugueteExist:
                if proveedorExist:
                    agregarj = Juguete(nombre=juguete['nombre'], costo=juguete['costo'], cantidad=juguete['cantidad'],proveedor_id=juguete['proveedor_id'])
                    try:
                        db.session.add(agregarj)
                        db.session.commit()
                        mensaje = "Juguete agregado"
                    except exc.SQLAlchemyError as e:
                        mensaje = print(e)
                else:
                    mensaje= "El proveedor no existe"
            else:
                mensaje="El juguete ya existe"
            return render_template('juguete/agregarjuguete.html', forma=jugueteForma, mensaje=mensaje)
    return render_template('juguete/agregarjuguete.html', forma=jugueteForma, mensaje=mensaje)

@appjuguete.route('/juguetes', methods=["GET"])
@tokenCheck
def getJuguete(usuario):
    output=[]
    juguetes = Juguete.query.all()
    return render_template('juguete/juguete.html', juguetes=juguetes)


@appjuguete.route('/juguetes/editar/<int:id>', methods=['GET', 'POST'])
@tokenCheck
def editarjuguete(usuario, id):
    mensaje = "Editar juguete"
    if usuario['admin']:
        juguete = Juguete.query.get_or_404(id)
        jugueteForma = JugueteForm(obj=juguete)
        if request.method == "POST":
            if jugueteForma.validate_on_submit():
                jugueteForma.populate_obj(juguete)
                db.session.commit()
                return redirect(url_for('appjuguete.getJuguete'))
        return render_template('juguete/editarjuguete.html', forma=jugueteForma,mensaje=mensaje)
    else:
        return jsonify({"mensaje": "Es necesario tener permisos de administrador"})

@appjuguete.route('/juguetes/eliminar/<int:id>', methods=['GET', 'POST'])
@tokenCheck
def eliminarjuguete(usuario, id):
    if usuario['admin']:
        juguete = Juguete.query.get_or_404(id)
        db.session.delete(juguete)
        db.session.commit()
        return redirect(url_for('appjuguete.getJuguete'))
    return jsonify({"mensaje": "Es necesario tener permisos de administrador"})

@appjuguete.route('/juguetes/detalle/<int:id>', methods=['GET', 'POST'])
@tokenCheck
def usuariodown(usuario, id):
    if 'admin' in usuario:
        juguete = Juguete.query.get_or_404(id)
        searchImage = Juguete_Imagen.query.filter_by(juguete_id=id).first()
        
        imag = searchImage.renderate_date
        data = searchImage.data
        imagen = data
        
        rendered = render_template('juguete/detallejuguete.html', juguete=juguete, imagen=imag, id=juguete.id)
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(40,10,f'Nombre: {juguete.nombre}')
        pdf.cell(40,10,txt=f'Costo: {juguete.costo.__str__()}')
        #pdf.image(imagen, 30, 30, w = 70, h = 40, type = 'jpg')
        pdf.output("archi.pdf")
        
        response = make_response(pdf.output(dest='s'))
        #response = make_response(pdf)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'inline; filename=output.pdf'
        return response
    return jsonify({"mensaje": "no encontrado"})