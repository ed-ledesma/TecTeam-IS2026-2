from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import create_app
from models.Administrador import Administrador
from models.Alumno import Alumno
from models.Curso import Curso
from models.Inscripcion import Inscripcion
from models.Profesor import Profesor
from models.Usuario import Usuario
from models import db

CREDENCIALES_CONOCIDAS = {
    "admin@sgci.com": "Admin12345",
    "profesor@sgci.com": "Profesor12345",
    "alumno@sgci.com": "Alumno12345",
}


def ejecutar_consulta():
    imprimir_usuarios()
    imprimir_cursos()


def imprimir_usuarios():
    usuarios = Usuario.query.order_by(Usuario.id_usuario.asc()).all()

    print("\nUSUARIOS")
    print("-" * 128)
    print(f"{'ID':<5} {'ROL':<16} {'ESTADO':<10} {'CORREO':<30} {'PASSWORD PRUEBA':<18} {'NOMBRE':<35}")
    print("-" * 128)

    for usuario in usuarios:
        print(
            f"{usuario.id_usuario:<5} "
            f"{obtener_rol(usuario.id_usuario):<16} "
            f"{obtener_estado(usuario):<10} "
            f"{usuario.correo:<30} "
            f"{CREDENCIALES_CONOCIDAS.get(usuario.correo, 'desconocido'):<18} "
            f"{obtener_nombre_completo(usuario):<35}"
        )

    print("-" * 128)
    print(f"Total: {len(usuarios)} usuario(s)")


def imprimir_cursos():
    cursos = Curso.query.order_by(Curso.id_curso.asc()).all()

    print("\nCURSOS")
    print("-" * 128)
    print(f"{'ID':<5} {'CÓDIGO':<14} {'ESTADO':<12} {'IDIOMA':<14} {'PROFESOR':<28} {'CURSO':<35} {'INSCRITOS':<10}")
    print("-" * 128)

    for curso in cursos:
        print(
            f"{curso.id_curso:<5} "
            f"{curso.codigo:<14} "
            f"{curso.estado_curso:<12} "
            f"{curso.idioma.nombre:<14} "
            f"{obtener_nombre_completo(curso.profesor.usuario):<28} "
            f"{curso.nombre:<35} "
            f"{contar_inscripciones_activas(curso.id_curso):<10}"
        )

    print("-" * 128)
    print(f"Total: {len(cursos)} curso(s)\n")


def obtener_rol(id_usuario):
    if db.session.get(Administrador, id_usuario):
        return "administrador"

    if db.session.get(Profesor, id_usuario):
        return "profesor"

    if db.session.get(Alumno, id_usuario):
        return "alumno"

    return "sin rol"


def obtener_estado(usuario):
    return "activo" if usuario.activo else "inactivo"


def obtener_nombre_completo(usuario):
    return f"{usuario.nombres} {usuario.apellido_paterno} {usuario.apellido_materno}"


def contar_inscripciones_activas(id_curso):
    return Inscripcion.query.filter_by(id_curso=id_curso, estado_inscripcion="activa").count()


app = create_app()

with app.app_context():
    ejecutar_consulta()
