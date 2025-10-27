from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint


class Estudiante(SQLModel, table=True):
    cedula: str = Field(primary_key=True)
    nombre: str
    email: str
    semestre:int
    activo: bool = Field(default=True, nullable=False)

    matriculas: List["Matricula"] = Relationship(back_populates="estudiante")


class Curso(SQLModel, table=True):
    codigo: str = Field(primary_key=True)
    nombre: str
    creditos: int
    horario: str
    activo: bool = Field(default=True, nullable=False)

    matriculas: List["Matricula"] = Relationship(back_populates="curso")


class Matricula(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("cedula_estudiante", "codigo_curso", name="uq_estudiante_curso"),
    )

    id_matricula: Optional[int] = Field(default=None, primary_key=True)
    cedula_estudiante: str = Field(foreign_key="estudiante.cedula", nullable=False)
    codigo_curso: str = Field(foreign_key="curso.codigo", nullable=False)
    anio: int
    activo: bool = Field(default=True, nullable=False)

    estudiante: Optional[Estudiante] = Relationship(back_populates="matriculas")
    curso: Optional[Curso] = Relationship(back_populates="matriculas")