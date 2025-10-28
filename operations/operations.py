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