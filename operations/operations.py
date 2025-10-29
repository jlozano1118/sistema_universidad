from fastapi import HTTPException
from sqlmodel import Session, select
from data.models import Estudiante, Curso, Matricula


def crear_estudiante(session: Session, estudiante: Estudiante):
    existente = session.exec(select(Estudiante).where(Estudiante.email == estudiante.email)).first()
    if existente:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un estudiante con el correo {estudiante.email}"
        )

    existente_cedula = session.exec(select(Estudiante).where(Estudiante.cedula == estudiante.cedula)).first()
    if existente_cedula:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un estudiante con la cédula {estudiante.cedula}"
        )

    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante

def listar_estudiantes_por_semestre(session: Session, semestre: int):
    estudiantes = session.exec(
        select(Estudiante).where(
            (Estudiante.semestre == semestre) & (Estudiante.activo == True)
        )
    ).all()

    if not estudiantes:
        raise HTTPException(status_code=404, detail=f"No se encontraron estudiantes en el semestre {semestre}")

    return estudiantes


def actualizar_estudiante(session: Session, cedula: str, datos: Estudiante):
    estudiante = session.get(Estudiante, cedula)
    if not estudiante or not estudiante.activo:
        raise HTTPException(status_code=404, detail=f"Estudiante con cédula {cedula} no encontrado o inactivo")

    if datos.email != estudiante.email:
        existente = session.exec(select(Estudiante).where(Estudiante.email == datos.email)).first()
        if existente:
            raise HTTPException(status_code=400, detail=f"El correo {datos.email} ya está en uso")

    estudiante.nombre = datos.nombre
    estudiante.email = datos.email
    estudiante.semestre = datos.semestre
    estudiante.activo = datos.activo

    session.commit()
    session.refresh(estudiante)
    return estudiante


def eliminar_estudiante(session: Session, cedula: str):
    estudiante = session.get(Estudiante, cedula)
    if not estudiante:
        raise HTTPException(status_code=404, detail=f"Estudiante con cédula {cedula} no encontrado")

    if not estudiante.activo:
        raise HTTPException(status_code=400, detail=f"El estudiante con cédula {cedula} ya está inactivo")

    estudiante.activo = False
    session.commit()
    session.refresh(estudiante)

    return {"mensaje": f"Estudiante con cédula {cedula} fue desactivado correctamente"}

def crear_curso(session: Session, curso: Curso):
    existente_codigo = session.exec(
        select(Curso).where(Curso.codigo == curso.codigo)
    ).first()
    if existente_codigo:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un curso con el código {curso.codigo}"
        )

    existente_nombre = session.exec(
        select(Curso).where(Curso.nombre == curso.nombre)
    ).first()
    if existente_nombre:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un curso con el nombre {curso.nombre}"
        )

    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso

def listar_cursos_por_creditos(session: Session, creditos: int):
    cursos = session.exec(
        select(Curso).where(
            (Curso.creditos == creditos) & (Curso.activo == True)
        )
    ).all()

    if not cursos:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron cursos con {creditos} créditos"
        )

    return cursos


def listar_cursos_por_codigo(session: Session, codigo: str):
    curso = session.exec(
        select(Curso).where(
            (Curso.codigo == codigo) & (Curso.activo == True)
        )
    ).first()

    if not curso:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró un curso con el código {codigo}"
        )

    return curso


def actualizar_curso(session: Session, codigo: str, datos: Curso):
    curso = session.get(Curso, codigo)
    if not curso or not curso.activo:
        raise HTTPException(status_code=404, detail=f"Curso con código {codigo} no encontrado o inactivo")

    if datos.nombre != curso.nombre:
        existente = session.exec(select(Curso).where(Curso.nombre == datos.nombre)).first()
        if existente:
            raise HTTPException(status_code=400, detail=f"El curso con nombre {datos.nombre} ya existe")

    curso.nombre = datos.nombre
    curso.creditos = datos.creditos
    curso.horario = datos.horario
    curso.activo = datos.activo

    session.commit()
    session.refresh(curso)
    return curso


def eliminar_curso(session: Session, codigo: str):
    curso = session.get(Curso, codigo)
    if not curso:
        raise HTTPException(status_code=404, detail=f"Curso con código {codigo} no encontrado")

    if not curso.activo:
        raise HTTPException(status_code=400, detail=f"El curso con código {codigo} ya está inactivo")

    curso.activo = False
    session.commit()
    session.refresh(curso)

    return {"mensaje": f"Curso con código {codigo} fue desactivado correctamente"}

