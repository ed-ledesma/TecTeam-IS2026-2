from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from models import db
from models.Curso import Curso
from models.Idioma import Idioma
from models.Inscripcion import Inscripcion
from models.NivelAlumno import NivelAlumno

from utils.auth import (
    ROL_ALUMNO,
    obtener_id_usuario_autenticado,
    rol_requerido,
    sesion_requerida,
)
alumno_bp = Blueprint("alumno", __name__)

# Dashboard inicial
@alumno_bp.route("/dashboard")
@sesion_requerida
@rol_requerido(ROL_ALUMNO)
def dashboard():
    id_alumno = obtener_id_usuario_autenticado()

    cursos = Curso.query.filter_by(
        estado_curso="publicado"
    ).all()

    for curso in cursos:
        curso.esta_inscrito = Inscripcion.query.filter_by(
            id_curso=curso.id_curso,
            id_alumno=id_alumno,
            estado_inscripcion="activa",
        ).first() is not None

    return render_template(
        "alumno/dashboard.html",
        cursos=cursos,
    )

# Mostrar cursos inscritos
@alumno_bp.route("/cursos")
@sesion_requerida
@rol_requerido(ROL_ALUMNO)
def listar_cursos():
    estado_filtrado = request.args.get("estado", "").strip().lower()

    consulta = (
        Curso.query
        .join(Inscripcion, Inscripcion.id_curso == Curso.id_curso)
        .filter(Inscripcion.id_alumno == obtener_id_usuario_autenticado())
    )

    cursos = consulta.order_by(Curso.id_curso.desc()).all()

    return render_template(
        "alumno/cursos.html",
        cursos=cursos,
    )

# Detalle del curso
@alumno_bp.route("/cursos/<int:id_curso>")
@sesion_requerida
@rol_requerido(ROL_ALUMNO)
def detalle_curso(id_curso):
    id_alumno = obtener_id_usuario_autenticado()

    curso = Curso.query.get_or_404(id_curso)

    lugares_disponibles = contar_lugares_disponibles(curso.id_curso)

    esta_inscrito = Inscripcion.query.filter_by(
        id_curso=curso.id_curso,
        id_alumno=id_alumno,
        estado_inscripcion="activa",
    ).first() is not None

    return render_template(
        "alumno/detalle_curso.html",
        curso=curso,
        lugares_disponibles=lugares_disponibles,
        esta_inscrito=esta_inscrito,
    )

# Inscribirse a un curso
@alumno_bp.route("/cursos/<int:id_curso>/inscribir", methods=["POST"])
@sesion_requerida
@rol_requerido(ROL_ALUMNO)
def inscribir_curso(id_curso):
    id_alumno = obtener_id_usuario_autenticado()

    curso = Curso.query.get_or_404(id_curso)

    # Verificar si ya está inscrito
    inscripcion_existente = Inscripcion.query.filter_by(
        id_curso=curso.id_curso,
        id_alumno=id_alumno,
        estado_inscripcion="activa",
    ).first()

    if inscripcion_existente:
        flash("Ya estás inscrito en este curso.", "warning")
        return redirect(url_for("alumno.detalle_curso", id_curso=curso.id_curso))

    # Verificar cupo disponible
    if curso.cupo_maximo is not None:
        inscripciones_activas = Inscripcion.query.filter_by(
            id_curso=curso.id_curso,
            estado_inscripcion="activa",
        ).count()

        if inscripciones_activas >= curso.cupo_maximo:
            flash("No hay lugares disponibles en este curso.", "error")
            return redirect(url_for("alumno.detalle_curso", id_curso=curso.id_curso))

    # Verificar nivel del alumno
    nivel_alumno = NivelAlumno.query.filter_by(
        id_usuario=id_alumno,
        id_idioma=curso.id_idioma,
    ).first()

    if not nivel_alumno:
        flash("No tienes nivel registrado para este idioma.", "error")
        return redirect(url_for("alumno.detalle_curso", id_curso=curso.id_curso))

    if nivel_alumno.nivel < curso.nivel_requerido:
        flash("Tu nivel no es suficiente para este curso.", "error")
        return redirect(url_for("alumno.detalle_curso", id_curso=curso.id_curso))

    nueva_inscripcion = Inscripcion(
        id_alumno=id_alumno,
        id_curso=curso.id_curso,
        estado_inscripcion="activa",
    )

    db.session.add(nueva_inscripcion)
    db.session.commit()

    flash("Te has inscrito correctamente al curso.", "success")

    return redirect(url_for("alumno.detalle_curso", id_curso=curso.id_curso))


def contar_lugares_disponibles(id_curso):
    curso = Curso.query.get_or_404(id_curso)

    inscripciones_activas = Inscripcion.query.filter_by(
        id_curso=id_curso,
        estado_inscripcion="activa",
    ).count()

    if curso.cupo_maximo is None:
        return "Sin límite"

    return max(curso.cupo_maximo - inscripciones_activas, 0)