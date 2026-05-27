from datetime import date

from werkzeug.security import generate_password_hash

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
from utils.auth import ROL_ALUMNO, ROL_SESION, USUARIO_SESION


def iniciar_sesion(client, usuario, rol):
    with client.session_transaction() as session:
        session[USUARIO_SESION] = usuario.id_usuario
        session[ROL_SESION] = rol


def crear_usuario(
    correo="usuario@sgci.test",
    password="Password123",
    activo=True,
    nombres="Usuario",
    apellido_paterno="Prueba",
    apellido_materno="Sistema",
):
    usuario = Usuario(
        nombres=nombres,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        correo=correo,
        fecha_nacimiento=date(2000, 1, 1),
        activo=activo,
        password_hash=generate_password_hash(password),
    )
    db.session.add(usuario)
    db.session.flush()
    return usuario


def crear_administrador(correo="admin@sgci.test", password="Password123", activo=True):
    usuario = crear_usuario(correo=correo, password=password, activo=activo, nombres="Admin")
    db.session.add(
        Administrador(
            id_usuario=usuario.id_usuario,
            nivel_acceso=1,
            area_responsable="Sistema",
        )
    )
    db.session.flush()
    return usuario


def crear_profesor(
    correo="profesor@sgci.test",
    password="Password123",
    activo=True,
    numero_empleado="EMP-001",
):
    usuario = crear_usuario(correo=correo, password=password, activo=activo, nombres="Profesor")
    db.session.add(
        Profesor(
            id_usuario=usuario.id_usuario,
            numero_empleado=numero_empleado,
            especialidad="Inglés",
            fecha_contratacion=date(2024, 1, 15),
        )
    )
    db.session.flush()
    return usuario


def crear_alumno(
    correo="alumno@sgci.test",
    password="Password123",
    activo=True,
    matricula="ALU-001",
    idioma=None,
    nivel=6,
):
    usuario = crear_usuario(correo=correo, password=password, activo=activo, nombres="Alumno")
    db.session.add(Alumno(id_usuario=usuario.id_usuario, matricula=matricula))
    db.session.flush()

    if idioma is not None:
        db.session.add(
            NivelAlumno(
                id_usuario=usuario.id_usuario,
                id_idioma=idioma.id_idioma,
                nivel=nivel,
            )
        )
        db.session.flush()

    return usuario


def crear_idioma(nombre="Inglés"):
    idioma = Idioma(nombre=nombre)
    db.session.add(idioma)
    db.session.flush()
    return idioma


def crear_curso(
    profesor,
    idioma,
    codigo="ING-A1-001",
    nombre="Inglés básico A1",
    estado="borrador",
    nivel_requerido=1,
    cupo_maximo=25,
):
    curso = Curso(
        id_profesor=profesor.id_usuario,
        id_idioma=idioma.id_idioma,
        codigo=codigo,
        nombre=nombre,
        nivel_requerido=nivel_requerido,
        modalidad="En línea",
        cupo_maximo=cupo_maximo,
        estado_curso=estado,
    )
    db.session.add(curso)
    db.session.flush()
    return curso


def crear_inscripcion(alumno, curso, estado="activa"):
    inscripcion = Inscripcion(
        id_alumno=alumno.id_usuario,
        id_curso=curso.id_curso,
        estado_inscripcion=estado,
    )
    db.session.add(inscripcion)
    db.session.flush()
    return inscripcion


def crear_material(curso, titulo="Guía inicial", visible=True, url_archivo="https://example.com/material.pdf"):
    material = Material(
        id_curso=curso.id_curso,
        titulo=titulo,
        tipo_material="PDF",
        url_archivo=url_archivo,
        visible=visible,
    )
    db.session.add(material)
    db.session.flush()
    return material


def datos_formulario_usuario(**overrides):
    datos = {
        "nombres": "Nuevo",
        "apellido_paterno": "Usuario",
        "apellido_materno": "Prueba",
        "correo": "nuevo@sgci.test",
        "fecha_nacimiento": "2001-05-20",
        "password": "Password123",
        "rol": ROL_ALUMNO,
        "matricula": "ALU-NEW",
        "numero_empleado": "",
        "especialidad": "",
        "fecha_contratacion": "",
        "nivel_acceso": "1",
        "area_responsable": "",
    }
    datos.update(overrides)
    return datos


def datos_formulario_curso(idioma, **overrides):
    datos = {
        "codigo": "ING-A1-100",
        "nombre": "Inglés básico A1",
        "id_idioma": str(idioma.id_idioma),
        "nivel_requerido": "1",
        "modalidad": "En línea",
        "cupo_maximo": "20",
    }
    datos.update(overrides)
    return datos
