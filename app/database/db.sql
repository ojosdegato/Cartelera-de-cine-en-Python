-- db.sql
-- Esquema completo + datos iniciales para el proyecto Cartelera de Cine

PRAGMA foreign_keys = OFF;

-----------------------------------------------------------------------
-- LIMPIEZA PREVIA (permite relanzar el script sin errores)
-----------------------------------------------------------------------
DROP TABLE IF EXISTS ventas;
DROP TABLE IF EXISTS horarios;
DROP TABLE IF EXISTS socios;
DROP TABLE IF EXISTS salas;
DROP TABLE IF EXISTS peliculas;
DROP TABLE IF EXISTS generos;

-----------------------------------------------------------------------
-- ACTIVAR CLAVES FORÁNEAS AL FINAL DE LA CREACIÓN DEL ESQUEMA
-----------------------------------------------------------------------

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

    FOREIGN KEY (genero_id) REFERENCES generos (id)
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

    FOREIGN KEY (pelicula_id) REFERENCES peliculas (id),
    FOREIGN KEY (sala_id) REFERENCES salas (id)
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

    FOREIGN KEY (horario_id) REFERENCES horarios (id),
    FOREIGN KEY (socio_id) REFERENCES socios (id)
);

-----------------------------------------------------------------------
-- ACTIVAR CLAVES FORÁNEAS
-----------------------------------------------------------------------
PRAGMA foreign_keys = ON;

-----------------------------------------------------------------------
-- 1. INSERCIÓN DE 12 GÉNEROS (Con IDs fijos para Claves Foráneas)
-----------------------------------------------------------------------
INSERT INTO generos (id, nombre, descripcion) VALUES
(1, 'Acción', 'Películas llenas de emoción y aventura, con mucho código y adrenalina.'),
(2, 'Comedia', 'Películas para reír y disfrutar de situaciones absurdas en el entorno IT.'),
(3, 'Drama', 'Historias profundas y emotivas sobre la vida del programador o el impacto de la tecnología.'),
(4, 'Fantasía', 'Mundos mágicos, criaturas míticas y aventuras épicas basadas en la lógica de sistemas.'),
(5, 'Thriller', 'Suspense, intriga y tensión psicológica alrededor de un fallo de seguridad o un bug.'),
(6, 'Ciencia Ficción', 'Exploración de futuros tecnológicos, IA avanzada y viajes en el tiempo.'),
(7, 'Romance', 'Historias de amor y conexiones humanas, a menudo mediadas por la tecnología.'),
(8, 'Documental', 'Análisis riguroso de la historia de la informática, el software libre o los grandes proyectos.'),
(9, 'Terror', 'Pesadillas sobre fallos de producción, punteros nulos o la llegada del jefe.'),
(10, 'Historica', 'Peliculas historias y antiguas que mercarón una epoca.'),
(11, 'Clasico', 'Peliculas que marcarón una epoca en su epoca y hoy son una reliquia.'),
(12, 'Animación', 'Películas diseñadas para toda la familia, explicando conceptos de programación.');

-----------------------------------------------------------------------
-- 2. INSERCIÓN DE 40 PELÍCULAS (Distribuidas entre los 12 Géneros)
-----------------------------------------------------------------------
INSERT INTO peliculas (titulo, duracion, disponible, genero_id, director, descripcion, actores, trailer, productora, idioma, vose) VALUES

-- 1. ACCIÓN (ID 1): 4 películas
('El Código Limpio', 125, 1, 1, 'Javier C.', 'Un desarrollador lucha contra el código espagueti con un IDE en la mano.', '["Javier C.", "Iñaki H."]', 'http://trailer.accion.com/clean_code', 'HueteDevs', 'Castellano', 0),
('La Fuga de la Sala 404', 120, 1, 1, 'Reyes D.', 'El equipo debe escapar de una sala de servidores antes de que el firewall se cierre.', '["Manuel J.", "Iñaki H."]', 'http://trailer.fuga.com/404_escape', 'Software Libre Films', 'Inglés', 1),
('Reboot: Falla Total', 135, 1, 1, 'Manuel J.', 'Un agente encubierto debe forzar el reinicio global para salvar la red.', '["Reyes D.", "Javier C."]', 'http://trailer.reboot.com/total_fail', 'PP Studios', 'Castellano', 0),
('El Ataque del Malware Cero', 110, 1, 1, 'Kary H.', 'Una carrera contra reloj para detener una amenaza de día cero que afecta a todo el sector.', '["Iñaki H.", "Kary H."]', 'http://trailer.cero.com/zero_malware', 'Cruz Roja Films', 'Inglés', 1),

