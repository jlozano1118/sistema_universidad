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
