<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8" />
  <p align="center">
  <img src="banner_adecco.png" alt="HueteDevs banner" width="750" />
  </p>
    <title>🎥 Cartelera de Cine en Python (Parte 1)</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="Proyecto Cartelera de Cine en Python: descripción funcional, arquitectura, entidades y modelo de datos." />
    <style>
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background: #f5f7fb;            /* Fondo claro corporativo */
            color: #1f2933;                 /* Texto gris oscuro legible */
        }
        header {
            background: linear-gradient(135deg, #0d47a1, #1565c0); /* Azul corporativo */
            padding: 2.5rem 1.5rem;
            text-align: center;
            border-bottom: 3px solid #0056b3;                       /* Azul más intenso */
            color: #ffffff;
        }
        header h1 {
            margin: 0;
            font-size: 2.2rem;
        }
        header p {
            margin: 0.5rem 0 0;
            font-size: 1rem;
            color: #e3f2fd;
        }
        main {
            max-width: 980px;
            margin: 0 auto;
            padding: 2rem 1.5rem 3rem;
        }
        h2, h3, h4 {
            color: #0056b3;              /* Azul empresarial */
            margin-top: 2rem;
        }
        h2 {
            border-bottom: 1px solid #d0d7e2;
            padding-bottom: 0.3rem;
        }
        h3 {
            margin-top: 1.5rem;
        }
        h4 {
            margin-top: 1rem;
        }
        p {
            margin: 0.5rem 0;
        }
        ul {
            margin: 0.3rem 0 0.8rem 1.2rem;
        }
        li {
            margin-bottom: 0.2rem;
        }
        .tag {
            display: inline-block;
            background: #e8f1ff;           /* Azul muy claro */
            color: #0056b3;
            border-radius: 999px;
            padding: 0.1rem 0.75rem;
            font-size: 0.8rem;
            border: 1px solid #b3c7f2;
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
        }
        .card {
            border-radius: 0.75rem;
            border: 1px solid #d0d7e2;
            background: #ffffff;           /* Tarjeta fondo blanco */
            padding: 1.25rem 1.25rem 1rem;
            margin-top: 1.5rem;
            box-shadow: 0 4px 10px rgba(15, 23, 42, 0.06);
        }
        .entity-header {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            gap: 0.5rem;
            align-items: baseline;
            margin-bottom: 0.7rem;
        }
        .entity-header h3 {
            margin: 0;
        }
        .entity-owner {
            font-size: 0.85rem;
            color: #6b7280;             /* Gris medio */
        }
        .section-label {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #6b7280;
            margin-bottom: 0.25rem;
        }
        .relations-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 0.75rem;
            font-size: 0.9rem;
        }
        .relations-table th,
        .relations-table td {
            border: 1px solid #d0d7e2;
            padding: 0.4rem 0.5rem;
            text-align: left;
        }
        .relations-table th {
            background: #e8f1ff;
            color: #0056b3;
        }
        code {
            font-family: "JetBrains Mono", "Fira Code", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            font-size: 0.9em;
            background: #f3f4f6;           /* Gris claro sobre fondo blanco */
            padding: 0.1rem 0.25rem;
            border-radius: 0.25rem;
            color: #111827;
        }
        pre { /* Estilo para bloques de código */
            background: #f3f4f6;
            padding: 1rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            font-size: 0.9em;
            line-height: 1.4;
        }
        pre code {
            background: none;
            padding: 0;
            border-radius: 0;
        }
        footer {
            text-align: center;
            padding: 1.5rem 1rem 2rem;
            font-size: 0.85rem;
            color: #6b7280;
            border-top: 1px solid #e5e7eb;
            background: #ffffff;
        }
        a {
            color: #0056b3;
        }
        a:hover {
            color: #1d4ed8;
        }
        .subtle {
            color: #6b7280;
            font-size: 0.9rem;
        }
        @media (max-width: 640px) {
            main {
                padding: 1.5rem 1rem 2.5rem;
            }
        }
    </style>
</head>
<body>
<header role="banner">
    <h1>🎥 Cartelera de Cine en Python</h1>
    <p>La magia del cine… programada en Python 🐍🍿</p>
</header>

