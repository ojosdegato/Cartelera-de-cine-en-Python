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

INSERT INTO peliculas (titulo, duracion, disponible, genero_id, director, descripcion, actores, trailer, productora, idioma, vose) VALUES
-- ACCIÓN (ID 1)
('El Código Limpio', 125, 1, 1, 'Javier C.', 'Un desarrollador lucha contra el código espagueti con un IDE en la mano.', '["Javier C.", "Iñaki H."]', 'http://trailer.accion.com', 'HueteDevs', 'Castellano', 0),
('La Fuga de la Sala 404', 120, 1, 1, 'Reyes D.', 'El equipo debe escapar de una sala de servidores antes de que el firewall se cierre.', '["Manuel J.", "Iñaki H."]', 'http://trailer.fuga.com', 'Software Libre Films', 'Inglés', 1),
('Reboot: Falla Total', 135, 1, 1, 'Manuel J.', 'Un agente encubierto debe forzar el reinicio global para salvar la red.', '["Reyes D.", "Javier C."]', 'https://www.google.com/search?q=http://trailer.reboot.com', 'PP Studios', 'Castellano', 0),
('El Ataque del Malware Cero', 110, 1, 1, 'Kary H.', 'Una carrera contra reloj para detener una amenaza de día cero que afecta a todo el sector.', '["Iñaki H.", "Kary H."]', 'https://www.google.com/search?q=http://trailer.cero.com', 'Cruz Roja Films', 'Inglés', 1),

-- COMEDIA (ID 2)
('La Debugging Party', 90, 1, 2, 'Reyes D.', 'Una comedia sobre una sesión de depuración de fin de semana que sale mal.', '["Reyes D.", "Manuel J."]', 'http://trailer.debug.com', 'AsturTech', 'Castellano', 0),
('El Chiste del Devops', 92, 1, 2, 'Iñaki H.', 'Un gurú del DevOps debe aprender a ser gracioso para salvar una presentación.', '["Javier C.", "Manuel J."]', 'http://trailer.devops.com', 'Code Laughs', 'Inglés', 1),
('SQL: El Musical', 105, 1, 2, 'Javier C.', 'Una ópera rock sobre un ingeniero que aprende a amar las bases de datos relacionales.', '["Equipo Dev"]', 'https://www.google.com/search?q=http://trailer.sql.com', 'Adecco Cinema', 'Castellano', 0),

-- DRAMA (ID 3)
('El Último Commit', 160, 0, 3, 'Kary H.', 'La historia de un proyecto de software libre que se enfrenta a su obsolescencia.', '["Javier C.", "Manuel J."]', 'http://trailer.commit.com', 'Proyecto Cero', 'Castellano', 0),
('Tarde de Viernes', 145, 0, 3, 'Manuel J.', 'Un drama sobre el dilema moral de hacer un deployment crítico un viernes por la tarde.', '["Javier C.", "Kary H."]', 'http://trailer.viernes.com', 'PP Studios', 'Castellano', 0),
('La Curva de Aprendizaje', 130, 1, 3, 'Reyes D.', 'La difícil transición de un veterano de código a las nuevas metodologías Agile.', '["Iñaki H.", "Reyes D."]', 'https://www.google.com/search?q=http://trailer.agile.com', 'HueteDevs', 'Inglés', 1),

-- FANTASÍA (ID 4)
('La Herencia de la IA', 180, 1, 4, 'Manuel J. Marín', 'Un programador descubre que es el heredero de un reino digital oculto.', '["Javier C.", "Kary H."]', 'http://trailer.herencia.com', 'Adecco Cinema', 'Inglés', 1),
('Cacheando Sueños', 122, 1, 4, 'Reyes D.', 'Una aventura épica en el mundo de la memoria caché y la persistencia de datos.', '["Javier C.", "Iñaki H."]', 'http://trailer.cache.com', 'Software Libre Films', 'Castellano', 0),

-- THRILLER (ID 5)
('El Error de la Memoria', 140, 1, 5, 'Kary Haro', 'Un thriller psicológico sobre un bug que borra la memoria a corto plazo del protagonista.', '["Javier C.", "Manuel J."]', 'http://trailer.memoria.com', 'Cruz Roja Films', 'Castellano', 0),
('Lluvia de Errores 500', 100, 1, 5, 'Manuel J.', 'Un experto en APIs debe detener una cascada de errores 500 antes de que la bolsa colapse.', '["Iñaki H.", "Reyes D."]', 'http://trailer.500.com', 'FastAPI Prod.', 'Inglés', 1),

