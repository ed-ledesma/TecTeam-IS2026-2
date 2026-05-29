from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from models import db
from models.Curso import Curso
from models.Idioma import Idioma
from models.Inscripcion import Inscripcion
from models.Material import Material

from utils.auth import (
    ROL_PROFESOR,
    obtener_id_usuario_autenticado,
    rol_requerido,
    sesion_requerida,
)

profesor_bp = Blueprint("profesor", __name__)

ESTADOS_CURSO = ("borrador", "publicado", "cerrado")
MODALIDADES_CURSO = ("En línea", "Presencial", "Mixta")


@profesor_bp.route("/dashboard")
@sesion_requerida
@rol_requerido(ROL_PROFESOR)
def dashboard():
    id_profesor = obtener_id_usuario_autenticado()
    cursos = Curso.query.filter_by(id_profesor=id_profesor).all()
    resumen = construir_resumen_cursos(cursos)
    cursos_recientes = sorted(cursos, key=lambda curso: curso.id_curso, reverse=True)[:5]

    return render_template(
        "profesor/dashboard.html",
        resumen=resumen,
        cursos_recientes=cursos_recientes,
    )


@profesor_bp.route("/cursos")
@sesion_requerida
@rol_requerido(ROL_PROFESOR)
def listar_cursos():
    estado_filtrado = request.args.get("estado", "").strip().lower()
    consulta = Curso.query.filter_by(id_profesor=obtener_id_usuario_autenticado())

    if estado_filtrado in ESTADOS_CURSO:
        consulta = consulta.filter_by(estado_curso=estado_filtrado)

    cursos = consulta.order_by(Curso.id_curso.desc()).all()
    return render_template(
        "profesor/cursos.html",
        cursos=cursos,
        estados=ESTADOS_CURSO,
        estado_filtrado=estado_filtrado,
    )


@profesor_bp.route("/cursos/crear", methods=["GET", "POST"])
@sesion_requerida
@rol_requerido(ROL_PROFESOR)
def crear_curso():
    idiomas = obtener_idiomas_disponibles()

    if request.method == "POST":
        datos = obtener_datos_formulario_curso()
        errores = validar_datos_para_crear_curso(datos)

        if errores:
            mostrar_errores(errores)
            return render_template(
                "profesor/formulario_curso.html",
                modo="crear",
                datos=datos,
                idiomas=idiomas,
                modalidades=MODALIDADES_CURSO,
            ), 400

        curso = construir_curso(datos)
        db.session.add(curso)

        if guardar_cambios():
            flash("Curso creado correctamente en estado borrador.", "success")
            return redirect(url_for("profesor.detalle_curso", id_curso=curso.id_curso))

        return render_template(
            "profesor/formulario_curso.html",
            modo="crear",
            datos=datos,
            idiomas=idiomas,
            modalidades=MODALIDADES_CURSO,
        ), 400

    return render_template(
        "profesor/formulario_curso.html",
        modo="crear",
        datos=datos_iniciales_curso(),
        idiomas=idiomas,
        modalidades=MODALIDADES_CURSO,
    )


@profesor_bp.route("/cursos/<int:id_curso>")
@sesion_requerida
@rol_requerido(ROL_PROFESOR)
def detalle_curso(id_curso):
    curso = obtener_curso_propio(id_curso)
    inscripciones_activas = contar_inscripciones_activas(curso.id_curso)

    materiales = Material.query.filter_by(
        id_curso=curso.id_curso,
    ).all()

    return render_template(
        "profesor/detalle_curso.html",
        curso=curso,
        inscripciones_activas=inscripciones_activas,
        materiales=materiales,
    )


@profesor_bp.route("/cursos/<int:id_curso>/editar", methods=["GET", "POST"])
@sesion_requerida
@rol_requerido(ROL_PROFESOR)
def editar_curso(id_curso):
    curso = obtener_curso_propio(id_curso)
    idiomas = obtener_idiomas_disponibles()

    if request.method == "POST":
        datos = obtener_datos_formulario_curso()
        errores = validar_datos_para_editar_curso(datos, curso)

        if errores:
            mostrar_errores(errores)
            return render_template(
                "profesor/formulario_curso.html",
                modo="editar",
                curso=curso,
                datos=datos,
                idiomas=idiomas,
                modalidades=MODALIDADES_CURSO,
            ), 400

        actualizar_curso(curso, datos)

        if guardar_cambios():
            flash("Curso actualizado correctamente.", "success")
            return redirect(url_for("profesor.detalle_curso", id_curso=curso.id_curso))

        return render_template(
            "profesor/formulario_curso.html",
            modo="editar",
            curso=curso,
            datos=datos,
            idiomas=idiomas,
            modalidades=MODALIDADES_CURSO,
        ), 400

    return render_template(
        "profesor/formulario_curso.html",
        modo="editar",
        curso=curso,
        datos=datos_desde_curso(curso),
        idiomas=idiomas,
        modalidades=MODALIDADES_CURSO,
    )