<main role="main">

    <section id="intro" aria-labelledby="intro-heading">
        <h2 id="intro-heading" style="display: none;">Introducción al Proyecto</h2>
        <p>
            Bienvenido al repositorio oficial de <strong>Cartelera de Cine</strong>, una aplicación desarrollada en 
            <strong>Python</strong> cuyo objetivo es gestionar de forma eficiente la cartelera digital de un cine.
            Este proyecto forma parte del aprendizaje del curso <strong>Python + Inteligencia Artificial</strong>, 
            combinando conceptos de programación estructurada, POO, bases de datos, APIs y arquitectura web moderna.
        </p>
    </section>

    <section id="finalidad" aria-labelledby="finalidad-heading">
        <h2 id="finalidad-heading">🎯 Finalidad del Proyecto</h2>
        <p>El propósito de este proyecto es diseñar un sistema backend capaz de:</p>
        <ul>
            <li>📌 Mostrar información de <strong>películas</strong> disponibles en cartelera.</li>
            <li>🕒 Gestionar <strong>horarios</strong> y <strong>salas</strong>.</li>
            <li>🎫 Administrar <strong>ventas de entradas</strong> y <strong>precios</strong>.</li>
            <li>🎭 Organizar <strong>géneros</strong> y <strong>clasificaciones</strong>.</li>
            <li>👥 Gestionar <strong>usuarios, autenticación</strong> y <strong>socios</strong>.</li>
            <li>📚 Aplicar <strong>POO</strong>, estructuras de datos y buenas prácticas de desarrollo.</li>
            <li>🚀 Integrar tecnologías modernas como <strong>FastAPI</strong> y <strong>SQLAlchemy</strong>.</li>
        </ul>
    </section>

    <section id="equipo" aria-labelledby="equipo-heading">
        <h2 id="equipo-heading">👥 Equipo de Desarrollo</h2>
        <p>El proyecto ha sido diseñado y desarrollado por el siguiente equipo:</p>
        <ul>
            <li><strong>Javier Cachón Garrido</strong></li>
            <li><strong>Kary Haro Pérez</strong></li>
            <li><strong>Manuel Jesús Marín García</strong></li>
            <li><strong>Reyes Delestal Barrios</strong></li>
            <li><strong>Iñaki Huete Montes</strong></li>
        </ul>
    </section>

    <section id="tecnologias" aria-labelledby="tecnologias-heading">
        <h2 id="tecnologias-heading">🛠️ Tecnologías utilizadas</h2>
        <div>
            <span class="tag">Python 3</span>
            <span class="tag">SQLAlchemy (ORM)</span>
            <span class="tag">SQLite</span>
            <span class="tag">Programación Orientada a Objetos</span>
            <span class="tag">FastAPI</span>
            <span class="tag">Jinja2</span>
            <span class="tag">Bootstrap 4/5</span>
            <span class="tag">HTML5</span>
            <span class="tag">CSS3</span>
            <span class="tag">JavaScript</span>
            <span class="tag">SQL</span>
            <span class="tag">Visual Studio Code</span>
        </div>
    </section>

    <section id="arquitectura" aria-labelledby="arquitectura-heading">
        <h2 id="arquitectura-heading">🏛️ Arquitectura del Sistema</h2>
        <p>
            El proyecto está basado en una arquitectura modular que separa claramente las 
            <strong>entidades de dominio</strong>, la <strong>lógica de negocio</strong> y los 
            <strong>servicios</strong> (endpoints, vistas, etc.).
        </p>
        <p>
            A continuación se detallan todas las entidades con sus campos, sus responsabilidades 
            dentro del sistema y las <strong>relaciones entre ellas</strong>, así como cómo se pueden 
            modelar en la base de datos y, cuando procede, en el ORM.
        </p>
    </section>

    <section id="estructura" aria-labelledby="estructura-heading">
        <h2 id="estructura-heading">📁 Estructura del Proyecto</h2>
        <p>A continuación se detalla la estructura recomendada del proyecto Cartelera de Cine en Python:</p>
        <pre><code>.