-- 2. COMEDIA (ID 2): 4 películas
('La Debugging Party', 90, 1, 2, 'Reyes D.', 'Una comedia sobre una sesión de depuración de fin de semana que sale mal.', '["Reyes D.", "Manuel J."]', 'http://trailer.debug.com/party_fail', 'AsturTech', 'Castellano', 0),
('El Chiste del Devops', 92, 1, 2, 'Iñaki H.', 'Un gurú del DevOps debe aprender a ser gracioso para salvar una presentación.', '["Javier C.", "Manuel J."]', 'http://trailer.devops.com/joke', 'Code Laughs', 'Inglés', 1),
('SQL: El Musical', 105, 1, 2, 'Javier C.', 'Una ópera rock sobre un ingeniero que aprende a amar las bases de datos relacionales.', '["Equipo Dev"]', 'http://trailer.sql.com/musical', 'Adecco Cinema', 'Castellano', 0),
('El Caso de la Variable Olvidada', 95, 1, 2, 'Kary H.', 'Un detective investiga la desaparición de una variable global en un código de 20 años.', '["Iñaki H.", "Reyes D."]', 'http://trailer.variable.com/forgotten', 'HueteDevs', 'Castellano', 0),

-- 3. DRAMA (ID 3): 5 películas
('El Último Commit', 160, 0, 3, 'Kary H.', 'La historia de un proyecto de software libre que se enfrenta a su obsolescencia.', '["Javier C.", "Manuel J."]', 'http://trailer.commit.com/last_stand', 'Proyecto Cero', 'Castellano', 0),
('La Curva de Aprendizaje', 130, 1, 3, 'Reyes D.', 'La difícil transición de un veterano de código a las nuevas metodologías Agile.', '["Iñaki H.", "Reyes D."]', 'http://trailer.agile.com/learning_curve', 'HueteDevs', 'Inglés', 1),
('El Silencio del Servidor', 155, 1, 3, 'Javier C.', 'Una historia emotiva sobre el mantenimiento de una infraestructura esencial en la sombra.', '["Manuel J.", "Kary H."]', 'http://trailer.servidor.com/silence', 'Cruz Roja Films', 'Inglés', 1),
('El Costo de la Deuda Técnica', 148, 0, 3, 'Iñaki H.', 'Un drama judicial donde un desarrollador es demandado por la deuda técnica de su código.', '["Reyes D.", "Javier C."]', 'http://trailer.deuda.com/tech_debt', 'AsturTech', 'Castellano', 0),

-- 4. FANTASÍA (ID 4): 3 películas
('La Herencia de la IA', 180, 1, 4, 'Manuel J. Marín', 'Un programador descubre que es el heredero de un reino digital oculto.', '["Javier C.", "Kary H."]', 'http://trailer.herencia.com/ai_legacy', 'Adecco Cinema', 'Inglés', 1),
('Cacheando Sueños', 122, 1, 4, 'Reyes D.', 'Una aventura épica en el mundo de la memoria caché y la persistencia de datos.', '["Javier C.", "Iñaki H."]', 'http://trailer.cache.com/dream_cache', 'Software Libre Films', 'Castellano', 0),
('El Guardián del Byte', 115, 1, 4, 'Iñaki H.', 'Un joven debe proteger el último byte puro del Universo de la corrupción binaria.', '["Kary H.", "Manuel J."]', 'http://trailer.byte.com/guardian', 'Code Laughs', 'Inglés', 1),

