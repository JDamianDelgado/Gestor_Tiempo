from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

class Usuario(Base):
    __tablename__ = "Usuarios"

    id:Mapped[int]= mapped_column(primary_key=True, index=True)

    email:Mapped[str]= mapped_column(String(150), unique=True, index=True
    )
    nombre:Mapped[str]= mapped_column(String(100))

    apellido:Mapped[str]= mapped_column(String(100))

    dni:Mapped[int]= mapped_column(unique=True)
    
    registros = relationship('Gestor_tiempo', back_populates="usuario")


