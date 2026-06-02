from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from models import db
from models.Usuario import Usuario
from models.Alumno import Alumno
from models.Idioma import Idioma
from models.NivelAlumno import NivelAlumno
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


@login_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombres = request.form.get("nombres", "").strip()
        apellido_paterno = request.form.get("apellido_paterno", "").strip()
        apellido_materno = request.form.get("apellido_materno", "").strip()
        correo = request.form.get("correo", "").strip().lower()
        password = request.form.get("password", "")
        fecha_nacimiento = request.form.get("fecha_nacimiento")

        if Usuario.query.filter_by(correo=correo).first():
            return render_template(
                "error.html",
                titulo="Correo existente",
                mensaje="Ya existe una cuenta con ese correo."
            ), 400

        usuario = Usuario(
            nombres=nombres,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            correo=correo,
            fecha_nacimiento=datetime.strptime(
                fecha_nacimiento,
                "%Y-%m-%d"
            ).date(),
            activo=True,
            password_hash=generate_password_hash(password)
        )

        db.session.add(usuario)
        db.session.flush()

        alumno = Alumno(
            id_usuario=usuario.id_usuario,
            matricula=f"ALU-{usuario.id_usuario:03d}"
        )

        db.session.add(alumno)

        idiomas = Idioma.query.all()

        for idioma in idiomas:
            db.session.add(
                NivelAlumno(
                    id_usuario=usuario.id_usuario,
                    id_idioma=idioma.id_idioma,
                    nivel=1,
                )
            )

        db.session.commit()

        return redirect(url_for("login.login"))

    return render_template("registro.html")


@login_bp.route("/logout")
def logout():
    cerrar_sesion_actual()
    return redirect(url_for("login.login"))
