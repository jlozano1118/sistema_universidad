<h1 align="center">Sistema de Gestión de Universidad</h1>

<hr>

<h2>1. <b>Descripción del Proyecto</b></h2>

<p>
Este sistema fue desarrollado para gestionar la información académica de una universidad, incluyendo cursos, estudiantes y matrículas.
El objetivo principal es ofrecer una plataforma que permita realizar operaciones CRUD (crear, leer, actualizar y eliminar) de forma eficiente,
garantizando la integridad de los datos y aplicando reglas de negocio coherentes.
</p>

<h2>2. Funcionalidades Principales</h2>
<ul>
  <li>Registrar cursos con código, nombre, número de créditos y horario.</li>
  <li>Registrar estudiantes con cédula, nombre, email y semestre.</li>
  <li>Consultar cursos de un estudiante.</li>
  <li>Consultar estudiantes matriculados en un curso.</li>
  <li>Gestionar matrículas entre estudiantes y cursos.</li>
</ul>

<h2>3. Lógica de Negocio</h2>
<ul>
  <li>La cédula del estudiante es única → no pueden existir estudiantes duplicados.</li>
  <li>El código de curso es único → no pueden existir cursos repetidos.</li>
  <li>Un estudiante no puede estar matriculado dos veces en el mismo curso.</li>
  <li>Cascada: si se elimina un estudiante, también se eliminan sus matrículas asociadas.</li>
</ul>

<h2>4. Modelos</h2>

<h3> Estudiante</h3>

<table>
  <tr><th>Campo</th><th>Tipo</th><th>Descripción</th></tr>
  <tr><td>cedula</td><td>String</td><td>Llave primaria</td></tr>
  <tr><td>nombre</td><td>String</td><td>Nombre completo del estudiante</td></tr>
  <tr><td>email</td><td>String</td><td>Correo electrónico</td></tr>
  <tr><td>semestre</td><td>int</td><td>Semestre actual</td></tr>
  <tr><td>activo</td><td>bool</td><td>Estado del estudiante</td></tr>
</table>

<h3>Curso</h3>

<table>
  <tr><th>Campo</th><th>Tipo</th><th>Descripción</th></tr>
  <tr><td>codigo</td><td>String</td><td>Llave primaria</td></tr>
  <tr><td>nombre</td><td>String</td><td>Nombre del curso</td></tr>
  <tr><td>creditos</td><td>int</td><td>Número de créditos</td></tr>
  <tr><td>horario</td><td>String</td><td>Horario del curso</td></tr>
  <tr><td>activo</td><td>bool</td><td>Estado del curso</td></tr>
</table>

<h3>Matrícula</h3>

<table>
  <tr><th>Campo</th><th>Tipo</th><th>Descripción</th></tr>
  <tr><td>id_matricula</td><td>int</td><td>Llave primaria</td></tr>
  <tr><td>cedula_estudiante</td><td>String</td><td>Llave foránea → Estudiante</td></tr>
  <tr><td>codigo_curso</td><td>String</td><td>Llave foránea → Curso</td></tr>
  <tr><td>anio</td><td>int</td><td>Año de la matrícula</td></tr>
  <tr><td>activo</td><td>bool</td><td>Estado de la matrícula</td></tr>
</table>

<h3>Relaciones entre Modelos</h3>
<ul>
  <li>Un curso puede tener muchos estudiantes (Relación N:M).</li>
  <li>Un estudiante puede estar matriculado en muchos cursos (Relación N:M).</li>
</ul>

<h2>5. Mapa de Endpoints</h2>

<table>
  <tr><th>Método</th><th>Endpoint</th><th>Descripción</th><th>Modelo Relacionado</th></tr>
  <tr><td>POST</td><td>/estudiantes/</td><td>Crear un nuevo estudiante</td><td>Estudiante</td></tr>
  <tr><td>GET</td><td>/estudiantes/?semestre=</td><td>Listar estudiantes por semestre</td><td>Estudiante</td></tr>
  <tr><td>PUT</td><td>/estudiantes/{cedula}</td><td>Actualizar datos de un estudiante</td><td>Estudiante</td></tr>
  <tr><td>DELETE</td><td>/estudiantes/{cedula}</td><td>Eliminar un estudiante</td><td>Estudiante</td></tr>
  <tr><td>GET</td><td>/estudiantes/inactivos</td><td>Listar estudiantes eliminados (histórico)</td><td>Estudiante</td></tr>
  <tr><td>GET</td><td>/estudiantes/{cedula}/cursos</td><td>Listar cursos de un estudiante</td><td>Estudiante ↔ Curso</td></tr>
  <tr><td>POST</td><td>/cursos/</td><td>Crear un nuevo curso</td><td>Curso</td></tr>
  <tr><td>GET</td><td>/cursos/creditos/{creditos}</td><td>Listar cursos por número de créditos</td><td>Curso</td></tr>
  <tr><td>GET</td><td>/cursos/{codigo}</td><td>Obtener curso por código</td><td>Curso</td></tr>
  <tr><td>GET</td><td>/cursos/{codigo}/estudiantes</td><td>Listar estudiantes matriculados en un curso</td><td>Curso ↔ Estudiante</td></tr>
  <tr><td>PUT</td><td>/cursos/{codigo}</td><td>Actualizar datos de un curso</td><td>Curso</td></tr>
  <tr><td>DELETE</td><td>/cursos/{codigo}</td><td>Eliminar un curso</td><td>Curso</td></tr>
  <tr><td>POST</td><td>/matriculas/</td><td>Matricular un estudiante en un curso</td><td>Matrícula</td></tr>
  <tr><td>PUT</td><td>/matriculas/desmatricular/{cedula_estudiante}/{codigo_curso}</td><td>Desmatricular a un estudiante de un curso</td><td>Matrícula</td></tr>
</table>

<h2>7. Tecnologías Utilizadas</h2>
<ul>
  <li>Python 3.13</li>
  <li>FastAPI</li>
  <li>SQLModel / SQLAlchemy</li>
  <li>PostgreSQL</li>
  <li>Uvicorn</li>
  <li>Render</li>
</ul>

<h2>8. Acceso al Swagger</h2>
<p>
Puedes acceder a la documentación interactiva de la API en el siguiente enlace:<br>
<a href="https://sistema-universidad-rxy6.onrender.com/docs#" target="_blank">
  🔗 https://sistema-universidad-rxy6.onrender.com/docs#
</a>
</p>
