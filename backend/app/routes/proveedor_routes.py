from flask import Blueprint
from app.controllers.proveedor_controller import ProveedorController
from app.decorators.rol_access import rol_access

proveedor_bp = Blueprint("proveedores", __name__, url_prefix="/proveedores")


@proveedor_bp.route("/", methods=["GET"])
@rol_access("admin")
def get_all():
    return ProveedorController.get_all()


@proveedor_bp.route("/<int:id>", methods=["GET"])
@rol_access("admin")
def get_one(id):
    return ProveedorController.get_by_id(id)


@proveedor_bp.route("/", methods=["POST"])
@rol_access("admin")
def create():
    return ProveedorController.create()


@proveedor_bp.route("/<int:id>", methods=["PUT"])
@rol_access("admin")
def update(id):
    return ProveedorController.update(id)


@proveedor_bp.route("/<int:id>", methods=["DELETE"])
@rol_access("admin")
def delete(id):
    return ProveedorController.delete(id)