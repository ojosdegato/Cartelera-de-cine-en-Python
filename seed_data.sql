-- seed_data.sql
-- Datos iniciales para Peliculas y Generos (10 Géneros, 20 Películas)

-- Deshabilitar temporalmente las claves foráneas para inserción forzada
PRAGMA foreign_keys = OFF; 


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
(10, 'Historicas', 'Peliculas historias y antiguas que mercarón una epoca.'),
(11, 'Clasico', 'Peliculas que marcarón una epoca en su epoca y hoy son una reliquia.'),
(12, 'Animación', 'Películas diseñadas para toda la familia, explicando conceptos de programación.');

-- Actualizar la secuencia de IDs para que la próxima inserción use el ID 13
--# UPDATE sqlite_sequence SET seq = 12 WHERE name = 'generos';


-----------------------------------------------------------------------
-- 2. INSERCIÓN DE 20 PELÍCULAS (Distribuidas entre los 10 Géneros)
-----------------------------------------------------------------------

INSERT INTO peliculas (titulo, duracion, disponible, genero_id, director, descripcion, actores, trailer) VALUES
-- ACCIÓN (ID 1)
('El Código Limpio', 125, 1, 1, 'Javier C.', 'Un desarrollador lucha contra el código espagueti con un IDE en la mano.', '["Javier C.", "Iñaki H."]', 'http://trailer.accion.com'),
('La Fuga de la Sala 404', 120, 1, 1, 'Reyes D.', 'El equipo debe escapar de una sala de servidores antes de que el firewall se cierre.', '["Manuel J.", "Iñaki H."]', 'http://trailer.fuga.com'),

-- COMEDIA (ID 2)
('La Debugging Party', 90, 1, 2, 'Reyes D.', 'Una comedia sobre una sesión de depuración de fin de semana que sale mal.', '["Reyes D.", "Manuel J."]', 'http://trailer.debug.com'),
('El Chiste del Devops', 92, 1, 2, 'Iñaki H.', 'Un gurú del DevOps debe aprender a ser gracioso para salvar una presentación.', '["Javier C.", "Manuel J."]', 'http://trailer.devops.com'),

-- DRAMA (ID 3)
('El Último Commit', 160, 0, 3, 'Kary H.', 'La historia de un proyecto de software libre que se enfrenta a su obsolescencia.', '["Javier C.", "Manuel J."]', 'http://trailer.commit.com'),
('Tarde de Viernes', 145, 0, 3, 'Manuel J.', 'Un drama sobre el dilema moral de hacer un deployment crítico un viernes por la tarde.', '["Javier C.", "Kary H."]', 'http://trailer.viernes.com'),

-- FANTASÍA (ID 4)
('La Herencia de la IA', 180, 1, 4, 'Manuel J. Marín', 'Un programador descubre que es el heredero de un reino digital oculto.', '["Javier C.", "Kary H."]', 'http://trailer.herencia.com'),
('Cacheando Sueños', 122, 1, 4, 'Reyes D.', 'Una aventura épica en el mundo de la memoria caché y la persistencia de datos.', '["Javier C.", "Iñaki H."]', 'http://trailer.cache.com'),

-- THRILLER (ID 5)
('El Error de la Memoria', 140, 1, 5, 'Kary Haro', 'Un thriller psicológico sobre un bug que borra la memoria a corto plazo del protagonista.', '["Javier C.", "Manuel J."]', 'http://trailer.memoria.com'),
('Lluvia de Errores 500', 100, 1, 5, 'Manuel J.', 'Un experto en APIs debe detener una cascada de errores 500 antes de que la bolsa colapse.', '["Iñaki H.", "Reyes D."]', 'http://trailer.500.com'),

-- CIENCIA FICCIÓN (ID 6)
('Los Servidores Silenciosos', 95, 1, 6, 'Iñaki H.', 'La humanidad descubre que sus servidores han tomado conciencia, pero no quieren ser notados.', '["Manuel J.", "Reyes D."]', 'http://trailer.servidores.com'),
('El Protocolo Olvidado', 118, 1, 6, 'Javier C.', 'Una misión al espacio para recuperar un protocolo de comunicación perdido.', '["Reyes D.", "Kary H."]', 'http://trailer.protocolo.com'),

-- ROMANCE (ID 7)
('El Hilo de la Vida', 110, 1, 7, 'Reyes D.', 'Una historia de amor entre dos ingenieros separados por la distancia y un latency crítico.', '["Kary H.", "Iñaki H."]', 'http://trailer.hilo.com'),
('Cifrado de un Corazón', 108, 1, 7, 'Javier C.', 'Un experto en seguridad debe descifrar los sentimientos de su colega.', '["Kary H.", "Reyes D."]', 'http://trailer.cifrado.com'),

-- DOCUMENTAL (ID 8)
('Bitácora de un Bug', 85, 1, 8, 'Javier C.', 'Un seguimiento semana a semana de un bug crítico desde su nacimiento hasta su resolución.', '["Equipo Dev"]', 'http://trailer.bitacora.com'),
('Crónica del Deployment', 98, 1, 8, 'Iñaki H.', 'La historia real y dramática de un solo despliegue de software.', '["Equipo Dev"]', 'http://trailer.cronica.com'),

-- TERROR (ID 9)
('La Venganza del Puntero Nulo', 130, 0, 9, 'Iñaki H.', 'Una pesadilla de programación donde un puntero nulo busca venganza en cada lenguaje.', '["Kary H."]', 'http://trailer.nulo.com'),
('El Despertar del Legacy', 128, 0, 9, 'Kary H.', 'Un código antiguo y sin documentar cobra vida en la noche.', '["Manuel J."]', 'http://trailer.legacy.com'),

-- ANIMACIÓN (ID 10)
('Aventuras en el Heap', 75, 1, 10, 'Manuel J. Marín', 'Una colorida exploración animada sobre la gestión de memoria.', '["Pepe Coder"]', 'http://trailer.heap.com'),
('La Leyenda del Binario', 78, 1, 10, 'Kary H.', 'Una aventura animada para niños sobre los secretos de los 0s y 1s.', '["Pepe Coder"]', 'http://trailer.binario.com');

-- Volver a habilitar las claves foráneas
PRAGMA foreign_keys = ON;