def crear_matricula(session: Session, matricula: Matricula):
    if matricula.id_matricula is not None:
        existente_id = session.get(Matricula, matricula.id_matricula)
        if existente_id:
            raise HTTPException(
                status_code=400,
                detail=f"El ID de matrícula {matricula.id_matricula} ya existe"
            )
    estudiante = session.get(Estudiante, matricula.cedula_estudiante)
    if not estudiante or not estudiante.activo:
        raise HTTPException(
            status_code=404,
            detail=f"El estudiante con cédula {matricula.cedula_estudiante} no existe o está inactivo"
        )


    curso = session.get(Curso, matricula.codigo_curso)
    if not curso or not curso.activo:
        raise HTTPException(
            status_code=404,
            detail=f"El curso con código {matricula.codigo_curso} no existe o está inactivo"
        )


    existente = session.exec(
        select(Matricula).where(
            (Matricula.cedula_estudiante == matricula.cedula_estudiante) &
            (Matricula.codigo_curso == matricula.codigo_curso)
        )
    ).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail=f"El estudiante {matricula.cedula_estudiante} ya está matriculado en el curso {matricula.codigo_curso}"
        )

    session.add(matricula)
    session.commit()
    session.refresh(matricula)
    return matricula


def cursos_estudiante(session: Session, cedula_estudiante: str):

    estudiante = session.get(Estudiante, cedula_estudiante)
    if not estudiante or not estudiante.activo:
        raise HTTPException(
            status_code=404,
            detail=f"Estudiante con cédula {cedula_estudiante} no encontrado o inactivo"
        )

    matriculas = session.exec(
        select(Matricula).where(
            (Matricula.cedula_estudiante == cedula_estudiante) &
            (Matricula.activo == True)
        )
    ).all()

    if not matriculas:
        raise HTTPException(
            status_code=404,
            detail=f"El estudiante con cédula {cedula_estudiante} no tiene cursos activos"
        )


    cursos = []
    for m in matriculas:
        curso = session.get(Curso, m.codigo_curso)
        if curso and curso.activo:
            cursos.append(curso)

    if not cursos:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron cursos activos para el estudiante {cedula_estudiante}"
        )

    return cursos


def obtener_estudiantes_por_curso(session: Session, codigo_curso: str):
    curso = session.get(Curso, codigo_curso)
    if not curso or not curso.activo:
        raise HTTPException(
            status_code=404,
            detail=f"Curso con código {codigo_curso} no encontrado o inactivo"
        )


    matriculas = session.exec(
        select(Matricula).where(
            (Matricula.codigo_curso == codigo_curso) &
            (Matricula.activo == True)
        )
    ).all()

    if not matriculas:
        raise HTTPException(
            status_code=404,
            detail=f"No hay estudiantes matriculados en el curso {codigo_curso}"
        )

    estudiantes = []
    for m in matriculas:
        estudiante = session.get(Estudiante, m.cedula_estudiante)
        if estudiante and estudiante.activo:
            estudiantes.append(estudiante)

    if not estudiantes:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron estudiantes activos en el curso {codigo_curso}"
        )

    return estudiantes

def desmatricular_estudiante(session: Session, cedula_estudiante: str, codigo_curso: str):

    estudiante = session.get(Estudiante, cedula_estudiante)
    if not estudiante:
        raise HTTPException(status_code=404, detail=f"Estudiante con cédula {cedula_estudiante} no encontrado")

    curso = session.get(Curso, codigo_curso)
    if not curso:
        raise HTTPException(status_code=404, detail=f"Curso con código {codigo_curso} no encontrado")


    query = select(Matricula).where(
        Matricula.cedula_estudiante == cedula_estudiante,
        Matricula.codigo_curso == codigo_curso
    )
    matricula = session.exec(query).first()

    if not matricula:
        raise HTTPException(status_code=404, detail="El estudiante no está matriculado en este curso")


    if not matricula.activo:
        raise HTTPException(status_code=400, detail="El estudiante ya fue desmatriculado de este curso")


    matricula.activo = False
    session.commit()
    session.refresh(matricula)

    return {
        "mensaje": f"El estudiante {cedula_estudiante} fue desmatriculado del curso {codigo_curso} correctamente"
    }


def obtener_estudiantes_inactivos(session: Session):
    estudiantes_inactivos = session.exec(
        select(Estudiante).where(Estudiante.activo == False)
    ).all()

    if not estudiantes_inactivos:
        raise HTTPException(status_code=404, detail="No hay estudiantes inactivos registrados")

    return estudiantes_inactivos