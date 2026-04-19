from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.categoria_controller import CategoriaController
from app.decorators.rol_access import rol_access

categoria_bp = Blueprint("categorias", __name__, url_prefix="/categorias")



@categoria_bp.route("/", methods=["GET"])
@jwt_required()
def get_all():
    return CategoriaController.get_all()



@categoria_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_one(id):
    return CategoriaController.get_by_id(id)



@categoria_bp.route("/", methods=["POST"])
@rol_access("admin")
def create():
    return CategoriaController.create()



@categoria_bp.route("/<int:id>", methods=["PUT"])
@rol_access("admin")
def update(id):
    return CategoriaController.update(id)



@categoria_bp.route("/<int:id>", methods=["DELETE"])
@rol_access("admin")
def delete(id):
    return CategoriaController.delete(id)