├── app/
│   ├── main.py
│   ├── models/
│   │   ├── pelicula.py      # Entidad Pelicula
│   │   ├── genero.py        # Entidad Genero
│   │   ├── sala.py          # Entidad Sala
│   │   ├── horario.py       # Entidad Horario
│   │   ├── venta.py         # Entidad Venta
│   │   ├── socio.py         # Entidad Socio
│   │   └── login.py         # Entidad Login / Usuario
│   ├── routes/
│   │   ├── peliculas.py     # Rutas CRUD Peliculas
│   │   ├── generos.py       # Rutas CRUD Generos
│   │   ├── salas.py         # Rutas CRUD Salas
│   │   ├── horarios.py      # Rutas CRUD Horarios
│   │   ├── ventas.py        # Rutas CRUD Ventas
│   │   ├── socios.py        # Rutas CRUD Socios
│   │   └── login.py         # Rutas de autenticación / login
│   ├── database/
│   │   ├── db.py            # Motor de conexión SQLAlchemy
│   │   ├── db.sql               # Schema y seed de la base de datos
│   │   └── cartelera_cine.db    # Base de datos SQLite
│   ├── templates/
│   │   ├── base.html        # Layout común
│   │   ├── peliculas/       # Vistas HTML de peliculas
│   │   ├── generos/         # Vistas HTML de generos
│   │   ├── salas/           # Vistas HTML de salas
│   │   ├── horarios/        # Vistas HTML de horarios
│   │   ├── ventas/          # Vistas HTML de ventas
│   │   ├── socios/          # Vistas HTML de socios
│   │   └── login/           # Vistas HTML de login/autenticación
│   └── static/
│       ├── css/
│       ├── js/
│       └── img/
├── requirements.txt
├── README.html
└── run.py</code></pre>
    </section>

    <section id="entidades" aria-labelledby="entidades-heading">
        <h2 id="entidades-heading">🎬 Entidades del Sistema</h2>

        <article id="pelicula" class="card" aria-labelledby="pelicula-h3">
            <div class="entity-header">
                <h3 id="pelicula-h3">🎞️ Pelicula</h3>
                <span class="entity-owner">Responsable: JAVIER CACHÓN</span>
            </div>
            <p>Representa una película disponible (o no) en la cartelera.</p>

            <h4>Campos</h4>
            <ul>
                <li><code>id</code>: int — <strong>PK</strong> (clave primaria)</li>
                <li><code>titulo</code>: string</li>
                <li><code>genero_id</code>: int — <strong>FK → generos.id</strong></li>
                <li><code>duracion</code>: int</li>
                <li><code>director</code>: string</li>
                <li><code>descripcion</code>: string</li>
                <li><code>trailer</code>: string (URL)</li>
                <li><code>productora</code>: string</li>
                <li><code>idioma</code>: string</li>
                <li><code>VOSE</code>: boolean</li>
                <li><code>actores</code>: lista (strings)</li>
                <li><code>disponible</code>: boolean</li>
            </ul>

            <h4>Relaciones (modelo y ORM)</h4>
            <ul>
                <li>
                    <strong>Pelicula ↔ Género</strong><br />
                    A nivel de base de datos:
                    <ul>
                        <li>La FK está en <code>peliculas.genero_id</code> apuntando a <code>generos.id</code>.</li>
                    </ul>
                    A nivel lógico/ORM:
                    <ul>
                        <li>Cada <strong>Pelicula</strong> está asociada a un único <strong>Genero</strong> (lado N:1).</li>
                        <li>Cada <strong>Genero</strong> puede exponer una colección de <strong>peliculas</strong> (lado 1:N).</li>
                    </ul>
                    Navegación típica en ORM:
                    <ul>
                        <li>Desde una película: <code>pelicula.genero</code></li>
                        <li>Desde un género (si se implementa la colección): <code>genero.peliculas</code></li>
                    </ul>
                </li>
                <li>
                    <strong>Pelicula ↔ Horario</strong><br />
                    A nivel de base de datos (modelo relacional):
                    <ul>
                        <li>La FK está en <code>horarios.pelicula_id</code> apuntando a <code>peliculas.id</code>.</li>
                        <li>Conceptualmente: una <strong>Pelicula</strong> puede tener muchos <strong>Horarios</strong> (1:N).</li>
                    </ul>
                    Navegación ORM implementada:
                    <ul>
                        <li>Se navega desde <strong>Horario</strong> hacia <strong>Pelicula</strong> mediante <code>horario.pelicula</code>.</li>
                        <li><strong>No</strong> se implementa en el ORM la colección <code>pelicula.horarios</code> (no hay atributo en la entidad Pelicula).</li>
                    </ul>
                    Es decir, la relación es 1:N en la base de datos, pero la navegación en código se ha definido solo en el sentido <strong>Horario → Pelicula</strong>.
                </li>
            </ul>

            <h4>Servicios — Películas 🎬</h4>
            <ul>
                <li>Añadir película</li>
                <li>Ver películas disponibles</li>
                <li>Ver detalle de una película</li>
                <li>Editar película</li>
                <li>Eliminar o desactivar película</li>
            </ul>

            <h4>Extra (futuro)</h4>
            <ul>
                <li>Filtrar por género, duración, clasificación, etc.</li>
                <li>Búsquedas avanzadas (título, director, actor, etc.)</li>
                <li>Exportar catálogo a CSV/JSON</li>
            </ul>
        </article>

        <article id="sala" class="card" aria-labelledby="sala-h3">
            <div class="entity-header">
                <h3 id="sala-h3">🏟️ Sala</h3>
                <span class="entity-owner">Responsable: REYES</span>
            </div>
            <p>Representa una sala física del cine.</p>

            <h4>Campos</h4>
            <ul>
                <li><code>id</code>: int — <strong>PK</strong></li>
                <li><code>numero</code>: int</li>
                <li><code>capacidad</code>: int (número de butacas)</li>
                <li><code>tipo</code>: enum (normal, 3D, IMAX, premium)</li>
                <li><code>precio_base</code>: float</li>
            </ul>

            <h4>Relaciones (modelo y ORM)</h4>
            <ul>
                <li>
                    <strong>Sala ↔ Horario</strong><br />
                    A nivel de base de datos:
                    <ul>
                        <li>La FK está en <code>horarios.sala_id</code> apuntando a <code>salas.id</code>.</li>
                    </ul>
                    A nivel lógico/ORM:
                    <ul>
                        <li>Una <strong>Sala</strong> puede tener muchos <strong>Horarios</strong> (1:N).</li>
                        <li>Un <strong>Horario</strong> se proyecta en una sola <strong>Sala</strong> (N:1).</li>
                    </ul>
                    Dependiendo de la configuración del ORM se puede navegar:
                    <ul>
                        <li>Desde el horario: <code>horario.sala</code></li>
                        <li>Desde la sala (si se define colección): <code>sala.horarios</code></li>
                    </ul>
                </li>
            </ul>

            <h4>Servicios — Salas 🏟️</h4>
            <ul>
                <li>Añadir sala</li>
                <li>Listar salas</li>
                <li>Editar sala (capacidad, tipo, precio_base)</li>
                <li>Activar/desactivar sala (si se implementa este campo)</li>
            </ul>

            <h4>Extra (futuro)</h4>
            <ul>
                <li>Gestión de mantenimiento (salas fuera de servicio)</li>
                <li>Suplementos por tipo de sala (3D, IMAX, etc.)</li>
            </ul>
        </article>

        <article id="horario" class="card" aria-labelledby="horario-h3">
            <div class="entity-header">
                <h3 id="horario-h3">🕒 Horario</h3>
                <span class="entity-owner">Responsable: MANUEL</span>
            </div>
            <p>Representa una sesión concreta de una película en una sala y hora determinada.</p>

            <h4>Campos</h4>
            <ul>
                <li><code>id</code>: int — <strong>PK</strong></li>
                <li><code>pelicula_id</code>: int — <strong>FK → peliculas.id</strong></li>
                <li><code>sala_id</code>: int — <strong>FK → salas.id</strong></li>
                <li><code>hora</code>: datetime/string</li>
                <li><code>disponible</code>: boolean</li>
            </ul>

            <h4>Relaciones (modelo y ORM)</h4>
            <ul>
                <li>
                    <strong>Horario ↔ Pelicula</strong><br />
                    Modelo relacional:
                    <ul>
                        <li>Cada <strong>Horario</strong> referencia una única <strong>Pelicula</strong> mediante <code>pelicula_id</code>.</li>
                        <li>Una <strong>Pelicula</strong> puede tener muchos <strong>Horarios</strong> asociados (1:N, a nivel de tabla).</li>
                    </ul>
                    Navegación ORM implementada:
                    <ul>
                        <li>Desde <strong>Horario</strong> hacia <strong>Pelicula</strong>: <code>horario.pelicula</code>.</li>
                        <li>No se ha definido en el ORM la colección inversa <code>pelicula.horarios</code>; la navegación se mantiene intencionadamente unidireccional.</li>
                    </ul>
                </li>
                <li>
                    <strong>Horario ↔ Sala</strong><br />
                    <ul>
                        <li>Cada <strong>Horario</strong> referencia una única <strong>Sala</strong> mediante <code>sala_id</code>.</li>
                        <li>Una <strong>Sala</strong> puede tener múltiples <strong>Horarios</strong> (1:N, a nivel de modelo lógico).</li>
                    </ul>
                </li>
                <li>
                    <strong>Horario ↔ Venta</strong><br />
                    A nivel de base de datos:
                    <ul>
                        <li>La FK está en <code>ventas.horario_id</code> apuntando a <code>horarios.id</code>.</li>
                    </ul>
                    A nivel lógico/ORM:
                    <ul>
                        <li>Un <strong>Horario</strong> puede tener muchas <strong>Ventas</strong> (1:N).</li>
                        <li>Cada <strong>Venta</strong> corresponde a un único <strong>Horario</strong> (N:1).</li>
                    </ul>
                </li>
            </ul>

            <h4>Servicios — Horarios</h4>
            <ul>
                <li>Crear horario para una película en una sala</li>
                <li>Listar horarios por película</li>
                <li>Listar horarios por fecha</li>
                <li>Listar horarios por sala</li>
                <li>Editar horario (cambiar hora, sala, película)</li>
                <li>Cancelar horario (marcar como no disponible)</li>
            </ul>

            <h4>Extra (futuro)</h4>
            <ul>
                <li>Comprobar solapamientos de horarios en la misma sala</li>
                <li>Mostrar solo sesiones futuras</li>
                <li>Control de aforo basado en ventas</li>
            </ul>
        </article>

        <article id="venta" class="card" aria-labelledby="venta-h3">
            <div class="entity-header">
                <h3 id="venta-h3">💳 Venta</h3>
                <span class="entity-owner">Responsable: IÑAKI</span>
            </div>
            <p>Representa la compra de entradas para un determinado horario.</p>

            <h4>Campos</h4>
            <ul>
                <li><code>id</code>: int — <strong>PK</strong></li>
                <li><code>horario_id</code>: int — <strong>FK → horarios.id</strong></li>
                <li><code>precio_total</code>: float</li>
                <li><code>cantidad</code>: int (número de entradas)</li>
                <li><code>metodo_pago</code>: enum (efectivo, tarjeta, cripto…)</li>
                <li><code>socio_id</code>: int (opcional) — <strong>FK → socios.id</strong></li>
            </ul>

            <h4>Relaciones (modelo y ORM)</h4>
            <ul>
                <li>
                    <strong>Venta ↔ Horario</strong><br />
                    <ul>
                        <li>Cada <strong>Venta</strong> está asociada a un único <strong>Horario</strong> mediante <code>horario_id</code>.</li>
                        <li>Un <strong>Horario</strong> puede tener múltiples <strong>Ventas</strong> asociadas.</li>
                    </ul>
                </li>
                <li>
                    <strong>Venta ↔ Socio</strong> (opcional / futuro)<br />
                    <ul>
                        <li>Cada <strong>Venta</strong> puede opcionalmente estar asociada a un <strong>Socio</strong> mediante <code>socio_id</code>.</li>
                        <li>Un <strong>Socio</strong> puede acumular muchas <strong>Ventas</strong> a su nombre.</li>
                    </ul>
                </li>
            </ul>

            <h4>Servicios — Ventas 💳</h4>
            <ul>
                <li>Registrar venta</li>
                <li>Calcular precio total</li>
                <li>Listar ventas (por día, película, horario…)</li>
                <li>Consultar recaudación en un rango de fechas</li>
            </ul>

            <h4>Extra (futuro)</h4>
            <ul>
                <li>Cupones de descuento</li>
                <li>Asignar venta a <code>usuario</code> o <code>socio</code></li>
                <li>Generar ticket (PDF / código QR)</li>
            </ul>
        </article>

        <article id="genero" class="card" aria-labelledby="genero-h3">
            <div class="entity-header">
                <h3 id="genero-h3">🏷️ Género</h3>
                <span class="entity-owner">Responsable: KARY</span>
            </div>
            <p>Catálogo de géneros cinematográficos asociados a las películas.</p>

            <h4>Campos</h4>
            <ul>
                <li><code>id</code>: int — <strong>PK</strong></li>
                <li><code>nombre</code>: string</li>
                <li><code>descripcion</code>: string</li>
            </ul>

            <h4>Relaciones (modelo y ORM)</h4>
            <ul>
                <li>
                    <strong>Género ↔ Pelicula</strong><br />
                    <ul>
                        <li>Cada <strong>Pelicula</strong> referencia un <strong>Genero</strong> mediante <code>genero_id</code>.</li>
                        <li>Cada <strong>Genero</strong> puede agrupar muchas <strong>Peliculas</strong> asociadas.</li>
                    </ul>
                </li>
            </ul>

            <h4>Servicios — Géneros 🏷️</h4>
            <ul>
                <li>Crear género</li>
                <li>Listar géneros</li>
                <li>Editar género</li>
                <li>Eliminar género (según política de negocio)</li>
            </ul>

            <h4>Extra (futuro)</h4>
            <ul>
                <li>Permitir múltiples géneros por película (tabla intermedia)</li>
                <li>Estadísticas por género (películas, ventas, horarios, etc.)</li>
            </ul>
        </article>

        <article id="login" class="card" aria-labelledby="login-h3">
            <div class="entity-header">
                <h3 id="login-h3">🔐 Login / Autenticación</h3>
                <span class="entity-owner">Responsable: JAVIER CACHÓN</span>
            </div>
            <p>Sistema central de autenticación y autorización de usuarios (clientes y administradores).</p>

            <h4>Campos</h4>
            <ul>
                <li><code>id</code>: int — <strong>PK</strong></li>
                <li><code>username</code>: string (único)</li>
                <li><code>email</code>: string (único)</li>
                <li><code>password_hash</code>: string</li>
                <li><code>rol</code>: enum (usuario, administrador)</li>
                <li><code>activo</code>: boolean</li>
                <li><code>bloqueado</code>: boolean</li>
                <li><code>creado_en</code>: datetime</li>
                <li><code>actualizado_en</code>: datetime</li>
            </ul>

            <h4>Relaciones (modelo y ORM)</h4>
            <ul>
                <li>
                    <strong>Login ↔ Socio</strong><br />
                    <p class="subtle">Relación modelada típicamente como <strong>Optional One-to-One</strong>: la FK opcional reside en la tabla <code>socios</code>.</p>
                    <ul>
                        <li>Un <strong>Socio</strong> puede vincularse a un único <strong>Login</strong> mediante <code>login_id</code>.</li>
                        <li>Un <strong>Login</strong> puede estar vinculado, como máximo, a un <strong>Socio</strong>.</li>
                    </ul>
                    <p class="subtle">Esta relación permite: socios sin login (alta en taquilla) y logins sin socio (usuario registrado sin programa de puntos).</p>
                </li>
            </ul>

            <h4>Servicios — Login 🔐</h4>
            <ul>
                <li>Registrar usuario</li>
                <li>Iniciar sesión</li>
                <li>Cerrar sesión</li>
                <li>Cambiar contraseña</li>
                <li>Recuperar contraseña</li>
                <li>Bloquear / desbloquear cuenta</li>
                <li>Editar email o username</li>
                <li>Listar logins activos / bloqueados</li>
            </ul>

            <h4>Extra (futuro)</h4>
            <ul>
                <li>Doble factor de autenticación (2FA)</li>
                <li>Historial de accesos (IP, fecha, dispositivo)</li>
                <li>Expiración periódica de contraseña</li>
            </ul>
        </article>

        <article id="socio" class="card" aria-labelledby="socio-h3">
            <div class="entity-header">
                <h3 id="socio-h3">👥 Socio / Fidelización</h3>
                <span class="entity-owner">Responsable: JAVIER CACHÓN</span>
            </div>
            <p>Sistema de clientes registrados con ventajas y programa de puntos.</p>

            <h4>Campos</h4>
            <ul>
                <li><code>id</code>: int — <strong>PK</strong></li>
                <li><code>numero_socio</code>: string</li>
                <li><code>login_id</code>: int — (opcional) <strong>FK → logins.id</strong></li>
                <li><code>email</code>: string (único)</li>
                <li><code>nivel</code>: enum (Basic, Silver, Gold, VIP)</li>
                <li><code>puntos</code>: int</li>
                <li><code>fecha_alta</code>: datetime</li>
                <li><code>activo</code>: boolean</li>
            </ul>

            <h4>Relaciones (modelo y ORM)</h4>
            <ul>
                <li>
                    <strong>Socio ↔ Login</strong><br />
                    <ul>
                        <li>Cada <strong>Socio</strong> puede estar vinculado a un único <strong>Login</strong> (cuenta de acceso web).</li>
                        <li>Cada <strong>Login</strong> puede vincularse, como máximo, a un <strong>Socio</strong>.</li>
                    </ul>
                </li>
                <li>
                    <strong>Socio ↔ Venta</strong> (opcional / futuro)<br />
                    <ul>
                        <li>Un <strong>Socio</strong> puede tener asociadas múltiples <strong>Ventas</strong> (historial de compras).</li>
                        <li>Cada <strong>Venta</strong> puede referenciar al <strong>Socio</strong> que la realizó.</li>
                    </ul>
                </li>
            </ul>

            <h4>Servicios — Socios 👥</h4>
            <ul>
                <li>Alta de socio</li>
                <li>Vincular socio con login</li>
                <li>Consultar perfil de socio</li>
                <li>Consultar puntos</li>
                <li>Upgrade/downgrade de nivel</li>
                <li>Sumar puntos (compras, promociones)</li>
                <li>Restar puntos (canjes, devoluciones)</li>
                <li>Baja de socio (marcar como inactivo)</li>
            </ul>

            <h4>Extra (futuro)</h4>
            <ul>
                <li>Historial de puntos</li>
                <li>Ventajas por nivel (descuentos, preestrenos, etc.)</li>
                <li>Envío de promociones por email</li>
                <li>Tarjeta digital QR</li>
            </ul>
        </article>
    </section>

    <section id="relaciones" aria-labelledby="relaciones-heading">
        <h2 id="relaciones-heading">🔗 Modelo de Datos y Relaciones (Cardinalidad)</h2>
        <p>
            A continuación se resumen las relaciones entre las entidades, indicando 
            claves foráneas, dirección, cardinalidad y, cuando aplica, cómo se navega 
            en el ORM.
        </p>

        <h3>2.1. Pelicula ↔ Género</h3>
        <ul>
            <li><strong>FK:</strong> <code>peliculas.genero_id → generos.id</code></li>
            <li>
                <strong>Cardinalidad (modelo lógico):</strong>
                <ul>
                    <li>Una <strong>Pelicula</strong> pertenece a un único <strong>Genero</strong>.</li>
                    <li>Un <strong>Genero</strong> puede tener muchas <strong>Peliculas</strong>.</li>
                </ul>
            </li>
            <li>
                <strong>Tipo:</strong>
                <ul>
                    <li>Pelicula → Genero: <strong>ManyToOne (N:1)</strong></li>
                    <li>Genero → Pelicula: <strong>OneToMany (1:N)</strong></li>
                </ul>
            </li>
            <li><strong>Navegación ORM típica:</strong> <code>pelicula.genero</code> y, si se define, <code>genero.peliculas</code></li>
        </ul>

        <h3>2.2. Horario ↔ Pelicula</h3>
        <ul>
            <li><strong>FK:</strong> <code>horarios.pelicula_id → peliculas.id</code></li>
            <li>
                <strong>Cardinalidad (modelo lógico):</strong>
                <ul>
                    <li>Un <strong>Horario</strong> corresponde a una <strong>Pelicula</strong> concreta.</li>
                    <li>Una <strong>Pelicula</strong> puede tener muchos <strong>Horarios</strong> (1:N).</li>
                </ul>
            </li>
            <li>
                <strong>Tipo:</strong>
                <ul>
                    <li>Horario → Pelicula: <strong>ManyToOne (N:1)</strong></li>
                    <li>Pelicula → Horario: <strong>OneToMany (1:N)</strong> (a nivel de diseño de datos)</li>
                </ul>
            </li>
            <li><strong>Navegación ORM implementada:</strong> solo <code>horario.pelicula</code> (no se implementa <code>pelicula.horarios</code> en el modelo actual).</li>
        </ul>

        <h3>2.3. Horario ↔ Sala</h3>
        <ul>
            <li><strong>FK:</strong> <code>horarios.sala_id → salas.id</code></li>
            <li>
                <strong>Cardinalidad:</strong>
                <ul>
                    <li>Un <strong>Horario</strong> se proyecta en una sola <strong>Sala</strong>.</li>
                    <li>Una <strong>Sala</strong> puede tener muchos <strong>Horarios</strong>.</li>
                </ul>
            </li>
            <li>
                <strong>Tipo:</strong>
                <ul>
                    <li>Horario → Sala: <strong>ManyToOne (N:1)</strong></li>
                    <li>Sala → Horario: <strong>OneToMany (1:N)</strong></li>
                </ul>
            </li>
        </ul>

        <h3>2.4. Venta ↔ Horario</h3>
        <ul>
            <li><strong>FK:</strong> <code>ventas.horario_id → horarios.id</code></li>
            <li>
                <strong>Cardinalidad:</strong>
                <ul>
                    <li>Una <strong>Venta</strong> está asociada a un solo <strong>Horario</strong>.</li>
                    <li>Un <strong>Horario</strong> puede tener muchas <strong>Ventas</strong>.</li>
                </ul>
            </li>
            <li>
                <strong>Tipo:</strong>
                <ul>
                    <li>Venta → Horario: <strong>ManyToOne (N:1)</strong></li>
                    <li>Horario → Venta: <strong>OneToMany (1:N)</strong></li>
                </ul>
            </li>
        </ul>

        <h3>2.5. Socio ↔ Login</h3>
        <ul>
            <li><strong>FK:</strong> <code>socios.login_id → logins.id</code> (opcional)</li>
            <li>
                <strong>Cardinalidad:</strong>
                <ul>
                    <li>Un <strong>Socio</strong> puede estar vinculado a un solo <strong>Login</strong>.</li>
                    <li>Un <strong>Login</strong> puede estar vinculado, como máximo, a un <strong>Socio</strong>.</li>
                </ul>
            </li>
            <li>
                <strong>Tipo:</strong>
                <ul>
                    <li>Socio → Login: <strong>Optional OneToOne (0..1 : 1)</strong></li>
                    <li>Login → Socio: <strong>Optional OneToOne (1 : 0..1)</strong></li>
                </ul>
            </li>
        </ul>

        <h3>2.6. Venta ↔ Socio (futuro)</h3>
        <p class="subtle">(Opcional, si se implementa en el modelo)</p>
        <ul>
            <li><strong>FK:</strong> <code>ventas.socio_id → socios.id</code></li>
            <li>
                <strong>Cardinalidad:</strong>
                <ul>
                    <li>Una <strong>Venta</strong> puede estar asociada a un <strong>Socio</strong>.</li>
                    <li>Un <strong>Socio</strong> puede tener muchas <strong>Ventas</strong> a lo largo del tiempo.</li>
                </ul>
            </li>
            <li>
                <strong>Tipo:</strong>
                <ul>
                    <li>Venta → Socio: <strong>ManyToOne (N:1)</strong></li>
                    <li>Socio → Venta: <strong>OneToMany (1:N)</strong></li>
                </ul>
            </li>
        </ul>

        <h3>Resumen visual simplificado</h3>
        <pre><code>generos (1) ────&lt; (N) peliculas

