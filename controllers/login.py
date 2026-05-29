from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash

from models import db
from models.Usuario import Usuario
from utils.auth import (
    cerrar_sesion_actual,
    encontrar_rol_de_usuario,
    guardar_usuario_en_sesion,
    hay_usuario_autenticado,
    obtener_rol_usuario_autenticado,
    redirigir_a_dashboard_por_rol,
    sesion_requerida,
)

login_bp = Blueprint("login", __name__)


@login_bp.route("/", methods=["GET", "POST"])
@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if hay_usuario_autenticado():
        return redirigir_a_dashboard_por_rol(obtener_rol_usuario_autenticado())

    if request.method == "POST":
        correo = request.form.get("correo", "").strip().lower()
        password = request.form.get("password", "")

        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario is None or not check_password_hash(usuario.password_hash, password):
            return render_template(
                "error.html",
                titulo="Credenciales inválidas",
                mensaje="El correo o la contraseña no son correctos.",
                enlace=url_for("login.login"),
                texto_enlace="Volver al login",
            ), 401

        if not usuario.activo:
            return render_template(
                "error.html",
                titulo="Usuario inactivo",
                mensaje="Tu usuario está inactivo. Contacta al administrador del sistema.",
                enlace=url_for("login.login"),
                texto_enlace="Volver al login",
            ), 403

        rol = encontrar_rol_de_usuario(usuario.id_usuario)

        if rol is None:
            return render_template(
                "error.html",
                titulo="Usuario sin rol",
                mensaje="Tu usuario no tiene un rol asignado en el sistema.",
                enlace=url_for("login.login"),
                texto_enlace="Volver al login",
            ), 403

        usuario.ultimo_acceso = datetime.utcnow()
        db.session.commit()
        guardar_usuario_en_sesion(usuario, rol)

        return redirigir_a_dashboard_por_rol(rol)

    return render_template("login.html")


@login_bp.route("/dashboard")
@sesion_requerida
def dashboard():
    return redirigir_a_dashboard_por_rol(obtener_rol_usuario_autenticado())


@login_bp.route("/logout")
def logout():
    cerrar_sesion_actual()
    return redirect(url_for("login.login"))
