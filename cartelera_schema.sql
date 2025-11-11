-- cartelera_schema.sql
-- Definición del esquema de la base de datos de la cartelera
-- Generado a partir de los modelos ORM de SQLAlchemy

PRAGMA foreign_keys = ON; -- Asegura que las claves foráneas estén activas en SQLite

-- Tabla Generos
CREATE TABLE generos (
	id INTEGER NOT NULL, 
	nombre VARCHAR(100) NOT NULL UNIQUE, 
	descripcion VARCHAR(500), 
	PRIMARY KEY (id)
);

-- Tabla Peliculas
CREATE TABLE peliculas (
	id INTEGER NOT NULL, 
	titulo VARCHAR(255) NOT NULL, 
	genero_id INTEGER NOT NULL, 
	duracion INTEGER NOT NULL, 
	disponible BOOLEAN NOT NULL, 
	director VARCHAR(100), 
	descripcion VARCHAR(1000), 
	trailer VARCHAR(255), 
	productora VARCHAR(100), 
	idioma VARCHAR(50), 
	vose BOOLEAN, 
	actores JSON, 
	PRIMARY KEY (id), 
	FOREIGN KEY(genero_id) REFERENCES generos (id)
);