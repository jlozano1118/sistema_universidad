<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>README - Sistema de Gestión de Universidad</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
  <style>
    :root{--bg:#0f1724;--card:#0b1220;--muted:#94a3b8;--accent:#60a5fa;--glass: rgba(255,255,255,0.03)}
    body{font-family:Inter,system-ui,Segoe UI,Roboto,-apple-system,"Helvetica Neue",Arial;line-height:1.6;background:linear-gradient(180deg,#071028 0%, #07182a 100%);color:#e6eef8;padding:32px}
    .container{max-width:1000px;margin:0 auto}
    header h1{font-size:2rem;margin:0 0 8px}
    header p{color:var(--muted);margin:0 0 18px}
    .card{background:var(--card);border-radius:12px;padding:20px;margin-bottom:18px;box-shadow:0 6px 18px rgba(2,6,23,0.6)}
    table{width:100%;border-collapse:collapse;margin-top:12px}
    th,td{padding:10px;border-bottom:1px solid rgba(255,255,255,0.04);text-align:left}
    th{background:linear-gradient(90deg,rgba(255,255,255,0.02),transparent);font-weight:600}
    code{background:var(--glass);padding:4px 6px;border-radius:6px;color:#dff1ff}
    pre{background:#061021;padding:12px;border-radius:8px;overflow:auto}
    .badge{display:inline-block;padding:6px 10px;border-radius:999px;background:rgba(96,165,250,0.12);color:var(--accent);font-weight:600}
    .flex{display:flex;gap:12px;align-items:center}
    .small{color:var(--muted);font-size:0.95rem}
    a{color:var(--accent);text-decoration:none}
    .table-responsive{overflow:auto}
    footer{color:var(--muted);font-size:0.9rem;margin-top:20px}
  
    @media (max-width:720px){body{padding:18px}.card{padding:14px}}
  </style>

  <script src="https://unpkg.com/mermaid@10/dist/mermaid.min.js"></script>
  <script>mermaid.initialize({startOnLoad:true});</script>
</head>
<body>
  <div class="container">
    <header class="card">
      <div class="flex">
        <div>
          <h1> Sistema de Gestión de Universidad</h1>
        </div>
        <div style="margin-left:auto"><span class="badge">FastAPI • SQLModel • PostgreSQL</span></div>
      </div>
    </header>

    <section class="card">
      <h2> Descripción del Proyecto</h2>
      <p>Este sistema gestiona la información académica de una universidad: <strong>cursos</strong>, <strong>estudiantes</strong> y <strong>matrículas</strong>. Permite realizar operaciones CRUD, consultar relaciones entre entidades y asegura reglas de negocio para mantener la integridad de los datos.</p>
    </section>

    <section class="card">
      <h2> Funcionalidades Principales</h2>
      <ul>
        <li>Registrar cursos (código, nombre, créditos, horario).</li>
        <li>Registrar estudiantes (cédula, nombre, email, semestre).</li>
        <li>Consultar cursos de un estudiante.</li>
        <li>Consultar estudiantes de un curso.</li>
        <li>Gestionar matrículas entre estudiantes y cursos.</li>
      </ul>
    </section>

    <section class="card">
      <h2> Lógica de Negocio</h2>
      <ul>
        <li>La <strong>cédula</strong> del estudiante es <strong>única</strong> (sin duplicados).</li>
        <li>El <strong>código de curso</strong> es <strong>único</strong> (sin cursos repetidos).</li>
        <li>Un estudiante no puede estar matriculado dos veces en el mismo curso.</li>
        <li><strong>Cascada:</strong> al eliminar un estudiante, se eliminan sus matrículas asociadas (soft delete o eliminación física según implementación).</li>
      </ul>
    </section>

    <section class="card">
      <h2> Modelos de Datos</h2>

      <h3>Estudiante</h3>
      <div class="table-responsive">
      <table>
        <thead><tr><th>Campo</th><th>Tipo</th><th>Descripción</th></tr></thead>
        <tbody>
          <tr><td>cedula</td><td>String</td><td>Llave primaria</td></tr>
          <tr><td>nombre</td><td>String</td><td>Nombre completo</td></tr>
          <tr><td>email</td><td>String</td><td>Correo electrónico</td></tr>
          <tr><td>semestre</td><td>int</td><td>Semestre actual</td></tr>
          <tr><td>activo</td><td>bool</td><td>Estado del estudiante</td></tr>
        </tbody>
      </table>
      </div>

      <h3 style="margin-top:12px">Curso</h3>
      <div class="table-responsive">
      <table>
        <thead><tr><th>Campo</th><th>Tipo</th><th>Descripción</th></tr></thead>
        <tbody>
          <tr><td>codigo</td><td>String</td><td>Llave primaria</td></tr>
          <tr><td>nombre</td><td>String</td><td>Nombre del curso</td></tr>
          <tr><td>creditos</td><td>int</td><td>Número de créditos</td></tr>
          <tr><td>horario</td><td>String</td><td>Horario del curso</td></tr>
          <tr><td>activo</td><td>bool</td><td>Estado del curso</td></tr>
        </tbody>
      </table>
      </div>

      <h3 style="margin-top:12px">Matrícula</h3>
      <div class="table-responsive">
      <table>
        <thead><tr><th>Campo</th><th>Tipo</th><th>Descripción</th></tr></thead>
        <tbody>
          <tr><td>id_matricula</td><td>int</td><td>Llave primaria</td></tr>
          <tr><td>cedula_estudiante</td><td>String</td><td>Llave foránea → Estudiante</td></tr>
          <tr><td>codigo_curso</td><td>String</td><td>Llave foránea → Curso</td></tr>
          <tr><td>anio</td><td>int</td><td>Año de la matrícula</td></tr>
          <tr><td>activo</td><td>bool</td><td>Estado de la matrícula</td></tr>
        </tbody>
      </table>
      </div>
    </section>

    <section class="card">
      <h2> Relaciones entre Modelos</h2>
      <p>Un estudiante puede estar en muchos cursos y un curso puede tener muchos estudiantes (relación N:M), implementada a través de la tabla <code>MATRICULA</code>.</p>


      </div>
    </section>

    <section class="card">
      <h2>Mapa de Endpoints</h2>
      <div class="table-responsive">
      <table>
        <thead><tr><th>Método</th><th>Endpoint</th><th>Descripción</th><th>Modelo</th></tr></thead>
        <tbody>
          <tr><td>POST</td><td>/estudiantes/</td><td>Crear un nuevo estudiante</td><td>Estudiante</td></tr>
          <tr><td>GET</td><td>/estudiantes/</td><td>Listar estudiantes por semestre (query: semestre)</td><td>Estudiante</td></tr>
          <tr><td>PUT</td><td>/estudiantes/{cedula}</td><td>Actualizar datos de un estudiante</td><td>Estudiante</td></tr>
          <tr><td>DELETE</td><td>/estudiantes/{cedula}</td><td>Eliminar un estudiante</td><td>Estudiante</td></tr>
          <tr><td>GET</td><td>/estudiantes/inactivos</td><td>Histórico de estudiantes eliminados</td><td>Estudiante</td></tr>
          <tr><td>GET</td><td>/estudiantes/{cedula}/cursos</td><td>Listar cursos de un estudiante</td><td>Estudiante ↔ Curso</td></tr>
          <tr><td>POST</td><td>/cursos/</td><td>Crear un nuevo curso</td><td>Curso</td></tr>
          <tr><td>GET</td><td>/cursos/creditos/{creditos}</td><td>Listar cursos por créditos</td><td>Curso</td></tr>
          <tr><td>GET</td><td>/cursos/{codigo}</td><td>Obtener curso por código</td><td>Curso</td></tr>
          <tr><td>GET</td><td>/cursos/{codigo}/estudiantes</td><td>Listar estudiantes de un curso</td><td>Curso ↔ Estudiante</td></tr>
          <tr><td>PUT</td><td>/cursos/{codigo}</td><td>Actualizar datos de un curso</td><td>Curso</td></tr>
          <tr><td>DELETE</td><td>/cursos/{codigo}</td><td>Eliminar un curso</td><td>Curso</td></tr>
          <tr><td>POST</td><td>/matriculas/</td><td>Matricular un estudiante en un curso</td><td>Matrícula</td></tr>
          <tr><td>PUT</td><td>/matriculas/desmatricular/{cedula_estudiante}/{codigo_curso}</td><td>Desmatricular a un estudiante</td><td>Matrícula</td></tr>
        </tbody>
      </table>
      </div>
    </section>

    <section class="card">
      <h2>Tecnologías y servicios</h2>
      <p class="small">Python 3.13, FastAPI, SQLModel/SQLAlchemy, PostgreSQL, Uvicorn, Render</p>
    </section>

    <section class="card">
      <h2>Para acceder al Swagger(/docs) funcional</h2>
      <p class="small">https://sistema-universidad-rxy6.onrender.com/docs#/</p>
      
    </section>

    <footer>
      <div class="small">Autor: <strong>Juan Lozano</strong> • Estudiante de Ingeniería de Sistemas y Computación </div> 
    </footer>
  </div>
</body>
</html>