@profesor_bp.post("/cursos/<int:id_curso>/publicar")
@sesion_requerida
@rol_requerido(ROL_PROFESOR)
def publicar_curso(id_curso):
    curso = obtener_curso_propio(id_curso)

    if curso.estado_curso == "cerrado":
        flash("Un curso cerrado no puede publicarse nuevamente.", "error")
        return redirect(url_for("profesor.detalle_curso", id_curso=curso.id_curso))

    curso.estado_curso = "publicado"
    db.session.commit()
    flash("Curso publicado correctamente.", "success")
    return redirect(url_for("profesor.detalle_curso", id_curso=curso.id_curso))


@profesor_bp.post("/cursos/<int:id_curso>/cerrar")
@sesion_requerida
@rol_requerido(ROL_PROFESOR)
def cerrar_curso(id_curso):
    curso = obtener_curso_propio(id_curso)
    curso.estado_curso = "cerrado"
    db.session.commit()
    flash("Curso cerrado correctamente.", "success")
    return redirect(url_for("profesor.detalle_curso", id_curso=curso.id_curso))


@profesor_bp.route("/cursos/<int:id_curso>/materiales/crear", methods=["GET", "POST"])
@sesion_requerida
@rol_requerido(ROL_PROFESOR)
def crear_material(id_curso):
    curso = obtener_curso_propio(id_curso)

    tipos_material = (
        "PDF",
        "Documento",
        "Presentación",
        "Video",
        "Enlace",
        "Otro",
    )

    if request.method == "POST":
        datos = obtener_datos_formulario_material()
        errores = validar_datos_material(datos)

        if errores:
            mostrar_errores(errores)

            return render_template(
                "profesor/formulario_material.html",
                modo="crear",
                curso=curso,
                datos=datos,
                tipos_material=tipos_material,
            ), 400

        material = construir_material(curso, datos)

        db.session.add(material)

        if guardar_cambios_material():
            flash("Material agregado correctamente.", "success")

            return redirect(
                url_for(
                    "profesor.detalle_curso",
                    id_curso=curso.id_curso,
                )
            )

        return render_template(
            "profesor/formulario_material.html",
            modo="crear",
            curso=curso,
            datos=datos,
            tipos_material=tipos_material,
        ), 400

    return render_template(
        "profesor/formulario_material.html",
        modo="crear",
        curso=curso,
        datos=datos_iniciales_material(),
        tipos_material=tipos_material,
    )


@profesor_bp.route(
    "/cursos/<int:id_curso>/materiales/<int:id_material>/editar",
    methods=["GET", "POST"],
)
@sesion_requerida
@rol_requerido(ROL_PROFESOR)
def editar_material(id_curso, id_material):
    curso = obtener_curso_propio(id_curso)

    material = Material.query.filter_by(
        id_material=id_material,
        id_curso=curso.id_curso,
    ).first_or_404()

    tipos_material = (
        "PDF",
        "Documento",
        "Presentación",
        "Video",
        "Enlace",
        "Otro",
    )

    if request.method == "POST":
        datos = obtener_datos_formulario_material()
        errores = validar_datos_material(datos)

        if errores:
            mostrar_errores(errores)

            return render_template(
                "profesor/formulario_material.html",
                modo="editar",
                curso=curso,
                material=material,
                datos=datos,
                tipos_material=tipos_material,
            ), 400

        actualizar_material(material, datos)

        if guardar_cambios_material():
            flash("Material actualizado correctamente.", "success")

            return redirect(
                url_for(
                    "profesor.detalle_curso",
                    id_curso=curso.id_curso,
                )
            )

        return render_template(
            "profesor/formulario_material.html",
            modo="editar",
            curso=curso,
            material=material,
            datos=datos,
            tipos_material=tipos_material,
        ), 400

    return render_template(
        "profesor/formulario_material.html",
        modo="editar",
        curso=curso,
        material=material,
        datos=datos_desde_material(material),
        tipos_material=tipos_material,
    )


def obtener_datos_formulario_material():
    return {
        "titulo": request.form.get("titulo", "").strip(),
        "tipo_material": request.form.get("tipo_material", "").strip(),
        "url_archivo": request.form.get("url_archivo", "").strip(),
    }


def datos_iniciales_material():
    return {
        "titulo": "",
        "tipo_material": "",
        "url_archivo": "",
    }


def datos_desde_material(material):
    return {
        "titulo": material.titulo,
        "tipo_material": material.tipo_material or "",
        "url_archivo": material.url_archivo or "",
    }


def validar_datos_material(datos):
    errores = []

    if not datos["titulo"]:
        errores.append("El título del material es obligatorio.")

    if not datos["tipo_material"]:
        errores.append("El tipo de material es obligatorio.")

    if not datos["url_archivo"]:
        errores.append("La URL del archivo es obligatoria.")

    return errores


def construir_material(curso, datos):
    return Material(
        id_curso=curso.id_curso,
        titulo=datos["titulo"],
        tipo_material=datos["tipo_material"],
        url_archivo=datos["url_archivo"],
        visible=True,
    )


def actualizar_material(material, datos):
    material.titulo = datos["titulo"]
    material.tipo_material = datos["tipo_material"]
    material.url_archivo = datos["url_archivo"]