-- CIENCIA FICCIÓN (ID 6)
('Los Servidores Silenciosos', 95, 1, 6, 'Iñaki H.', 'La humanidad descubre que sus servidores han tomado conciencia, pero no quieren ser notados.', '["Manuel J.", "Reyes D."]', 'http://trailer.servidores.com', 'Code Laughs', 'Inglés', 1),
('El Protocolo Olvidado', 118, 1, 6, 'Javier C.', 'Una misión al espacio para recuperar un protocolo de comunicación perdido.', '["Reyes D.", "Kary H."]', 'http://trailer.protocolo.com', 'HueteDevs', 'Castellano', 0),
('Nexus 7', 102, 1, 6, 'Kary H.', 'Una distopía donde la única forma de comunicación es a través de un chat encriptado.', '["Javier C."]', 'https://www.google.com/search?q=http://trailer.nexus.com', 'Proyecto Cero', 'Inglés', 1),

-- ROMANCE (ID 7)
('El Hilo de la Vida', 110, 1, 7, 'Reyes D.', 'Una historia de amor entre dos ingenieros separados por la distancia y un latency crítico.', '["Kary H.", "Iñaki H."]', 'http://trailer.hilo.com', 'AsturTech', 'Castellano', 0),
('Cifrado de un Corazón', 108, 1, 7, 'Javier C.', 'Un experto en seguridad debe descifrar los sentimientos de su colega.', '["Kary H.", "Reyes D."]', 'http://trailer.cifrado.com', 'Proyecto Cero', 'Inglés', 1),

-- DOCUMENTAL (ID 8)
('Bitácora de un Bug', 85, 1, 8, 'Javier C.', 'Un seguimiento semana a semana de un bug crítico desde su nacimiento hasta su resolución.', '["Equipo Dev"]', 'http://trailer.bitacora.com', 'Documental Dev', 'Castellano', 0),
('Crónica del Deployment', 98, 1, 8, 'Iñaki H.', 'La historia real y dramática de un solo despliegue de software.', '["Equipo Dev"]', 'http://trailer.cronica.com', 'Documental Dev', 'Inglés', 1),

-- TERROR (ID 9)
('La Venganza del Puntero Nulo', 130, 0, 9, 'Iñaki H.', 'Una pesadilla de programación donde un puntero nulo busca venganza en cada lenguaje.', '["Kary H."]', 'http://trailer.nulo.com', 'FastAPI Prod.', 'Castellano', 0),
('El Despertar del Legacy', 128, 0, 9, 'Kary H.', 'Un código antiguo y sin documentar cobra vida en la noche.', '["Manuel J."]', 'http://trailer.legacy.com', 'Cruz Roja Films', 'Inglés', 1),
('La Función Recursiva', 112, 0, 9, 'Javier C.', 'Una función sin condición de parada atormenta a un desarrollador en sus sueños.', '["Reyes D."]', 'https://www.google.com/search?q=http://trailer.recursivo.com', 'PP Studios', 'Castellano', 0),

-- HISTORICAS (ID 10)
('Los Foros de la Red', 115, 1, 10, 'Manuel J.', 'Un recuento de las primeras comunidades de software libre en internet.', '["Javier C.", "Kary H."]', 'https://www.google.com/search?q=http://trailer.historica.com', 'Software Libre Films', 'Castellano', 0),
('El Inicio del Kernel', 150, 1, 10, 'Iñaki H.', 'Un drama histórico sobre la creación del primer núcleo monolítico.', '["Javier C.", "Reyes D."]', 'https://www.google.com/search?q=http://trailer.kernel.com', 'HueteDevs', 'Inglés', 1),

-- CLASICO (ID 11)
('El Proyecto Pascal (1985)', 140, 1, 11, 'Reyes D.', 'Un clásico de culto sobre los inicios de la programación estructurada.', '["Iñaki H.", "Reyes D."]', 'https://www.google.com/search?q=http://trailer.clasico.com', 'AsturTech', 'Inglés', 0),
('El Primer Byte', 95, 1, 11, 'Manuel J.', 'La historia de la primera máquina de Turing y su impacto.', '["Kary H.", "Manuel J."]', 'https://www.google.com/search?q=http://trailer.byte.com', 'Adecco Cinema', 'Castellano', 0),

-- ANIMACIÓN (ID 12)
('Aventuras en el Heap', 75, 1, 12, 'Manuel J. Marín', 'Una colorida exploración animada sobre la gestión de memoria.', '["Pepe Coder"]', 'http://trailer.heap.com', 'Animaciones Dev', 'Castellano', 0),
('La Leyenda del Binario', 78, 1, 12, 'Kary H.', 'Una aventura animada para niños sobre los secretos de los 0s y 1s.', '["Pepe Coder"]', 'http://trailer.binario.com', 'Animaciones Dev', 'Inglés', 1);

-- Volver a habilitar las claves foráneas
PRAGMA foreign_keys = ON;