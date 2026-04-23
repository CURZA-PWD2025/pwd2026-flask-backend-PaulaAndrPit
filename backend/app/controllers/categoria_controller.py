from abc import abstractmethod
from typing import Literal

from sqlalchemy.exc import IntegrityError
#from app.models.producto import Producto--es necesario importarlo o ya basta con que este relacionado??
from app.models.categoria import Categoria
from app.models import db
from flask import Response, jsonify
from app.controllers import Controller

class CategoriaController (Controller):
    
    @staticmethod
    def get_all() -> tuple[Response, int]:
        categorias_list = db.session.execute(db.select(Categoria).order_by(db.desc(Categoria.id))).scalars().all()
        if len(categorias_list) > 0:
            categorias_to_dict = [categoria.to_dict() for categoria in categorias_list ]
            return jsonify(categorias_to_dict, 200), 200 
        return jsonify({"message": 'categorias no encontradas'}, 404), 404
    

    @staticmethod
    def show(id)->tuple[Response, int]:
        categoria = db.session.get(Categoria, id)
        if categoria:
            return jsonify(categoria.to_dict(),200), 200
        return jsonify({"message": 'categoria no encontrada'}, 404), 404
    
    @staticmethod
    def create(request) -> tuple[Response, int]:
        nombre:str = request.get[('nombre')]
        descripcion = request[('descripcion')]
        error :str | None = None
        if nombre is None:
            error = jsonify({'message': 'El nombre es requerido'}), 422
        if descripcion is None:
            error = jsonify({'message': 'La descripción es requerida'}), 422
            
        if error is None:
            try:
                categoria = Categoria(nombre=nombre, descripcion=descripcion)
                db.session.add(categoria)
                db.session.commit()
                return jsonify({'message': "categoria creada con exito"}, 201), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': "Categoria ya registrada"}, 409), 409
        return error
        
        
    @staticmethod
    def update(request, id) -> tuple[Response, int]:
        nombre: str = request.get('nombre')
        descripcion: str = request.get('descripcion')

        if nombre is None:
            return jsonify({'message': 'El nombre es requerido'}), 422
        if descripcion is None:
            return jsonify({'message': 'La descripción es requerida'}), 422

        categoria = db.session.get(Categoria, id)
        if categoria is None:
            return jsonify({'message': 'Categoria no encontrada'}), 404

        try:
            categoria.nombre = nombre
            categoria.descripcion = descripcion
            db.session.commit()
            return jsonify({'message': 'Categoria modificada con exito'}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({'message': 'El nombre o la descripción ya existen'}), 409
        
        
    @staticmethod
    def destroy(id) -> tuple[Response, int]:
        categoria = db.session.get(Categoria, id)
        error = None
        if categoria and len(categoria.productos) == 0:
            db.session.delete(categoria)
            db.session.commit()
            return jsonify({'message':'la categoria fue eliminada con exito'}, 200), 200
        else:
            error = 'categoria no encontrada o tiene productos asociados'
        return jsonify({'message':error}, 409), 409