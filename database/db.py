from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

DB_NAME     = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST     = "localhost"
DB_PORT     = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine       = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)
Base         = declarative_base()


class Miembro(Base):
    __tablename__ = "miembro"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    nombre         = Column(String(255), nullable=False)
    apellido       = Column(String(255), nullable=False)
    email          = Column(String(80), nullable=False)
    telefono       = Column(String(15), nullable=True)
    tipo           = Column(Enum("pregrado", "postgrado", "funcionario", "academico"), nullable=False)
    fecha_registro = Column(DateTime, nullable=False, default=datetime.now)

    actividades = relationship("Actividad", back_populates="miembro", cascade="all, delete")


class Actividad(Base):
    __tablename__ = "actividad"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    miembro_id  = Column(Integer, ForeignKey("miembro.id"), nullable=False)
    tipo        = Column(Enum("deportiva", "artistica", "tecnologica", "social", "recreativa"), nullable=False)
    nombre      = Column(String(45), nullable=False)
    descripcion = Column(Text, nullable=True)
    dia         = Column(Enum("lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"), nullable=False)
    hora_inicio = Column(String(5), nullable=False)
    hora_fin    = Column(String(5), nullable=False)
    enlace      = Column(String(500), nullable=True)

    miembro = relationship("Miembro", back_populates="actividades")
    fotos   = relationship("Foto", back_populates="actividad", cascade="all, delete")


class Foto(Base):
    __tablename__ = "foto"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    actividad_id   = Column(Integer, ForeignKey("actividad.id"), nullable=False)
    ruta_archivo   = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)

    actividad = relationship("Actividad", back_populates="fotos")



def get_ultimos_miembros(n=5):
    session = SessionLocal()
    miembros = session.query(Miembro).order_by(Miembro.fecha_registro.desc()).limit(n).all()
    session.close()
    return miembros


def get_todos_miembros(filtro_tipo=None, ordenar_por=None):
    session = SessionLocal()
    query = session.query(Miembro)

    if filtro_tipo:
        query = query.filter(Miembro.tipo == filtro_tipo)

    columnas_orden = {
        "nombre":   Miembro.nombre,
        "apellido": Miembro.apellido,
        "email":    Miembro.email,
    }
    if ordenar_por and ordenar_por in columnas_orden:
        query = query.order_by(columnas_orden[ordenar_por])
    else:
        query = query.order_by(Miembro.apellido)

    miembros = query.all()
    session.close()
    return miembros


def get_miembro_por_id(id):
    session = SessionLocal()
    miembro = session.query(Miembro).filter_by(id=id).first()
    session.close()
    return miembro


def crear_miembro(nombre, apellido, email, telefono, tipo):
    session = SessionLocal()
    nuevo = Miembro(
        nombre         = nombre,
        apellido       = apellido,
        email          = email,
        telefono       = telefono if telefono else None,
        tipo           = tipo,
        fecha_registro = datetime.now()
    )
    session.add(nuevo)
    session.commit()
    miembro_id = nuevo.id
    session.close()
    return miembro_id


def crear_actividad(miembro_id, tipo, nombre, descripcion, dia, hora_inicio, hora_fin, enlace):
    session = SessionLocal()
    nueva = Actividad(
        miembro_id  = miembro_id,
        tipo        = tipo,
        nombre      = nombre,
        descripcion = descripcion if descripcion else None,
        dia         = dia,
        hora_inicio = hora_inicio,
        hora_fin    = hora_fin,
        enlace      = enlace if enlace else None
    )
    session.add(nueva)
    session.commit()
    actividad_id = nueva.id
    session.close()
    return actividad_id


def get_actividades_por_miembro(miembro_id):
    session = SessionLocal()
    actividades = session.query(Actividad).filter_by(miembro_id=miembro_id).all()
    session.close()
    return actividades


def crear_foto(actividad_id, ruta_archivo, nombre_archivo):
    session = SessionLocal()
    nueva = Foto(
        actividad_id   = actividad_id,
        ruta_archivo   = ruta_archivo,
        nombre_archivo = nombre_archivo
    )
    session.add(nueva)
    session.commit()
    session.close()


def get_fotos_por_actividad(actividad_id):
    session = SessionLocal()
    fotos = session.query(Foto).filter_by(actividad_id=actividad_id).all()
    session.close()
    return fotos