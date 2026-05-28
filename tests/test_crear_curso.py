from models.Curso import Curso
from tests.factories import (
    crear_profesor,
    datos_formulario_curso,
    iniciar_sesion,
)
from utils.auth import ROL_PROFESOR


def test_profesor_crea_curso_en_estado_borrador(client, idioma):
    profesor = crear_profesor()
    iniciar_sesion(client, profesor, ROL_PROFESOR)

    respuesta = client.post(
        "/profesor/cursos/crear",
        data=datos_formulario_curso(
            idioma,
            codigo="ing-a1-200",
            nombre="Inglés intensivo A1",
            cupo_maximo="12",
        ),
    )

    curso = Curso.query.filter_by(codigo="ING-A1-200").one()
    assert respuesta.status_code == 302
    assert curso.id_profesor == profesor.id_usuario
    assert curso.estado_curso == "borrador"
    assert curso.cupo_maximo == 12


def test_profesor_no_crea_curso_con_idioma_invalido(client):
    profesor = crear_profesor()
    iniciar_sesion(client, profesor, ROL_PROFESOR)

    respuesta = client.post(
        "/profesor/cursos/crear",
        data={
            "codigo": "ING-A1-300",
            "nombre": "Curso inválido",
            "id_idioma": "999",
            "nivel_requerido": "1",
            "modalidad": "En línea",
            "cupo_maximo": "20",
        },
    )

    assert respuesta.status_code == 400
    assert Curso.query.filter_by(codigo="ING-A1-300").first() is None
