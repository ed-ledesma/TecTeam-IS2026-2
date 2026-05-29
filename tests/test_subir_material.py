from models.Material import Material
from tests.factories import (
    crear_profesor,
    crear_curso,
    iniciar_sesion,
)
from utils.auth import ROL_PROFESOR


def test_profesor_sube_material_a_curso(client, idioma):
    profesor = crear_profesor()
    iniciar_sesion(client, profesor, ROL_PROFESOR)
    curso = crear_curso(profesor=profesor, idioma=idioma, codigo="ING-A1-500",)

    respuesta = client.post(
        f"/profesor/cursos/{curso.id_curso}/materiales/crear",
        data={
            "titulo": "Guía unidad 1",
            "tipo_material": "PDF",
            "url_archivo": "https://example.com/guia.pdf",
        },
    )

    material = Material.query.filter_by(titulo="Guía unidad 1",).one()
    assert respuesta.status_code == 302
    assert material.id_curso == curso.id_curso
    assert material.tipo_material == "PDF"
    assert material.url_archivo == "https://example.com/guia.pdf"
    assert material.visible is True


def test_profesor_no_sube_material_con_datos_invalidos(client, idioma):
    profesor = crear_profesor()
    curso = crear_curso(
        profesor=profesor,
        idioma=idioma,
    )

    iniciar_sesion(client, profesor, ROL_PROFESOR)

    respuesta = client.post(
        f"/profesor/cursos/{curso.id_curso}/materiales/crear",
        data={
            "titulo": "",
            "tipo_material": "",
            "url_archivo": "",
        },
    )

    assert respuesta.status_code == 400
    assert Material.query.count() == 0