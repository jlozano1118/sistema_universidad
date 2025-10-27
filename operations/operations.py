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