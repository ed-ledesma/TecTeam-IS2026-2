from functools import wraps

from flask import abort, redirect, session, url_for

from models.Administrador import Administrador
from models.Alumno import Alumno
from models.Profesor import Profesor
from models import db

USUARIO_SESION = "user_id"
ROL_SESION = "rol"
ROL_ADMINISTRADOR = "administrador"
ROL_PROFESOR = "profesor"
ROL_ALUMNO = "alumno"

RUTA_DASHBOARD_POR_ROL = {
    ROL_ADMINISTRADOR: "admin.dashboard",
    ROL_PROFESOR: "profesor.dashboard",
    ROL_ALUMNO: "alumno.dashboard",
}


def encontrar_rol_de_usuario(id_usuario):
    if db.session.get(Administrador, id_usuario):
        return ROL_ADMINISTRADOR

    if db.session.get(Profesor, id_usuario):
        return ROL_PROFESOR

    if db.session.get(Alumno, id_usuario):
        return ROL_ALUMNO

    return None


def guardar_usuario_en_sesion(usuario, rol):
    session.clear()
    session[USUARIO_SESION] = usuario.id_usuario
    session[ROL_SESION] = rol


def cerrar_sesion_actual():
    session.clear()


def hay_usuario_autenticado():
    return USUARIO_SESION in session


def obtener_id_usuario_autenticado():
    return session.get(USUARIO_SESION)


def obtener_rol_usuario_autenticado():
    return session.get(ROL_SESION)


def obtener_ruta_dashboard_por_rol(rol):
    return RUTA_DASHBOARD_POR_ROL.get(rol)


def redirigir_a_dashboard_por_rol(rol):
    ruta_dashboard = obtener_ruta_dashboard_por_rol(rol)

    if ruta_dashboard is None:
        abort(403)

    return redirect(url_for(ruta_dashboard))


def sesion_requerida(vista):
    @wraps(vista)
    def vista_protegida(*args, **kwargs):
        if not hay_usuario_autenticado():
            return redirect(url_for("login.login"))

        if obtener_rol_usuario_autenticado() is None:
            cerrar_sesion_actual()
            return redirect(url_for("login.login"))

        return vista(*args, **kwargs)

    return vista_protegida


def rol_requerido(*roles_permitidos):
    def proteger_vista(vista):
        @wraps(vista)
        def vista_protegida(*args, **kwargs):
            if not hay_usuario_autenticado():
                return redirect(url_for("login.login"))

            if obtener_rol_usuario_autenticado() not in roles_permitidos:
                abort(403)

            return vista(*args, **kwargs)

        return vista_protegida

    return proteger_vista