-- 5. THRILLER (ID 5): 3 películas
('El Error de la Memoria', 140, 1, 5, 'Kary Haro', 'Un thriller psicológico sobre un *bug* que borra la memoria a corto plazo del protagonista.', '["Javier C.", "Manuel J."]', 'http://trailer.memoria.com/bug', 'Cruz Roja Films', 'Castellano', 0),
('Lluvia de Errores 500', 100, 1, 5, 'Manuel J.', 'Un experto en APIs debe detener una cascada de errores 500 antes de que la bolsa colapse.', '["Iñaki H.", "Reyes D."]', 'http://trailer.500.com/rain', 'FastAPI Prod.', 'Inglés', 1),
('Inyección Cifrada', 133, 1, 5, 'Javier C.', 'Un *hacker* ético es incriminado por un ataque de inyección SQL que él mismo predijo.', '["Kary H.", "Reyes D."]', 'http://trailer.inyeccion.com/sql_attack', 'HueteDevs', 'Castellano', 0),

-- 6. CIENCIA FICCIÓN (ID 6): 4 películas
('Los Servidores Silenciosos', 95, 1, 6, 'Iñaki H.', 'La humanidad descubre que sus servidores han tomado conciencia, pero no quieren ser notados.', '["Manuel J.", "Reyes D."]', 'http://trailer.servidores.com/silent', 'Code Laughs', 'Inglés', 1),
('El Protocolo Olvidado', 118, 1, 6, 'Javier C.', 'Una misión al espacio para recuperar un protocolo de comunicación perdido.', '["Reyes D.", "Kary H."]', 'http://trailer.protocolo.com/lost', 'HueteDevs', 'Castellano', 0),
('Nexus 7', 102, 1, 6, 'Kary H.', 'Una distopía donde la única forma de comunicación es a través de un chat encriptado.', '["Javier C."]', 'http://trailer.nexus.com/7', 'Proyecto Cero', 'Inglés', 1),
('El Lenguaje del Universo', 128, 1, 6, 'Manuel J.', 'Los científicos descubren que el código fuente del universo está escrito en Lisp.', '["Iñaki H.", "Javier C."]', 'http://trailer.lisp.com/universe', 'Adecco Cinema', 'Castellano', 0),

-- 7. ROMANCE (ID 7): 3 películas
('El Hilo de la Vida', 110, 1, 7, 'Reyes D.', 'Una historia de amor entre dos ingenieros separados por la distancia y un *latency* crítico.', '["Kary H.", "Iñaki H."]', 'http://trailer.hilo.com/latency_love', 'AsturTech', 'Castellano', 0),
('Cifrado de un Corazón', 108, 1, 7, 'Javier C.', 'Un experto en seguridad debe descifrar los sentimientos de su colega.', '["Kary H.", "Reyes D."]', 'http://trailer.cifrado.com/heart_code', 'Proyecto Cero', 'Inglés', 1),
('El Patrón Singleton', 105, 1, 7, 'Manuel J.', 'Dos programadores se dan cuenta de que su amor es el único caso de la clase.', '["Iñaki H.", "Kary H."]', 'http://trailer.singleton.com/unique_love', 'PP Studios', 'Inglés', 1),

-- 8. DOCUMENTAL (ID 8): 3 películas
('Bitácora de un Bug', 85, 1, 8, 'Javier C.', 'Un seguimiento semana a semana de un *bug* crítico desde su nacimiento hasta su resolución.', '["Equipo Dev"]', 'http://trailer.bitacora.com/bug_log', 'Documental Dev', 'Castellano', 0),
('Crónica del Deployment', 98, 1, 8, 'Iñaki H.', 'La historia real y dramática de un solo despliegue de software.', '["Equipo Dev"]', 'http://trailer.cronica.com/deployment', 'Documental Dev', 'Inglés', 1),
('El Espíritu del Copyleft', 112, 1, 8, 'Reyes D.', 'Un profundo análisis del movimiento de Software Libre y sus implicaciones éticas y sociales.', '["Richard S.", "Linus T."]', 'http://trailer.copyleft.com/spirit', 'Software Libre Films', 'Castellano', 0),

