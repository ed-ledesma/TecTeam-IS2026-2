from models import db
from models.Inscripcion import Inscripcion
from tests.factories import (
    crear_alumno,
    crear_curso,
    crear_idioma,
    crear_inscripcion,
    crear_profesor,
    iniciar_sesion,
)
from utils.auth import ROL_ALUMNO


def test_alumno_se_inscribe_a_curso_publicado_con_nivel_suficiente(client):
    idioma = crear_idioma()
    profesor = crear_profesor()
    alumno = crear_alumno(idioma=idioma, nivel=3)
    curso = crear_curso(profesor, idioma, estado="publicado", nivel_requerido=2)
    iniciar_sesion(client, alumno, ROL_ALUMNO)

    respuesta = client.post(f"/alumno/cursos/{curso.id_curso}/inscribir")

    inscripcion = Inscripcion.query.filter_by(
        id_alumno=alumno.id_usuario,
        id_curso=curso.id_curso,
        estado_inscripcion="activa",
    ).one()

    assert respuesta.status_code == 302
    assert respuesta.location.endswith(f"/alumno/cursos/{curso.id_curso}")
    assert inscripcion is not None


def test_alumno_no_duplica_inscripcion_activa(client):
    idioma = crear_idioma()
    profesor = crear_profesor()
    alumno = crear_alumno(idioma=idioma, nivel=3)
    curso = crear_curso(profesor, idioma, estado="publicado", nivel_requerido=1)
    crear_inscripcion(alumno, curso)
    db.session.commit()
    iniciar_sesion(client, alumno, ROL_ALUMNO)

    respuesta = client.post(f"/alumno/cursos/{curso.id_curso}/inscribir")

    total = Inscripcion.query.filter_by(
        id_alumno=alumno.id_usuario,
        id_curso=curso.id_curso,
    ).count()
    assert respuesta.status_code == 302
    assert total == 1
