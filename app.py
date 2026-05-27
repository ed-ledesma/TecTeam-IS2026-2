import os

from dotenv import load_dotenv
from flask import Flask, render_template
from sqlalchemy import URL

from controllers.admin import admin_bp
from controllers.alumno import alumno_bp
from controllers.login import login_bp
from controllers.profesor import profesor_bp
from models import db

load_dotenv(override=True)


def create_app(config_overrides=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = crear_uri_base_datos()
    app.config["SECRET_KEY"] = obtener_clave_secreta()

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    registrar_blueprints(app)
    registrar_manejadores_de_error(app)

    return app


def crear_uri_base_datos():
    return URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT", 3306)),
        database=os.getenv("DATABASE"),
    )


def obtener_clave_secreta():
    clave_secreta = os.getenv("SECRET_KEY")

    if not clave_secreta:
        raise ValueError("SECRET_KEY no está definida")

    return clave_secreta


def registrar_blueprints(app):
    app.register_blueprint(login_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(profesor_bp, url_prefix="/profesor")
    app.register_blueprint(alumno_bp, url_prefix="/alumno")


def registrar_manejadores_de_error(app):
    app.register_error_handler(403, acceso_no_autorizado)
    app.register_error_handler(404, recurso_no_encontrado)


def acceso_no_autorizado(error):
    return render_template(
        "error.html",
        titulo="Acceso no autorizado",
        mensaje="No tienes permisos para acceder a esta sección.",
        enlace="/dashboard",
        texto_enlace="Volver a mi panel",
    ), 403


def recurso_no_encontrado(error):
    return render_template(
        "error.html",
        titulo="Página no encontrada",
        mensaje="La página o recurso solicitado no existe.",
        enlace="/dashboard",
        texto_enlace="Volver a mi panel",
    ), 404


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
