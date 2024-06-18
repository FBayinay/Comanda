-- Tabla Roles
CREATE TABLE roles(
	id_rol SERIAL PRIMARY KEY,
	Nombre VARCHAR(50) NOT NULL
);
--Tabla Restaurantes
CREATE TABLE restaurantes(
	id_restaurante SERIAL PRIMARY KEY,
	Nombre VARCHAR(50)NOT NULL,
	Direccion VARCHAR(100) NOT NULL UNIQUE
);
--Tabla Usuarios
CREATE TABLE usuarios(
	id_usuario SERIAL PRIMARY KEY,
	Nombre VARCHAR(50) NOT NULL,
	Apellido VARCHAR(50) NOT NULL,
	Email VARCHAR(100) NOT NULL UNIQUE,
	RolID INT REFERENCES roles(id_rol),
	id_restaurante INT REFERENCES restaurantes(id_restaurante)
); 
--Tabla Almacenes
CREATE TABLE almacenes(
	id_almacenes SERIAL PRIMARY KEY,
	Nombre VARCHAR(50) NOT NULL,
	id_restaurante INT REFERENCES restaurantes(id_restaurante) UNIQUE,
	Tipo VARCHAR(50) NOT NULL
);
--Tabla Productos
CREATE TABLE productos(
	id_producto SERIAL PRIMARY KEY,
	Nombre VARCHAR(50) NOT NULL
);
--Tabla Stock
CREATE TABLE stock(
	id_stock SERIAL PRIMARY KEY,
	id_producto INT REFERENCES productos(id_producto) NOT NULL,
	id_almacen INT REFERENCES almacenes(id_almacenes) NOT NULL,
	Cantidad INT CHECK(Cantidad>=0) NOT NULL
);
--Tabla Movimientos entre almacenes
CREATE TABLE movimientos_alamcenes(
	id_movimiento SERIAL PRIMARY KEY,
	UsuarioID INT REFERENCES usuarios(id_usuario) NOT NUll,
	AlmacenOrigenID INT REFERENCES almacenes(id_almacenes) NOT NULL,
	AlmacenDestinoID INT REFERENCES almacenes(id_almacenes) NOT NULL,
	id_producto INT REFERENCES productos(id_producto) NOT NULL,
	Cantidad INT CHECK(Cantidad>0) NOT NULL,
	Fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
--Tabla Proveedores
CREATE TABLE proveedores(
	id_proveedor SERIAL PRIMARY KEY,
	Nombre VARCHAR(50) NOT NULL,
	Contacto VARCHAR (20) NOT NULL
);
--Tabla Pedidos
CREATE TABLE pedidos_alamcen_general(
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
CREATE TABLE movimientos_almacen(
	id_movimiento SERIAL PRIMARY KEY,
	id_almacen INT REFERENCES almacenes(id_almacenes) NOT NULL,
	id_usuario INT REFERENCES usuarios(id_usuario) NOT NUll,
	id_producto INT REFERENCES productos(id_producto) NOT NULL,
	Cantidad INT CHECK (Cantidad <> 0) NOT NULL,
	Fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

--Tabla Mesas
CREATE TABLE mesas(
	id_mesa SERIAL PRIMARY KEY,
	id_restaurante INT REFERENCES restaurantes(id_restaurante) NOT NULL,
	Numero_mesa INT CHECK(Numero_mesa>0) NOT NULL,
	Capacidad INT CHECK(Capacidad>0) NOT NULL,
	Estado VARCHAR(20) NOT NULL
);
--Tabla Categorias Menu
CREATE TABLE categorias_menu(
	id_categoria SERIAL PRIMARY KEY,
	Categoria VARCHAR(50) NOT NULL,
	Descripcion VARCHAR(50) NOT NULL
);
--Tabla Menus
CREATE TABLE menus(
	id_menu SERIAL PRIMARY KEY,
	id_restaurante INT REFERENCES restaurantes(id_restaurante) NOT NULL,
	Tipo VARCHAR(50) NOT NULL,
	FechaInicio VARCHAR(10) NOT NULL,
    FechaFin VARCHAR(10) NULL,
   	CONSTRAINT chk_fecha_inicio CHECK (TO_DATE(FechaInicio, 'DD/MM/YYYY') IS NOT NULL),
    CONSTRAINT chk_fecha_fin CHECK (FechaFin IS NULL OR TO_DATE(FechaFin, 'DD/MM/YYYY') IS NOT NULL)
);
--Tabla ItemsMenu
CREATE TABLE items_menu(
	id_items SERIAL PRIMARY KEY,
	id_menu INT REFERENCES menus(id_menu) NOT NULL,
	id_categoria INT REFERENCES categorias_menu(id_categoria) NOT NULL,
	Nombre VARCHAR(100) NOT NULL,
	Descripcion VARCHAR(200),
	Precio NUMERIC(10,2) NOT NULL CHECK(PRECIO>=0)
);
--Tabla Comanda
CREATE TABLE comanda(
	id_comanda SERIAL PRIMARY KEY,
	id_mesa INT REFERENCES mesas(id_mesa) NOT NULL,
	id_usuario INT REFERENCES usuarios(id_usuario) NOT NULL,
	Fecha_Inicio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	Fecha_Fin TIMESTAMP NULL,
    Estado VARCHAR(50) NOT NULL DEFAULT 'En Proceso'
);
--Tabla Detalles de la Comanda
CREATE TABLE detalles_comanda(
	id_detalles SERIAL PRIMARY KEY,
	id_comanda INT REFERENCES comanda(id_comanda) NOT NULL,
	id_item_menu INT REFERENCES items_menu(id_items) NOT NULL,
	id_menu INT REFERENCES menus(id_menu) NOT NULL,
	Cantidad INT NOT NULL,
	Precio_Total NUMERIC(10,2) NOT NULL CHECK (Precio_Total>=0)
);
--Tabla Recibo
CREATE TABLE recibo_cliente(
	id_recibo SERIAL PRIMARY KEY,
    id_comanda INT REFERENCES comanda(id_comanda) NOT NULL,
    Fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Total NUMERIC(10, 2) NOT NULL,
    EstadoPago VARCHAR(50) NOT NULL DEFAULT 'Pendiente',
    DetallesComanda TEXT
);