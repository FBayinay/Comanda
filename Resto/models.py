from . import db
class Role(db.Model):
    __tablename__ = 'roles'
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Role id={self.id_rol}, nombre={self.nombre}>'

class Action(db.Model):
    __tablename__ = 'acciones'
    id_accion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Action id={self.id_accion}, nombre={self.nombre}>'

class User(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(8), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    calle = db.Column(db.String(80), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id_rol'))
    id_accion = db.Column(db.Integer, db.ForeignKey('acciones.id_accion'), nullable=False)

    def __repr__(self):
        return (f'<User id={self.id_usuario}, nombre={self.nombre}, apellido={self.apellido}, '
                f'dni={self.dni}, email={self.email}, calle={self.calle}, numero={self.numero}, '
                f'rol_id={self.rol_id}, id_accion={self.id_accion}>')

class Login(db.Model):
    __tablename__ = 'login'
    id_login = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Login id={self.id_login}, id_usuario={self.id_usuario}, username={self.username}>'

class Product(db.Model):
    __tablename__ = 'productos'
    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Product id={self.id_producto}, nombre={self.nombre}>'

class Stock(db.Model):
    __tablename__ = 'stock'
    id_stock = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Stock id={self.id_stock}, id_producto={self.id_producto}, cantidad={self.cantidad}>'

class Supplier(db.Model):
    __tablename__ = 'proveedores'
    id_proveedor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    contacto = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Supplier id={self.id_proveedor}, nombre={self.nombre}, contacto={self.contacto}>'

class Order(db.Model):
    __tablename__ = 'pedidos_alamcen_general'
    id_pedido = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedores.id_proveedor'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    precio_total = db.Column(db.Numeric(10, 2), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return (f'<Order id={self.id_pedido}, id_usuario={self.id_usuario}, id_producto={self.id_producto}, '
                f'id_proveedor={self.id_proveedor}, cantidad={self.cantidad}, '
                f'precio_unitario={self.precio_unitario}, precio_total={self.precio_total}, fecha={self.fecha}>')

class WarehouseMovement(db.Model):
    __tablename__ = 'movimientos_almacen'
    id_movimiento = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return (f'<WarehouseMovement id={self.id_movimiento}, id_usuario={self.id_usuario}, '
                f'id_producto={self.id_producto}, cantidad={self.cantidad}, fecha={self.fecha}>')

class Table(db.Model):
    __tablename__ = 'mesas'
    id_mesa = db.Column(db.Integer, primary_key=True)
    numero_mesa = db.Column(db.Integer, nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return (f'<Table id={self.id_mesa}, numero_mesa={self.numero_mesa}, '
                f'capacidad={self.capacidad}, estado={self.estado}>')

class MenuCategory(db.Model):
    __tablename__ = 'categorias_menu'
    id_categoria = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return (f'<MenuCategory id={self.id_categoria}, categoria={self.categoria}, '
                f'descripcion={self.descripcion}>')

class Menu(db.Model):
    __tablename__ = 'menus'
    id_menu = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    fecha_inicio = db.Column(db.String(10), nullable=False)
    fecha_fin = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return (f'<Menu id={self.id_menu}, tipo={self.tipo}, fecha_inicio={self.fecha_inicio}, '
                f'fecha_fin={self.fecha_fin}>')

class MenuItem(db.Model):
    __tablename__ = 'items_menu'
    id_items = db.Column(db.Integer, primary_key=True)
    id_menu = db.Column(db.Integer, db.ForeignKey('menus.id_menu'), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias_menu.id_categoria'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    precio = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return (f'<MenuItem id={self.id_items}, id_menu={self.id_menu}, id_categoria={self.id_categoria}, '
                f'nombre={self.nombre}, descripcion={self.descripcion}, precio={self.precio}>')

class Command(db.Model):
    __tablename__ = 'comanda'
    id_comanda = db.Column(db.Integer, primary_key=True)
    id_mesa = db.Column(db.Integer, db.ForeignKey('mesas.id_mesa'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    fecha_fin = db.Column(db.DateTime, nullable=True)
    estado = db.Column(db.String(50), nullable=False, default='En Proceso')

    def __repr__(self):
        return (f'<Command id={self.id_comanda}, id_mesa={self.id_mesa}, id_usuario={self.id_usuario}, '
                f'fecha_inicio={self.fecha_inicio}, fecha_fin={self.fecha_fin}, estado={self.estado}>')

class CommandDetail(db.Model):
    __tablename__ = 'detalles_comanda'
    id_detalles = db.Column(db.Integer, primary_key=True)
    id_comanda = db.Column(db.Integer, db.ForeignKey('comanda.id_comanda'), nullable=False)
    id_item_menu = db.Column(db.Integer, db.ForeignKey('items_menu.id_items'), nullable=False)
    id_menu = db.Column(db.Integer, db.ForeignKey('menus.id_menu'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_total = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return (f'<CommandDetail id={self.id_detalles}, id_comanda={self.id_comanda}, '
                f'id_item_menu={self.id_item_menu}, id_menu={self.id_menu}, '
                f'cantidad={self.cantidad}, precio_total={self.precio_total}>')

class Receipt(db.Model):
    __tablename__ = 'recibo_cliente'
    id_recibo = db.Column(db.Integer, primary_key=True)
    id_comanda = db.Column(db.Integer, db.ForeignKey('comanda.id_comanda'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado_pago = db.Column(db.String(50), nullable=False, default='Pendiente')
    detalles_comanda = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return (f'<Receipt id={self.id_recibo}, id_comanda={self.id_comanda}, fecha={self.fecha}, '
                f'total={self.total}, estado_pago={self.estado_pago}, detalles_comanda={self.detalles_comanda}>')
