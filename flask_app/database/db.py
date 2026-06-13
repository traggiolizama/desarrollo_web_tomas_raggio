from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload
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


class Region(Base):
    __tablename__ = "region"

    id     = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)

    comunas = relationship("Comuna", back_populates="region")


class Comuna(Base):
    __tablename__ = "comuna"

    id        = Column(Integer, primary_key=True, autoincrement=True)
    nombre    = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey("region.id"), nullable=False)

    region = relationship("Region", back_populates="comunas")
    miembros = relationship("Miembro", back_populates="comuna")


class Miembro(Base):
    __tablename__ = "miembro"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    nombre         = Column(String(255), nullable=False)
    apellido       = Column(String(255), nullable=False)
    email          = Column(String(80), nullable=False)
    telefono       = Column(String(15), nullable=True)
    tipo           = Column(Enum("pregrado", "postgrado", "funcionario", "academico"), nullable=False)
    fecha_registro = Column(DateTime, nullable=False, default=datetime.now)
    comuna_id      = Column(Integer, ForeignKey("comuna.id"), nullable=True)

    actividades = relationship("Actividad", back_populates="miembro", cascade="all, delete")
    comuna = relationship("Comuna", back_populates="miembros")


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
    comentarios = relationship("Comentario", back_populates="actividad", cascade="all, delete")


class Foto(Base):
    __tablename__ = "foto"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    actividad_id   = Column(Integer, ForeignKey("actividad.id"), nullable=False)
    ruta_archivo   = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)

    actividad = relationship("Actividad", back_populates="fotos")


class Comentario(Base):
    __tablename__ = "comentario"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    nombre       = Column(String(80), nullable=False)
    texto        = Column(String(300), nullable=False)
    fecha        = Column(DateTime, nullable=False, default=datetime.now)
    actividad_id = Column(Integer, ForeignKey("actividad.id"), nullable=False)

    actividad = relationship("Actividad", back_populates="comentarios")


def comentario_a_dict(comentario):
    return {
        "id": comentario.id,
        "nombre": comentario.nombre,
        "texto": comentario.texto,
        "fecha": comentario.fecha.strftime("%d/%m/%Y %H:%M")
    }


def region_a_dict(region):
    return {
        "id": region.id,
        "nombre": region.nombre
    }


def comuna_a_dict(comuna):
    return {
        "id": comuna.id,
        "nombre": comuna.nombre,
        "region_id": comuna.region_id
    }


def get_regiones():
    session = SessionLocal()
    regiones = session.query(Region).order_by(Region.id).all()
    datos = [region_a_dict(region) for region in regiones]
    session.close()
    return datos


def get_comunas_por_region(region_id):
    session = SessionLocal()
    comunas = (
        session.query(Comuna)
        .filter_by(region_id=region_id)
        .order_by(Comuna.nombre)
        .all()
    )
    datos = [comuna_a_dict(comuna) for comuna in comunas]
    session.close()
    return datos


def get_comuna_por_id(comuna_id):
    session = SessionLocal()
    comuna = session.query(Comuna).filter_by(id=comuna_id).first()
    datos = comuna_a_dict(comuna) if comuna else None
    session.close()
    return datos


def comuna_pertenece_a_region(comuna_id, region_id):
    session = SessionLocal()
    existe = (
        session.query(Comuna)
        .filter_by(id=comuna_id, region_id=region_id)
        .first()
        is not None
    )
    session.close()
    return existe


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
    miembro = (
        session.query(Miembro)
        .options(joinedload(Miembro.comuna).joinedload(Comuna.region))
        .filter_by(id=id)
        .first()
    )
    session.close()
    return miembro


def crear_miembro(nombre, apellido, email, telefono, tipo, comuna_id):
    session = SessionLocal()
    nuevo = Miembro(
        nombre         = nombre,
        apellido       = apellido,
        email          = email,
        telefono       = telefono if telefono else None,
        tipo           = tipo,
        fecha_registro = datetime.now(),
        comuna_id      = comuna_id
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


def get_actividad_por_id(id):
    session = SessionLocal()
    actividad = session.query(Actividad).filter_by(id=id).first()
    session.close()
    return actividad


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


def get_comentarios_por_actividad(actividad_id):
    session = SessionLocal()
    comentarios = (
        session.query(Comentario)
        .filter_by(actividad_id=actividad_id)
        .order_by(Comentario.fecha.desc())
        .all()
    )
    datos = [comentario_a_dict(comentario) for comentario in comentarios]
    session.close()
    return datos


def crear_comentario(actividad_id, nombre, texto_comentario):
    session = SessionLocal()
    nuevo = Comentario(
        actividad_id = actividad_id,
        nombre       = nombre,
        texto        = texto_comentario,
        fecha        = datetime.now()
    )
    session.add(nuevo)
    session.commit()
    datos = comentario_a_dict(nuevo)
    session.close()
    return datos


def get_miembros_por_dia():
    session = SessionLocal()
    fecha_registro = func.date(Miembro.fecha_registro)
    filas = (
        session.query(fecha_registro.label("fecha"), func.count(Miembro.id).label("total"))
        .group_by(fecha_registro)
        .order_by(fecha_registro)
        .all()
    )
    datos = [
        {
            "fecha": fila.fecha.isoformat() if hasattr(fila.fecha, "isoformat") else str(fila.fecha),
            "total": int(fila.total)
        }
        for fila in filas
    ]
    session.close()
    return datos


def get_actividades_por_tipo():
    session = SessionLocal()
    filas = (
        session.query(Actividad.tipo.label("tipo"), func.count(Actividad.id).label("total"))
        .group_by(Actividad.tipo)
        .order_by(Actividad.tipo)
        .all()
    )
    datos = [{"tipo": fila.tipo, "total": int(fila.total)} for fila in filas]
    session.close()
    return datos


def get_actividades_por_comuna():
    session = SessionLocal()
    comuna_nombre = func.coalesce(Comuna.nombre, "Sin comuna")
    filas = (
        session.query(
            comuna_nombre.label("comuna"),
            func.count(Actividad.id).label("total")
        )
        .join(Miembro, Actividad.miembro_id == Miembro.id)
        .outerjoin(Comuna, Miembro.comuna_id == Comuna.id)
        .group_by(comuna_nombre)
        .order_by(func.count(Actividad.id).desc(), comuna_nombre.asc())
        .all()
    )

    datos = [{"comuna": fila.comuna, "total": int(fila.total)} for fila in filas]
    session.close()
    return datos


def get_estadisticas():
    return {
        "miembros_por_dia": get_miembros_por_dia(),
        "actividades_por_tipo": get_actividades_por_tipo(),
        "actividades_por_comuna": get_actividades_por_comuna()
    }
