from models.Material import Material
from tests.factories import (
    crear_curso,
    crear_idioma,
    crear_material,
    crear_profesor,
    iniciar_sesion,
)
from utils.auth import ROL_PROFESOR


def test_profesor_elimina_material_de_curso_propio(client):
    idioma = crear_idioma()
    profesor = crear_profesor()
    curso = crear_curso(profesor, idioma)
    material = crear_material(curso)

    iniciar_sesion(client, profesor, ROL_PROFESOR)

    respuesta = client.post(f"/profesor/cursos/{curso.id_curso}/materiales/{material.id_material}/eliminar")

    assert respuesta.status_code == 302
    assert material.visible is False


def test_profesor_no_elimina_material_de_otro_profesor(client):
    idioma = crear_idioma()
    profesor_dueno = crear_profesor(correo="dueno.material@sgci.test", numero_empleado="EMP-300",)
    profesor_intruso = crear_profesor(correo="intruso.material@sgci.test", numero_empleado="EMP-301",)
    curso = crear_curso(profesor_dueno, idioma)
    material = crear_material(curso)
    iniciar_sesion(client, profesor_intruso, ROL_PROFESOR)

    respuesta = client.post(f"/profesor/cursos/{curso.id_curso}/materiales/{material.id_material}/eliminar")

    assert respuesta.status_code == 403
    assert material.visible is True