peliculas (1) ────&lt; (N) horarios &gt;──── (1) salas

horarios (1) ────&lt; (N) ventas

logins (1) ────(0..1) socios

socios (1) ────&lt; (N) ventas    [opcional si se añade ventas.socio_id]
        </code></pre>
        

<section id="instalacion" aria-labelledby="instalacion-heading">
        <h2 id="instalacion-heading">📦 Instalación de dependencias</h2>
        <p>
            Antes de ejecutar el proyecto se recomienda utilizar un entorno virtual de Python
            y cargar todas las dependencias desde <code>requirements.txt</code>.
        </p>

        <h3>1. Clonar el repositorio</h3>
        <pre><code>git clone https://github.com/HueteDevs/Proyecto_Adecco
cd Proyecto_Adecco
        </code></pre>

        <h3>2. Crear y activar entorno virtual (opcional, pero recomendado)</h3>
        <pre><code># Linux y MacOS
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
        </code></pre>

        <h3>3. Instalar dependencias del proyecto</h3>
        <p>Con el entorno virtual activado:</p>
        <pre><code>pip install -r requirements.txt
        </code></pre>

        <p class="subtle">
            Entre las dependencias típicas se incluyen paquetes como
            <code>fastapi</code>, <code>uvicorn</code>, <code>sqlalchemy</code>,
            <code>pydantic</code> <code>jinja2</code> y el driver de <code>sqlite</code> ya incorporado
            en la librería estándar de Python.
        </p>
    </section>

    <section id="ejecucion" aria-labelledby="ejecucion-heading">
        <h2 id="ejecucion-heading">▶️ Ejecución paso a paso</h2>
        <p>
            Una vez instaladas las dependencias y creada la base de datos, la ejecución
            del proyecto se realiza normalmente a través de <strong>FastAPI</strong>
            y un servidor ASGI como <strong>Uvicorn</strong>.
        </p>

        <h3>1. Comprobar variables de entorno (opcional)</h3>
        <p>
            Si se utilizan variables de entorno (por ejemplo, para el modo debug o la URL
            de la base de datos), configúralas antes de lanzar la aplicación.
        </p>

        <h3>2. Ejecutar el servidor de desarrollo</h3>
        <pre><code># Desde la raíz del proyecto
