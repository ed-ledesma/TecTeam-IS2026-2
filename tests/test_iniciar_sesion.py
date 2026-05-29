import pytest

from models.Usuario import Usuario
from tests.factories import crear_administrador, crear_alumno, crear_profesor


@pytest.mark.parametrize(
    ("crear_rol", "correo", "ruta_esperada"),
    [
        (crear_alumno, "alumno.login@sgci.test", "/alumno/dashboard"),
        (crear_profesor, "profesor.login@sgci.test", "/profesor/dashboard"),
        (crear_administrador, "admin.login@sgci.test", "/admin/dashboard"),
    ],
)
def test_iniciar_sesion_redirige_al_dashboard_segun_rol(client, crear_rol, correo, ruta_esperada):
    crear_rol(correo=correo, password="Password123")

    respuesta = client.post(
        "/login",
        data={"correo": correo.upper(), "password": "Password123"},
    )

    assert respuesta.status_code == 302
    assert respuesta.location.endswith(ruta_esperada)


def test_iniciar_sesion_rechaza_credenciales_invalidas(client):
    crear_alumno(correo="alumno.invalidas@sgci.test", password="Password123")

    respuesta = client.post(
        "/login",
        data={"correo": "alumno.invalidas@sgci.test", "password": "incorrecta"},
    )

    assert respuesta.status_code == 401
    assert b"Credenciales inv" in respuesta.data


def test_iniciar_sesion_rechaza_usuario_inactivo(client):
    crear_profesor(correo="profesor.inactivo@sgci.test", password="Password123", activo=False)

    respuesta = client.post(
        "/login",
        data={"correo": "profesor.inactivo@sgci.test", "password": "Password123"},
    )

    usuario = Usuario.query.filter_by(correo="profesor.inactivo@sgci.test").one()
    assert respuesta.status_code == 403
    assert usuario.ultimo_acceso is None