def guardar_cambios_material():
    try:
        db.session.commit()
        return True

    except IntegrityError:
        db.session.rollback()

        flash(
            "No fue posible guardar el material.",
            "error",
        )

        return False


def construir_resumen_cursos(cursos):
    return {
        "total": len(cursos),
        "borradores": contar_cursos_por_estado(cursos, "borrador"),
        "publicados": contar_cursos_por_estado(cursos, "publicado"),
        "cerrados": contar_cursos_por_estado(cursos, "cerrado"),
    }


def contar_cursos_por_estado(cursos, estado):
    return sum(1 for curso in cursos if curso.estado_curso == estado)


def obtener_idiomas_disponibles():
    return Idioma.query.order_by(Idioma.nombre.asc()).all()


def obtener_curso_propio(id_curso):
    curso = db.get_or_404(Curso, id_curso)

    if curso.id_profesor != obtener_id_usuario_autenticado():
        abort(403)

    return curso


def obtener_datos_formulario_curso():
    return {
        "codigo": request.form.get("codigo", "").strip().upper(),
        "nombre": request.form.get("nombre", "").strip(),
        "id_idioma": request.form.get("id_idioma", "").strip(),
        "nivel_requerido": request.form.get("nivel_requerido", "").strip(),
        "modalidad": request.form.get("modalidad", "").strip(),
        "cupo_maximo": request.form.get("cupo_maximo", "").strip(),
    }


def datos_iniciales_curso():
    return {
        "codigo": "",
        "nombre": "",
        "id_idioma": "",
        "nivel_requerido": "1",
        "modalidad": "En línea",
        "cupo_maximo": "",
    }


def datos_desde_curso(curso):
    return {
        "codigo": curso.codigo,
        "nombre": curso.nombre,
        "id_idioma": str(curso.id_idioma),
        "nivel_requerido": str(curso.nivel_requerido),
        "modalidad": curso.modalidad or "",
        "cupo_maximo": str(curso.cupo_maximo or ""),
    }


def validar_datos_para_crear_curso(datos):
    errores = validar_datos_comunes_curso(datos)

    if Curso.query.filter_by(codigo=datos["codigo"]).first():
        errores.append("Ya existe un curso con ese código.")

    return errores


def validar_datos_para_editar_curso(datos, curso):
    errores = validar_datos_comunes_curso(datos)
    curso_con_codigo = Curso.query.filter_by(codigo=datos["codigo"]).first()

    if curso_con_codigo and curso_con_codigo.id_curso != curso.id_curso:
        errores.append("Ya existe otro curso con ese código.")

    return errores


def validar_datos_comunes_curso(datos):
    errores = []

    if not datos["codigo"]:
        errores.append("El código del curso es obligatorio.")

    if not datos["nombre"]:
        errores.append("El nombre del curso es obligatorio.")

    if not obtener_idioma_por_id(datos["id_idioma"]):
        errores.append("El idioma seleccionado no es válido.")

    if convertir_entero_positivo(datos["nivel_requerido"]) is None:
        errores.append("El nivel requerido debe ser un número entero positivo.")

    if datos["modalidad"] and datos["modalidad"] not in MODALIDADES_CURSO:
        errores.append("La modalidad seleccionada no es válida.")

    if datos["cupo_maximo"] and convertir_entero_positivo(datos["cupo_maximo"]) is None:
        errores.append("El cupo máximo debe ser un número entero positivo.")

    return errores


def obtener_idioma_por_id(valor):
    id_idioma = convertir_entero_positivo(valor)

    if id_idioma is None:
        return None

    return db.session.get(Idioma, id_idioma)


def convertir_entero_positivo(valor):
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        return None

    if numero < 1:
        return None

    return numero


def construir_curso(datos):
    return Curso(
        id_profesor=obtener_id_usuario_autenticado(),
        id_idioma=convertir_entero_positivo(datos["id_idioma"]),
        codigo=datos["codigo"],
        nombre=datos["nombre"],
        nivel_requerido=convertir_entero_positivo(datos["nivel_requerido"]),
        modalidad=datos["modalidad"] or None,
        cupo_maximo=convertir_entero_positivo(datos["cupo_maximo"]),
        estado_curso="borrador",
    )


def actualizar_curso(curso, datos):
    curso.id_idioma = convertir_entero_positivo(datos["id_idioma"])
    curso.codigo = datos["codigo"]
    curso.nombre = datos["nombre"]
    curso.nivel_requerido = convertir_entero_positivo(datos["nivel_requerido"])
    curso.modalidad = datos["modalidad"] or None
    curso.cupo_maximo = convertir_entero_positivo(datos["cupo_maximo"])


def contar_inscripciones_activas(id_curso):
    return Inscripcion.query.filter_by(
        id_curso=id_curso,
        estado_inscripcion="activa",
    ).count()


def mostrar_errores(errores):
    for error in errores:
        flash(error, "error")


def guardar_cambios():
    try:
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        flash("No fue posible guardar el curso por datos duplicados o relacionados.", "error")
        return False