uvicorn app.main:app --reload
        </code></pre>

        <p>
            Por defecto, la API estará disponible en:
            <code>http://127.0.0.1:8000</code> y la documentación interactiva en:
        </p>
        <ul>
            <li><code>http://127.0.0.1:8000/docs</code> (Swagger UI)</li>
            <li><code>http://127.0.0.1:8000/redoc</code> (ReDoc)</li>
        </ul>

        <h3>3. Ejecución desde <code>run.py</code> (alternativa)</h3>
        <pre><code>python run.py
        </code></pre>
        <p class="subtle">
            Este script puede actuar como punto de entrada unificado para
            entornos de desarrollo o despliegue.
        </p>
    </section>

    <section id="scripts-bd" aria-labelledby="scripts-bd-heading">
        <h2 id="scripts-bd-heading">🗄️ Scripts de inicialización de la base de datos</h2>
        <p>
            La base de datos principal del proyecto es un fichero
            <strong>SQLite</strong> llamado <code>cartelera_cine.db</code>,
            ubicado en <code>app/database/</code>.
        </p>

        <h3>1. Módulos de base de datos</h3>
        <ul>
            <li><code>app/database/db.py</code> — configuración de la conexión SQLAlchemy.</li>
            <li><code>app/database/db.sql</code> — creación de tablas y carga inicial de datos (seed).</li>
        </ul>

        <h3>2. Crear o recrear la base de datos</h3>
        <p>Desde la raíz del proyecto:</p>
        <pre><code>python -m app.cartelera_cine.db
        </code></pre>

        <p>
            Este script se encarga de:
        </p>
        <ul>
            <li>Crear el fichero <code>cartelera_cine.db</code> si no existe.</li>
            <li>Generar las tablas correspondientes a las entidades:
                <code>peliculas</code>, <code>generos</code>, <code>salas</code>,
                <code>horarios</code>, <code>ventas</code>, <code>logins</code> y <code>socios</code>.
            </li>
            <li>Cargar datos de ejemplo (películas, horarios, etc.) para pruebas.</li>
        </ul>

        <h3>3. Regenerar la base de datos (entornos de desarrollo)</h3>
        <p class="subtle">
            En desarrollo es habitual borrar el fichero
            <code>cartelera_cine.db</code> y volver a ejecutar
            <code>python -m app.cartelera_cine.db</code> para partir de un estado limpio.
        </p>
    </section>

    <section id="fastapi-endpoints" aria-labelledby="fastapi-endpoints-heading">
        <h2 id="fastapi-endpoints-heading">🌐 Definición de endpoints con FastAPI</h2>
        <p>
            La API se estructura en módulos de rutas dentro del paquete
            <code>app/routes/</code>, separando por dominio funcional
            (películas, géneros, salas, horarios, ventas, socios y login).
        </p>

        <h3>1. Punto de entrada de la API: <code>app/main.py</code></h3>
        <pre><code>from fastapi import FastAPI
