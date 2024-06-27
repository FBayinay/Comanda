from . import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column('id_rol', db.Integer, primary_key=True)
    name = db.Column('Nombre', db.String(50), nullable=False)

class Action(db.Model):
    __tablename__ = 'acciones'
    id = db.Column('id_accion', db.Integer, primary_key=True)
    name = db.Column('Nombre', db.String(50), nullable=False)

class Restaurant(db.Model):
    __tablename__ = 'restaurantes'
    id = db.Column('id_restaurante', db.Integer, primary_key=True)
    name = db.Column('Nombre', db.String(50), nullable=False)
    street = db.Column('Calle', db.String(100), nullable=False)
    number = db.Column('Numero', db.Integer, nullable=False)

class User(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column('id_usuario', db.Integer, primary_key=True)
    first_name = db.Column('Nombre', db.String(50), nullable=False)
    last_name = db.Column('Apellido', db.String(50), nullable=False)
    dni = db.Column('DNI', db.String(8), nullable=False, unique=True)
    email = db.Column('Email', db.String(100), nullable=False, unique=True)
    street = db.Column('Calle', db.String(80), nullable=False)
    number = db.Column('Numero', db.Integer, nullable=False)
    role_id = db.Column('Rol_ID', db.Integer, db.ForeignKey('roles.id_rol'))
    action_id = db.Column('id_accion', db.Integer, db.ForeignKey('acciones.id_accion'), nullable=False)
    restaurant_id = db.Column('id_restaurante', db.Integer, db.ForeignKey('restaurantes.id_restaurante'))

class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column('id_login', db.Integer, primary_key=True)
    user_id = db.Column('id_usuario', db.Integer, db.ForeignKey('usuarios.id_usuario'), unique=True)
    username = db.Column('username', db.String(50), unique=True, nullable=False)
    password_hash = db.Column('password_hash', db.String(100), nullable=False)
    
class Warehouse(db.Model):
    __tablename__ = 'almacenes'
    id = db.Column('id_almacenes', db.Integer, primary_key=True)
    name = db.Column('Nombre', db.String(50), nullable=False)
    restaurant_id = db.Column('id_restaurante', db.Integer, db.ForeignKey('restaurantes.id_restaurante'), unique=True)
    type = db.Column('Tipo', db.String(50), nullable=False)

class Product(db.Model):
    __tablename__ = 'productos'
    id = db.Column('id_producto', db.Integer, primary_key=True)
    name = db.Column('Nombre', db.String(50), nullable=False)

class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column('id_stock', db.Integer, primary_key=True)
    product_id = db.Column('id_producto', db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    warehouse_id = db.Column('id_almacen', db.Integer, db.ForeignKey('almacenes.id_almacenes'), nullable=False)
    quantity = db.Column('Cantidad', db.Integer, nullable=False)

class Movement(db.Model):
    __tablename__ = 'movimientos_alamcenes'
    id = db.Column('id_movimiento', db.Integer, primary_key=True)
    user_id = db.Column('UsuarioID', db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    origin_warehouse_id = db.Column('AlmacenOrigenID', db.Integer, db.ForeignKey('almacenes.id_almacenes'), nullable=False)
    destination_warehouse_id = db.Column('AlmacenDestinoID', db.Integer, db.ForeignKey('almacenes.id_almacenes'), nullable=False)
    product_id = db.Column('id_producto', db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    quantity = db.Column('Cantidad', db.Integer, nullable=False)
    date = db.Column('Fecha', db.DateTime, nullable=False, default=db.func.current_timestamp())

class Supplier(db.Model):
    __tablename__ = 'proveedores'
    id = db.Column('id_proveedor', db.Integer, primary_key=True)
    name = db.Column('Nombre', db.String(50), nullable=False)
    contact = db.Column('Contacto', db.String(20), nullable=False)

class Order(db.Model):
    __tablename__ = 'pedidos_alamcen_general'
    id = db.Column('id_pedido', db.Integer, primary_key=True)
    user_id = db.Column('id_usuario', db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    product_id = db.Column('id_producto', db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    supplier_id = db.Column('id_proveedor', db.Integer, db.ForeignKey('proveedores.id_proveedor'), nullable=False)
    quantity = db.Column('Cantidad', db.Integer, nullable=False)
    unit_price = db.Column('Precio_Unitario', db.Numeric(10, 2), nullable=False)
    total_price = db.Column('Precio_Total', db.Numeric(10, 2), nullable=False)
    date = db.Column('Fecha', db.DateTime, nullable=False, default=db.func.current_timestamp())

class Table(db.Model):
    __tablename__ = 'mesas'
    id = db.Column('id_mesa', db.Integer, primary_key=True)
    restaurant_id = db.Column('id_restaurante', db.Integer, db.ForeignKey('restaurantes.id_restaurante'), nullable=False)
    number = db.Column('Numero_mesa', db.Integer, nullable=False)
    capacity = db.Column('Capacidad', db.Integer, nullable=False)
    status = db.Column('Estado', db.String(20), nullable=False)

class MenuCategory(db.Model):
    __tablename__ = 'categorias_menu'
    id = db.Column('id_categoria', db.Integer, primary_key=True)
    category = db.Column('Categoria', db.String(50), nullable=False)
    description = db.Column('Descripcion', db.String(50), nullable=False)

class Menu(db.Model):
    __tablename__ = 'menus'
    id = db.Column('id_menu', db.Integer, primary_key=True)
    restaurant_id = db.Column('id_restaurante', db.Integer, db.ForeignKey('restaurantes.id_restaurante'), nullable=False)
    type = db.Column('Tipo', db.String(50), nullable=False)
    start_date = db.Column('FechaInicio', db.String(10), nullable=False)
    end_date = db.Column('FechaFin', db.String(10))

class MenuItem(db.Model):
    __tablename__ = 'items_menu'
    id = db.Column('id_items', db.Integer, primary_key=True)
    menu_id = db.Column('id_menu', db.Integer, db.ForeignKey('menus.id_menu'), nullable=False)
    category_id = db.Column('id_categoria', db.Integer, db.ForeignKey('categorias_menu.id_categoria'), nullable=False)
    name = db.Column('Nombre', db.String(100), nullable=False)
    description = db.Column('Descripcion', db.String(200))
    price = db.Column('Precio', db.Numeric(10, 2), nullable=False)

class OrderDetail(db.Model):
    __tablename__ = 'detalles_comanda'
    id = db.Column('id_detalles', db.Integer, primary_key=True)
    order_id = db.Column('id_comanda', db.Integer, db.ForeignKey('comanda.id_comanda'), nullable=False)
    menu_item_id = db.Column('id_item_menu', db.Integer, db.ForeignKey('items_menu.id_items'), nullable=False)
    menu_id = db.Column('id_menu', db.Integer, db.ForeignKey('menus.id_menu'), nullable=False)
    quantity = db.Column('Cantidad', db.Integer, nullable=False)
    total_price = db.Column('Precio_Total', db.Numeric(10, 2), nullable=False)

class Bill(db.Model):
    __tablename__ = 'recibo_cliente'
    id = db.Column('id_recibo', db.Integer, primary_key=True)
    order_id = db.Column('id_comanda', db.Integer, db.ForeignKey('comanda.id_comanda'), nullable=False)
    date = db.Column('Fecha', db.DateTime, nullable=False, default=db.func.current_timestamp())
    total = db.Column('Total', db.Numeric(10, 2), nullable=False)
    payment_status = db.Column('EstadoPago', db.String(50), nullable=False, default='Pendiente')
    order_details = db.Column('DetallesComanda', db.Text)

class Order(db.Model):
    __tablename__ = 'comanda'
    id = db.Column('id_comanda', db.Integer, primary_key=True)
    table_id = db.Column('id_mesa', db.Integer, db.ForeignKey('mesas.id_mesa'), nullable=False)
    user_id = db.Column('id_usuario', db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    start_date = db.Column('Fecha_Inicio', db.DateTime, nullable=False, default=db.func.current_timestamp())
    end_date = db.Column('Fecha_Fin', db.DateTime)
    status = db.Column('Estado', db.String(50), nullable=False, default='En Proceso')
