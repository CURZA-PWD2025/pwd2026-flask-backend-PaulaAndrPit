from app import create_app
from app.models import db
from app.models.rol import Rol
from app.models.user import User
from app.models.categoria import Categoria
from app.models.proveedor import Proveedor
from app.models.producto import Producto

app = create_app()

def get_or_create(model, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        db.session.add(instance)
    return instance

with app.app_context():
    db.create_all()
    rol_admin = get_or_create(Rol, nombre='admin')
    rol_op    = get_or_create(Rol, nombre='operador')
    db.session.commit()

    # Usuario admin
    admin = User.query.filter_by(email='admin@stock.com').first()

    if not admin:
        admin = User(
        nombre='admin',
        email='admin@stock.com',
        rol_id=rol_admin.id
    )
    db.session.add(admin)


    admin.generate_password('admin123')

    db.session.commit()

    # Categorías
    alm = get_or_create(Categoria, nombre='Almacén', descripcion='Productos secos')
    lim = get_or_create(Categoria, nombre='Limpieza', descripcion='Artículos de limpieza')
    db.session.commit()

    # Proveedor
    prov = Proveedor.query.filter_by(nombre='Distribuidora Norte').first()
    if not prov:
        prov = Proveedor(
            nombre='Distribuidora Norte',
            telefono='2994001234',
            email='norte@distribuidora.com'
        )
        db.session.add(prov)
        db.session.commit()

    # Productos
    prod1 = Producto.query.filter_by(nombre='Harina 000').first()
    if not prod1:
        db.session.add(Producto(
            nombre='Harina 000',
            descripcion='Harina de trigo 000',
            precio_costo=280,
            precio_venta=350,
            stock_actual=50,
            stock_minimo=10,
            categoria_id=alm.id,
            proveedor_id=prov.id
        ))

    prod2 = Producto.query.filter_by(nombre='Lavandina 1L').first()
    if not prod2:
        db.session.add(Producto(
            nombre='Lavandina 1L',
            descripcion='Lavandina de 1 litro',
            precio_costo=150,
            precio_venta=210,
            stock_actual=30,
            stock_minimo=5,
            categoria_id=lim.id,
            proveedor_id=prov.id
        ))

    db.session.commit()
    print("Seed completado sin duplicados.")