from sqlalchemy import String,DateTime,Integer,Boolean,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from datetime import datetime
from app.database.base import Base

class Gestor_tiempo(Base):
    __tablename__='Gestor_tiempo'
    id:Mapped[int]=mapped_column(primary_key=True, index=True)

    paciente:Mapped[str]= mapped_column(String(150), unique=False,index=True)

    activity:Mapped[str]= mapped_column(String(200),unique=False,index=True)

    usuario_id:Mapped[int] = mapped_column(ForeignKey("Usuarios.id"))

    usuario= relationship('Usuario', back_populates='registros')

    fecha_hora:Mapped[datetime]= mapped_column(DateTime)

    tiempo:Mapped[int]= mapped_column(Integer)

    modo_grupal:Mapped[bool]= mapped_column(Boolean, default=False)
