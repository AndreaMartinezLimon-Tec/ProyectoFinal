from flask import Blueprint, request,Flask,url_for,render_template,redirect,jsonify
from sqlalchemy import exc
from models import Juguete_Imagen, Juguete
from app import db,bcrypt
from auth import tokenCheck
import base64
from forms import ImageForm
from app import session
imageJuguete = Blueprint('imageJuguete',__name__,template_folder="templates")

def render_image(data):
    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic

@imageJuguete.route("/juguetes/imagen/<int:id>", methods=["POST","GET"])
@tokenCheck
def upload(usuario,id):
    if usuario['admin']:
        if 'registered_on' in usuario:
            pop=""
            mensaje="Ingresar imagen"
            imageForm = ImageForm()
            imageForm.type.data = "Foto"
            elegido = id
            imageForm.juguete_id.choices = [(juguete.id,juguete.nombre) for juguete in Juguete.query.filter_by(id=elegido).all()]

            if request.method == "POST":
                if imageForm.validate_on_submit():
                    try:
                        elegido = imageForm.juguete_id.data
                        searchImage = Juguete_Imagen.query.filter_by(juguete_id=elegido).first()
                        if searchImage:
                            file = imageForm.imagen.data
                            data = file.read()
                            render_file = render_image(data)
                            searchImage.data = data
                            searchImage.renderate_date = render_file
                            db.session.commit()
                            pop = "Imagen actualizada"
                            return (render_template('juguete/añadirimagen.html',forma=imageForm,mensaje=mensaje,pop=pop))
                        else:
                            file = imageForm.imagen.data
                            data = file.read()
                            render_file = render_image(data)
                            newFile = Juguete_Imagen()
                            newFile.type = imageForm.type.data
                            newFile.renderate_date = render_file
                            newFile.juguete_id = imageForm.juguete_id.data
                            newFile.data=data
                            db.session.add(newFile)
                            db.session.commit()
                            pop="Imagen insertada"
                            return (render_template('juguete/añadirimagen.html',forma=imageForm,mensaje=mensaje,pop=pop))
                    except exc.SQLAlchemyError as e:
                        print(e)
                        pop = f'Error: {e}'
                        return render_template ('juguete/añadirimagen.html',forma=imageForm,mensaje=mensaje,pop=pop)
            return render_template ('juguete/añadirimagen.html',forma=imageForm,mensaje=mensaje,pop=pop)
        else:
            return jsonify({"mensaje":"Sesion erronea"})
    else:
        return jsonify({"mensaje": "Es necesario tener permisos de administrador"})