from datetime import date, datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from werkzeug.security import generate_password_hash

from app import create_app
from models import db
from models.Administrador import Administrador
from models.Alumno import Alumno
from models.Curso import Curso
from models.Idioma import Idioma
from models.Inscripcion import Inscripcion
from models.Material import Material
from models.NivelAlumno import NivelAlumno
from models.Profesor import Profesor
from models.Usuario import Usuario

CREDENCIALES = {
    "admin@sgci.com": "Admin12345",
    "profesor@sgci.com": "Profesor12345",
    "alumno@sgci.com": "Alumno12345",
}


class UsuarioPrueba:
    def __init__(self, nombres, apellido_paterno, apellido_materno, correo, fecha_nacimiento, password):
        self.nombres = nombres
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.correo = correo
        self.fecha_nacimiento = fecha_nacimiento
        self.password = password


def ejecutar_poblacion():
    admin = crear_usuario_prueba(
        UsuarioPrueba(
            "Administrador",
            "General",
            "Sistema",
            "admin@sgci.com",
            date(1990, 1, 1),
            CREDENCIALES["admin@sgci.com"],
        )
    )
    profesor = crear_usuario_prueba(
        UsuarioPrueba(
            "Laura",
            "Martínez",
            "Gómez",
            "profesor@sgci.com",
            date(1985, 4, 15),
            CREDENCIALES["profesor@sgci.com"],
        )
    )
    alumno = crear_usuario_prueba(
        UsuarioPrueba(
            "Carlos",
            "Ramírez",
            "Luna",
            "alumno@sgci.com",
            date(2002, 9, 20),
            CREDENCIALES["alumno@sgci.com"],
        )
    )

    asignar_administrador(admin.id_usuario)
    asignar_profesor(profesor.id_usuario)
    asignar_alumno(alumno.id_usuario)

    ingles = crear_idioma("Inglés")
    frances = crear_idioma("Francés")
    aleman = crear_idioma("Alemán")

    curso_ingles = crear_curso(
        profesor.id_usuario,
        ingles.id_idioma,
        "ING-A1-001",
        "Inglés básico A1",
        1,
        "En línea",
        25,
        "publicado",
    )
    crear_curso(
        profesor.id_usuario,
        frances.id_idioma,
        "FRA-B1-001",
        "Francés intermedio B1",
        3,
        "Presencial",
        20,
        "borrador",
    )
    crear_curso(
        profesor.id_usuario,
        aleman.id_idioma,
        "ALE-A1-001",
        "Alemán inicial",
        1,
        "En línea",
        15,
        "cerrado",
    )

    crear_material(curso_ingles.id_curso, "Guía de pronunciación básica", "PDF", "https://example.com/materiales/guia-pronunciacion.pdf")
    crear_material(curso_ingles.id_curso, "Video introductorio del curso", "Video", "https://example.com/materiales/video-introduccion")
    crear_inscripcion(alumno.id_usuario, curso_ingles.id_curso)
    crear_nivel_alumno(alumno.id_usuario, ingles.id_idioma, 1)
    crear_nivel_alumno(alumno.id_usuario, frances.id_idioma, 1)

    db.session.commit()
    imprimir_resultado()


def crear_usuario_prueba(datos):
    usuario = Usuario.query.filter_by(correo=datos.correo).first()

    if usuario is None:
        usuario = Usuario(correo=datos.correo)
        db.session.add(usuario)

    usuario.nombres = datos.nombres
    usuario.apellido_paterno = datos.apellido_paterno
    usuario.apellido_materno = datos.apellido_materno
    usuario.fecha_nacimiento = datos.fecha_nacimiento
    usuario.activo = True
    usuario.password_hash = generate_password_hash(datos.password)
    usuario.ultimo_cambio_password = datetime.utcnow()

    db.session.flush()
    return usuario


def asignar_administrador(id_usuario):
    administrador = db.session.get(Administrador, id_usuario)

    if administrador is None:
        administrador = Administrador(id_usuario=id_usuario)
        db.session.add(administrador)

    administrador.nivel_acceso = 1
    administrador.area_responsable = "Sistema"


def asignar_profesor(id_usuario):
    profesor = db.session.get(Profesor, id_usuario)

    if profesor is None:
        profesor = Profesor(id_usuario=id_usuario)
        db.session.add(profesor)

    profesor.numero_empleado = "PROF-001"
    profesor.especialidad = "Inglés y Francés"
    profesor.fecha_contratacion = date(2023, 1, 10)


def asignar_alumno(id_usuario):
    alumno = db.session.get(Alumno, id_usuario)

    if alumno is None:
        alumno = Alumno(id_usuario=id_usuario)
        db.session.add(alumno)

    alumno.matricula = "ALU-001"


def crear_idioma(nombre):
    idioma = Idioma.query.filter_by(nombre=nombre).first()

    if idioma is None:
        idioma = Idioma(nombre=nombre)
        db.session.add(idioma)
        db.session.flush()

    return idioma


def crear_curso(id_profesor, id_idioma, codigo, nombre, nivel_requerido, modalidad, cupo_maximo, estado_curso):
    curso = Curso.query.filter_by(codigo=codigo).first()

    if curso is None:
        curso = Curso(codigo=codigo)
        db.session.add(curso)

    curso.id_profesor = id_profesor
    curso.id_idioma = id_idioma
    curso.nombre = nombre
    curso.nivel_requerido = nivel_requerido
    curso.modalidad = modalidad
    curso.cupo_maximo = cupo_maximo
    curso.estado_curso = estado_curso
    db.session.flush()
    return curso


def crear_material(id_curso, titulo, tipo_material, url_archivo):
    material = Material.query.filter_by(id_curso=id_curso, titulo=titulo).first()

    if material is None:
        material = Material(id_curso=id_curso, titulo=titulo)
        db.session.add(material)

    material.tipo_material = tipo_material
    material.url_archivo = url_archivo
    material.visible = True
    material.fecha_publicacion = datetime.utcnow()


def crear_inscripcion(id_alumno, id_curso):
    inscripcion = db.session.get(Inscripcion, {"id_alumno": id_alumno, "id_curso": id_curso})

    if inscripcion is None:
        inscripcion = Inscripcion(id_alumno=id_alumno, id_curso=id_curso)
        db.session.add(inscripcion)

    inscripcion.estado_inscripcion = "activa"
    inscripcion.fecha_inscripcion = datetime.utcnow()


def crear_nivel_alumno(id_usuario, id_idioma, nivel):
    nivel_alumno = db.session.get(NivelAlumno, {"id_usuario": id_usuario, "id_idioma": id_idioma})

    if nivel_alumno is None:
        nivel_alumno = NivelAlumno(id_usuario=id_usuario, id_idioma=id_idioma)
        db.session.add(nivel_alumno)

    nivel_alumno.nivel = nivel


def imprimir_resultado():
    print("Datos de prueba creados correctamente.\n")
    print("Credenciales de acceso:")
    print("- Administrador: admin@sgci.com / Admin12345")
    print("- Profesor: profesor@sgci.com / Profesor12345")
    print("- Alumno: alumno@sgci.com / Alumno12345\n")
    print("Ejecuta python scripts/listar_datos_prueba.py para consultar usuarios y cursos cargados.")


app = create_app()

with app.app_context():
    ejecutar_poblacion()