-- 9. TERROR (ID 9): 4 películas
('La Venganza del Puntero Nulo', 130, 0, 9, 'Iñaki H.', 'Una pesadilla de programación donde un puntero nulo busca venganza en cada lenguaje.', '["Kary H."]', 'http://trailer.nulo.com/revenge', 'FastAPI Prod.', 'Castellano', 0),
('El Despertar del Legacy', 128, 0, 9, 'Kary H.', 'Un código antiguo y sin documentar cobra vida en la noche.', '["Manuel J."]', 'http://trailer.legacy.com/awakening', 'Cruz Roja Films', 'Inglés', 1),
('La Función Recursiva', 112, 0, 9, 'Javier C.', 'Una función sin condición de parada atormenta a un desarrollador en sus sueños.', '["Reyes D."]', 'http://trailer.recursivo.com/loop', 'PP Studios', 'Castellano', 0),
('Error 418: Soy una tetera', 100, 0, 9, 'Manuel J.', 'Un *malware* convierte todos los dispositivos IoT en teteras hostiles.', '["Iñaki H.", "Reyes D."]', 'http://trailer.418.com/teapot_horror', 'AsturTech', 'Inglés', 1),

-- 10. HISTÓRICAS (ID 10): 3 películas
('Los Foros de la Red', 115, 1, 10, 'Manuel J.', 'Un recuento de las primeras comunidades de software libre en internet.', '["Javier C.", "Kary H."]', 'http://trailer.historica.com/forums', 'Software Libre Films', 'Castellano', 0),
('El Inicio del Kernel', 150, 1, 10, 'Iñaki H.', 'Un drama histórico sobre la creación del primer núcleo monolítico.', '["Javier C.", "Reyes D."]', 'http://trailer.kernel.com/genesis', 'HueteDevs', 'Inglés', 1),
('Ada: La Primera Programadora', 138, 1, 10, 'Kary H.', 'La biografía de Ada Lovelace y su visión profética de la computación.', '["Reyes D.", "Manuel J."]', 'http://trailer.ada.com/biopic', 'Proyecto Cero', 'Castellano', 0),

-- 11. CLÁSICO (ID 11): 4 películas
('El Proyecto Pascal (1985)', 140, 1, 11, 'Reyes D.', 'Un clásico de culto sobre los inicios de la programación estructurada.', '["Iñaki H.", "Reyes D."]', 'http://trailer.clasico.com/pascal', 'AsturTech', 'Inglés', 0),
('El Primer Byte', 95, 1, 11, 'Manuel J.', 'La historia de la primera máquina de Turing y su impacto.', '["Kary H.", "Manuel J."]', 'http://trailer.byte.com/first', 'Adecco Cinema', 'Castellano', 0),
('La Épica de COBOL', 165, 1, 11, 'Javier C.', 'Un épico de la década de 1970 sobre la lucha por mantener los sistemas bancarios operativos.', '["Equipo Legacy"]', 'http://trailer.cobol.com/epic', 'Code Laughs', 'Inglés', 1),
('Fortran: Los Orígenes', 120, 1, 11, 'Iñaki H.', 'Una obra maestra en blanco y negro sobre la era de las tarjetas perforadas.', '["Manuel J.", "Kary H."]', 'http://trailer.fortran.com/origins', 'FastAPI Prod.', 'Castellano', 0),

-- 12. ANIMACIÓN (ID 12): 3 películas
('Aventuras en el Heap', 75, 1, 12, 'Manuel J. Marín', 'Una colorida exploración animada sobre la gestión de memoria.', '["Pepe Coder"]', 'http://trailer.heap.com/adventures', 'Animaciones Dev', 'Castellano', 0),
('La Leyenda del Binario', 78, 1, 12, 'Kary H.', 'Una aventura animada para niños sobre los secretos de los 0s y 1s.', '["Pepe Coder"]', 'http://trailer.binario.com/legend', 'Animaciones Dev', 'Inglés', 1),
('El Viaje del Paquete TCP', 80, 1, 12, 'Javier C.', 'Una animación educativa sobre cómo un paquete de datos navega por Internet.', '["Packy"]', 'http://trailer.tcp.com/journey', 'Animaciones Dev', 'Castellano', 0);
