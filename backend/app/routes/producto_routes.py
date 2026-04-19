from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.producto_controller import ProductoController
from app.decorators.rol_access import rol_access

producto_bp = Blueprint("productos", __name__, url_prefix="/productos")



@producto_bp.route("/", methods=["GET"])
@jwt_required()
def get_all():
    return ProductoController.get_all()


@producto_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_one(id):
    return ProductoController.get_by_id(id)



@producto_bp.route("/", methods=["POST"])
@rol_access("admin")
def create():
    return ProductoController.create()


@producto_bp.route("/<int:id>", methods=["PUT"])
@rol_access("admin")
def update(id):
    return ProductoController.update(id)


@producto_bp.route("/<int:id>", methods=["DELETE"])
@rol_access("admin")
def delete(id):
    return ProductoController.delete(id)