from app.routes import peliculas, generos, salas, horarios, ventas, socios, login

app = FastAPI(title="Cartelera de Cine en Python")

app.include_router(peliculas.router, prefix="/peliculas", tags=["Películas"])
app.include_router(generos.router,   prefix="/generos",   tags=["Géneros"])
app.include_router(salas.router,     prefix="/salas",     tags=["Salas"])
app.include_router(horarios.router,  prefix="/horarios",  tags=["Horarios"])
app.include_router(ventas.router,    prefix="/ventas",    tags=["Ventas"])
app.include_router(socios.router,    prefix="/socios",    tags=["Socios"])
app.include_router(login.router,     prefix="/auth",      tags=["Login"])
        </code></pre>

        <h3>2. Ejemplo de endpoints: <code>app/routes/peliculas.py</code></h3>
        <pre><code>from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.pelicula import PeliculaCreate, PeliculaRead
from app.services.peliculas import PeliculaService

router = APIRouter()

@router.get("/", response_model=List[PeliculaRead])
def listar_peliculas():
    return PeliculaService.listar()

@router.get("/{pelicula_id}", response_model=PeliculaRead)
def obtener_pelicula(pelicula_id: int):
    pelicula = PeliculaService.obtener(pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return pelicula

@router.post("/", response_model=PeliculaRead, status_code=201)
def crear_pelicula(datos: PeliculaCreate):
    return PeliculaService.crear(datos)

@router.delete("/{pelicula_id}", status_code=204)
def eliminar_pelicula(pelicula_id: int):
    PeliculaService.eliminar(pelicula_id)
        </code></pre>

        <h3>3. Endpoints habituales por módulo</h3>
        <ul>
            <li><strong>/peliculas</strong>: CRUD de películas y filtros por género, disponibilidad, etc.</li>
            <li><strong>/generos</strong>: mantenimiento del catálogo de géneros.</li>
            <li><strong>/salas</strong>: gestión de salas y capacidades.</li>
            <li><strong>/horarios</strong>: gestión de sesiones (película + sala + hora).</li>
            <li><strong>/ventas</strong>: registro de ventas y consultas de recaudación.</li>
            <li><strong>/socios</strong>: alta, baja y gestión de datos de socios.</li>
            <li><strong>/auth</strong>: registro, login, logout y gestión de credenciales.</li>
        </ul>

        <p class="subtle">
            Esta organización facilita el mantenimiento, la escalabilidad del proyecto y
            la integración posterior con un frontend (por ejemplo, una SPA o plantillas
            Jinja2).
        </p>
    </section>

    <section id="futuras-mejoras" aria-labelledby="futuras-mejoras-heading">
        <h2 id="futuras-mejoras-heading">🚀 Futuras Mejoras del Proyecto</h2>
        <ul>
            <li>Sistema completo de compra de entradas (frontend + backend).</li>
            <li>Diseño gráfico tipo cine (UI/UX más cinematográfica).</li>
            <li>Panel de administración web (gestión de contenidos y usuarios).</li>
            <li>Estadísticas avanzadas (ventas, ocupación, popularidad de películas).</li>
            <li>Machine Learning para recomendaciones personalizadas de películas.</li>
        </ul>
    </section>

    <section id="actualizaciones" aria-labelledby="actualizaciones-heading">
        <h2 id="actualizaciones-heading">📦 Próximas actualizaciones</h2>
        <p>Se incorporará documentación detallada y ejemplos adicionales sobre:</p>
        <ul>
            <li>Estructura de carpetas del proyecto.</li>
            <li>Instalación de dependencias en distintos entornos.</li>
            <li>Ejecución paso a paso con distintos perfiles (desarrollo / producción).</li>
            <li>Scripts de inicialización y migraciones de la base de datos.</li>
            <li>Definición avanzada de endpoints y seguridad en FastAPI.</li>
        </ul>
    </section>

</main>

<footer role="contentinfo">
    ✨ Proyecto en constante evolución. Cada aportación suma. Este repositorio seguirá creciendo con nuevas funcionalidades, mejoras y buenas prácticas de programación.
</footer>

</body>
</html>
