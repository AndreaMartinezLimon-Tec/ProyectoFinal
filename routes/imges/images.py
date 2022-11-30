from flask import Blueprint, request,jsonify
from sqlalchemy import exc
from models import Juguete_Imagen
from app import db,bcrypt
from auth import tokenCheck
import base64
imageJuguete = Blueprint('imageJuguete',__name__,template_folder="templates")

def render_image(data):
    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic

@imageJuguete.route('/upload' , methods =['POST'])
@tokenCheck
def upload(usuario):
    juguete_id = None
    if 'juguete_id' in request.headers:
        juguete_id = request.headers['juguete_id']
    
    if not juguete_id:
        return jsonify({'mensaje':'Juguete no encontrado'})
    searchImage = Juguete_Imagen.query.filter_by(juguete_id = juguete_id).first()
    try:
        if searchImage:
            file = request.files['inputFile']
            data = file.read()
            render_file = render_image(data)
            searchImage.rendered_data=render_file
            searchImage.data=data
            db.session.commit()
            return jsonify({"message":"Imagen actualizada"})
        else:
            file = request.files['inputFile']
            data = file.read()
            render_file = render_image(data)
            newFile = Juguete_Imagen()
            newFile.type="Perfil"
            newFile.renderate_date=render_file
            newFile.juguete_id=juguete_id
            newFile.data=data
            db.session.add(newFile)
            db.session.commit()
            return jsonify({"message":"Imagen agregada"})
    except exc.SQLAlchemyError as e:
        print(e)
        return jsonify({"message":"Error"})