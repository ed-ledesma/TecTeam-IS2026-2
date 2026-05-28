from tests.factories import (
    crear_alumno,
    crear_curso,
    crear_idioma,
    crear_material,
    crear_profesor,
    iniciar_sesion,
)
from utils.auth import ROL_ALUMNO


def test_alumno_consulta_material_visible_de_un_curso_publicado(client):
    idioma = crear_idioma()
    profesor = crear_profesor()
    alumno = crear_alumno(idioma=idioma)
    curso = crear_curso(profesor, idioma, estado="publicado")
    crear_material(curso, titulo="Guía de bienvenida", visible=True)
    crear_material(curso, titulo="Material oculto", visible=False)
    iniciar_sesion(client, alumno, ROL_ALUMNO)

    respuesta = client.get(f"/alumno/cursos/{curso.id_curso}")

    assert respuesta.status_code == 200
    assert "Guía de bienvenida".encode() in respuesta.data
    assert b"Material oculto" not in respuesta.data
