from flask import Blueprint, render_template

from utils.auth import ROL_ALUMNO, rol_requerido, sesion_requerida

alumno_bp = Blueprint("alumno", __name__)


@alumno_bp.route("/dashboard")
@sesion_requerida
@rol_requerido(ROL_ALUMNO)
def dashboard():
    return render_template("alumno/dashboard.html")
