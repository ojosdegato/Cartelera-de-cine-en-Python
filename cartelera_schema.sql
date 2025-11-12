-- cartelera_schema.sql
-- Definición completa del esquema de la base de datos (DDL) para todas las entidades del proyecto.
-- Incluye Pelicula, Genero, Sala, Horario, Venta y Socio.

PRAGMA foreign_keys = ON; -- Asegura que las claves foráneas estén activas en SQLite

-----------------------------------------------------------------------
-- 1. TABLA GENEROS (KARY)
-----------------------------------------------------------------------
CREATE TABLE generos (
	id INTEGER NOT NULL PRIMARY KEY, 
	nombre VARCHAR(100) NOT NULL UNIQUE, 
	descripcion VARCHAR(500)
);

-----------------------------------------------------------------------
-- 2. TABLA PELICULAS (JAVIER)
-----------------------------------------------------------------------
CREATE TABLE peliculas (
	id INTEGER NOT NULL PRIMARY KEY, 
	titulo VARCHAR(255) NOT NULL, 
	
	-- Relación Many-to-One con Genero
	genero_id INTEGER NOT NULL, 
	
	duracion INTEGER NOT NULL, 
	disponible BOOLEAN NOT NULL, 
	
	-- Campos Opcionales (pueden ser NULL en la BBDD)
	director VARCHAR(100), 
	descripcion VARCHAR(1000), 
	trailer VARCHAR(255), 
	productora VARCHAR(100), 
	idioma VARCHAR(50), 
	vose BOOLEAN, 
	actores JSON, -- Lista de actores (almacenada como JSON/string en SQLite)
	
	FOREIGN KEY(genero_id) REFERENCES generos (id)
);

-----------------------------------------------------------------------
-- 3. TABLA SALAS (REYES)
-----------------------------------------------------------------------
CREATE TABLE salas (
	id INTEGER NOT NULL PRIMARY KEY, 
	numero VARCHAR(50) NOT NULL UNIQUE, -- Usamos VARCHAR por si son 'Sala IMAX' o 'Sala A'
	capacidad INTEGER NOT NULL, 
	tipo VARCHAR(50) NOT NULL, -- 'normal', '3d', 'imax', 'premium'
	precio_base FLOAT NOT NULL,
	disponible BOOLEAN NOT NULL DEFAULT 1
);

-----------------------------------------------------------------------
-- 4. TABLA SOCIOS (Javier - Mejora)
-----------------------------------------------------------------------
CREATE TABLE socios (
	id INTEGER NOT NULL PRIMARY KEY, 
	nombre VARCHAR(100) NOT NULL,
	apellidos VARCHAR(100) NOT NULL,
	email VARCHAR(150) NOT NULL UNIQUE,
	telefono VARCHAR(20),
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN NOT NULL DEFAULT 1
);

-----------------------------------------------------------------------
-- 5. TABLA HORARIOS (MANUEL)
-----------------------------------------------------------------------
CREATE TABLE horarios (
	id INTEGER NOT NULL PRIMARY KEY, 
	
	-- Relaciones Many-to-One
	pelicula_id INTEGER NOT NULL, 
	sala_id INTEGER NOT NULL, 
	
	hora VARCHAR(20) NOT NULL, -- Usamos VARCHAR para simplificar el manejo de datetime/string en SQLite
	disponible BOOLEAN NOT NULL,
	
	FOREIGN KEY(pelicula_id) REFERENCES peliculas (id),
	FOREIGN KEY(sala_id) REFERENCES salas (id)
);

-----------------------------------------------------------------------
-- 6. TABLA VENTAS (IÑAKI)
-----------------------------------------------------------------------
CREATE TABLE ventas (
	id INTEGER NOT NULL PRIMARY KEY, 
	
	-- Relación con Horario (Define qué función se vendió)
	horario_id INTEGER NOT NULL,
	
	-- Relación OPCIONAL con Socio (Para ventas con fidelidad)
	socio_id INTEGER, 
	
	precio_total FLOAT NOT NULL, 
	cantidad INTEGER NOT NULL, 
	metodo_pago VARCHAR(50) NOT NULL, -- 'efectivo', 'tarjeta', 'cripto'
	
	FOREIGN KEY(horario_id) REFERENCES horarios (id),
    FOREIGN KEY(socio_id) REFERENCES socios (id)
);