# comanda/tables/tables.py
from comanda.connection.connection import conectar_bd,cerrar_conexion
# Conectar a la base de datos
connection, cursor = conectar_bd()
def ensure_tables_exists():
    create_tables="""
    -- Tabla Roles
    CREATE TABLE IF NOT EXISTS roles(
	    id_rol SERIAL PRIMARY KEY,
	    Nombre VARCHAR(50) NOT NULL
    );
    -- Tabla Acciones
    CREATE TABLE IF NOT EXISTS acciones(
        id_accion SERIAL PRIMARY KEY,
        Nombre VARCHAR(50) NOT NULL
    );
    --Tabla Restaurantes
    CREATE TABLE IF NOT EXISTS restaurantes(
	    id_restaurante SERIAL PRIMARY KEY,
	    Nombre VARCHAR(50)NOT NULL,
	    Calle VARCHAR(100) NOT NULL,
        Numero INT CHECK(Numero>0) NOT NULL 
    );
    --Tabla Usuarios
    CREATE TABLE IF NOT EXISTS usuarios(
	    id_usuario SERIAL PRIMARY KEY,
	    Nombre VARCHAR(50) NOT NULL,
	    Apellido VARCHAR(50) NOT NULL,
        DNI CHAR(8) NOT NULL UNIQUE CHECK (dni ~ '^[0-9]{8}$'),
	    Email VARCHAR(100) NOT NULL UNIQUE,
        Calle VARCHAR(80) NOT NULL,
        Numero INT CHECK(Numero>0) NOT NULL, 
	    Rol_ID INT REFERENCES roles(id_rol),
        id_accion INT REFERENCES acciones(id_accion) NOT NULL,
	    id_restaurante INT REFERENCES restaurantes(id_restaurante)
    ); 
    -- Tabla login
    CREATE TABLE IF NOT EXISTS login (
        id_login SERIAL PRIMARY KEY,
        id_usuario INT UNIQUE REFERENCES usuarios(id_usuario),
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(100) NOT NULL
    );
    --Tabla Almacenes
    CREATE TABLE IF NOT EXISTS almacenes(
	    id_almacenes SERIAL PRIMARY KEY,
	    Nombre VARCHAR(50) NOT NULL,
	    id_restaurante INT REFERENCES restaurantes(id_restaurante) UNIQUE,
	    Tipo VARCHAR(50) NOT NULL
    );
    --Tabla Productos
    CREATE TABLE IF NOT EXISTS productos(
	    id_producto SERIAL PRIMARY KEY,
	    Nombre VARCHAR(50) NOT NULL
    );
    --Tabla Stock
    CREATE TABLE IF NOT EXISTS stock(
	    id_stock SERIAL PRIMARY KEY,
	    id_producto INT REFERENCES productos(id_producto) NOT NULL,
	    id_almacen INT REFERENCES almacenes(id_almacenes) NOT NULL,
	    Cantidad INT CHECK(Cantidad>=0) NOT NULL
    );
    --Tabla Movimientos entre almacenes
    CREATE TABLE IF NOT EXISTS movimientos_alamcenes(
        id_movimiento SERIAL PRIMARY KEY,
        UsuarioID INT REFERENCES usuarios(id_usuario) NOT NUll,
        AlmacenOrigenID INT REFERENCES almacenes(id_almacenes) NOT NULL,
        AlmacenDestinoID INT REFERENCES almacenes(id_almacenes) NOT NULL,
        id_producto INT REFERENCES productos(id_producto) NOT NULL,
        Cantidad INT CHECK(Cantidad>0) NOT NULL,
        Fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    --Tabla Proveedores
    CREATE TABLE IF NOT EXISTS proveedores(
        id_proveedor SERIAL PRIMARY KEY,
        Nombre VARCHAR(50) NOT NULL,
        Contacto VARCHAR (20) NOT NULL
    );
    --Tabla Pedidos
   CREATE TABLE IF NOT EXISTS pedidos_alamcen_general(
        id_pedido SERIAL PRIMARY KEY,
        id_usuario INT REFERENCES usuarios(id_usuario) NOT NULL,
        id_producto INT REFERENCES productos(id_producto) NOT NULL,
        id_proveedor INT REFERENCES proveedores(id_proveedor) NOT NULL,
        Cantidad INT CHECK(Cantidad>0) NOT NULL,
        Precio_Unitario NUMERIC(10,2) CHECK(Precio_Unitario>0) NOT NULL,
        Precio_Total NUMERIC(10,2) GENERATED ALWAYS AS (Cantidad * Precio_Unitario) STORED,
        Fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    --Tabla Movimiento en el mismo almacen
    CREATE TABLE IF NOT EXISTS movimientos_almacen(
        id_movimiento SERIAL PRIMARY KEY,
        id_almacen INT REFERENCES almacenes(id_almacenes) NOT NULL,
        id_usuario INT REFERENCES usuarios(id_usuario) NOT NUll,
        id_producto INT REFERENCES productos(id_producto) NOT NULL,
        Cantidad INT CHECK (Cantidad <> 0) NOT NULL,
        Fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    --Tabla Mesas
    CREATE TABLE IF NOT EXISTS mesas(
        id_mesa SERIAL PRIMARY KEY,
        id_restaurante INT REFERENCES restaurantes(id_restaurante) NOT NULL,
        Numero_mesa INT CHECK(Numero_mesa>0) NOT NULL,
        Capacidad INT CHECK(Capacidad>0) NOT NULL,
        Estado VARCHAR(20) NOT NULL
    );
    --Tabla Categorias Menu
    CREATE TABLE IF NOT EXISTS categorias_menu(
        id_categoria SERIAL PRIMARY KEY,
        Categoria VARCHAR(50) NOT NULL,
        Descripcion VARCHAR(50) NOT NULL
    );
    --Tabla Menus
    CREATE TABLE IF NOT EXISTS menus(
        id_menu SERIAL PRIMARY KEY,
        id_restaurante INT REFERENCES restaurantes(id_restaurante) NOT NULL,
        Tipo VARCHAR(50) NOT NULL,
        FechaInicio VARCHAR(10) NOT NULL,
        FechaFin VARCHAR(10) NULL,
        CONSTRAINT chk_fecha_inicio CHECK (TO_DATE(FechaInicio, 'DD/MM/YYYY') IS NOT NULL),
        CONSTRAINT chk_fecha_fin CHECK (FechaFin IS NULL OR TO_DATE(FechaFin, 'DD/MM/YYYY') IS NOT NULL)
    );
    --Tabla ItemsMenu
    CREATE TABLE IF NOT EXISTS items_menu(
        id_items SERIAL PRIMARY KEY,
        id_menu INT REFERENCES menus(id_menu) NOT NULL,
        id_categoria INT REFERENCES categorias_menu(id_categoria) NOT NULL,
        Nombre VARCHAR(100) NOT NULL,
        Descripcion VARCHAR(200),
        Precio NUMERIC(10,2) NOT NULL CHECK(PRECIO>=0)
    );
    --Tabla Comanda
    CREATE TABLE IF NOT EXISTS comanda(
        id_comanda SERIAL PRIMARY KEY,
        id_mesa INT REFERENCES mesas(id_mesa) NOT NULL,
        id_usuario INT REFERENCES usuarios(id_usuario) NOT NULL,
        Fecha_Inicio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        Fecha_Fin TIMESTAMP NULL,
        Estado VARCHAR(50) NOT NULL DEFAULT 'En Proceso'
    );
    --Tabla Detalles de la Comanda
    CREATE TABLE IF NOT EXISTS detalles_comanda(
        id_detalles SERIAL PRIMARY KEY,
        id_comanda INT REFERENCES comanda(id_comanda) NOT NULL,
        id_item_menu INT REFERENCES items_menu(id_items) NOT NULL,
        id_menu INT REFERENCES menus(id_menu) NOT NULL,
        Cantidad INT NOT NULL,
        Precio_Total NUMERIC(10,2) NOT NULL CHECK (Precio_Total>=0)
    );
    --Tabla Recibo
    CREATE TABLE IF NOT EXISTS recibo_cliente(
        id_recibo SERIAL PRIMARY KEY,
        id_comanda INT REFERENCES comanda(id_comanda) NOT NULL,
        Fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        Total NUMERIC(10, 2) NOT NULL,
        EstadoPago VARCHAR(50) NOT NULL DEFAULT 'Pendiente',
        DetallesComanda TEXT
    );

    """
    cursor.execute (create_tables)
    connection.commit()
ensure_tables_exists()


# Cerrar cursor y conexión al finalizar
cerrar_conexion(connection, cursor)