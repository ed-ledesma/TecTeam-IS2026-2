from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from models import db
from models.Administrador import Administrador
from models.Alumno import Alumno
from models.Curso import Curso
from models.Inscripcion import Inscripcion
from models.Profesor import Profesor
from models.Usuario import Usuario
from utils.auth import (
    ROL_ADMINISTRADOR,
    ROL_ALUMNO,
    ROL_PROFESOR,
    encontrar_rol_de_usuario,
    rol_requerido,
    sesion_requerida,
)

admin_bp = Blueprint("admin", __name__)

ROLES_PERMITIDOS = (ROL_ADMINISTRADOR, ROL_PROFESOR, ROL_ALUMNO)


@admin_bp.route("/dashboard")
@sesion_requerida
@rol_requerido(ROL_ADMINISTRADOR)
def dashboard():
    resumen = {
        "usuarios": Usuario.query.count(),
        "usuarios_activos": Usuario.query.filter_by(activo=True).count(),
        "profesores": Profesor.query.count(),
        "alumnos": Alumno.query.count(),
        "cursos": Curso.query.count(),
        "inscripciones": Inscripcion.query.count(),
    }

    return render_template("admin/dashboard.html", resumen=resumen)


@admin_bp.route("/usuarios")
@sesion_requerida
@rol_requerido(ROL_ADMINISTRADOR)
def listar_usuarios():
    rol_filtrado = request.args.get("rol", "").strip().lower()
    usuarios = Usuario.query.order_by(Usuario.id_usuario.desc()).all()
    usuarios_con_rol = agregar_rol_a_usuarios(usuarios)

    if rol_filtrado in ROLES_PERMITIDOS:
        usuarios_con_rol = [
            usuario for usuario in usuarios_con_rol if usuario["rol"] == rol_filtrado
        ]

    return render_template(
        "admin/usuarios.html",
        usuarios=usuarios_con_rol,
        rol_filtrado=rol_filtrado,
        roles=ROLES_PERMITIDOS,
    )


@admin_bp.route("/profesores")
@sesion_requerida
@rol_requerido(ROL_ADMINISTRADOR)
def listar_profesores():
    profesores = Profesor.query.join(Usuario).order_by(Usuario.nombres.asc()).all()
    return render_template("admin/profesores.html", profesores=profesores)


@admin_bp.route("/alumnos")
@sesion_requerida
@rol_requerido(ROL_ADMINISTRADOR)
def listar_alumnos():
    alumnos = Alumno.query.join(Usuario).order_by(Usuario.nombres.asc()).all()
    return render_template("admin/alumnos.html", alumnos=alumnos)


@admin_bp.route("/usuarios/crear", methods=["GET", "POST"])
@sesion_requerida
@rol_requerido(ROL_ADMINISTRADOR)
def crear_usuario():
    if request.method == "POST":
        datos = obtener_datos_formulario_usuario()
        errores = validar_datos_para_crear_usuario(datos)

        if errores:
            mostrar_errores(errores)
            return render_template(
                "admin/formulario_usuario.html",
                modo="crear",
                datos=datos,
                roles=ROLES_PERMITIDOS,
            ), 400

        usuario = construir_usuario(datos)
        asignacion_rol = construir_asignacion_rol(datos)

        db.session.add(usuario)
        db.session.flush()
        asignacion_rol.id_usuario = usuario.id_usuario
        db.session.add(asignacion_rol)

        if guardar_cambios():
            flash("Usuario creado correctamente.", "success")
            return redirect(url_for("admin.listar_usuarios"))

        return render_template(
            "admin/formulario_usuario.html",
            modo="crear",
            datos=datos,
            roles=ROLES_PERMITIDOS,
        ), 400

    return render_template(
        "admin/formulario_usuario.html",
        modo="crear",
        datos=datos_iniciales_usuario(),
        roles=ROLES_PERMITIDOS,
    )


@admin_bp.route("/usuarios/<int:id_usuario>/editar", methods=["GET", "POST"])
@sesion_requerida
@rol_requerido(ROL_ADMINISTRADOR)
def editar_usuario(id_usuario):
    usuario = db.get_or_404(Usuario, id_usuario)
    rol_actual = encontrar_rol_de_usuario(usuario.id_usuario)

    if request.method == "POST":
        datos = obtener_datos_formulario_usuario()
        errores = validar_datos_para_editar_usuario(datos, usuario)

        if errores:
            mostrar_errores(errores)
            return render_template(
                "admin/formulario_usuario.html",
                modo="editar",
                usuario=usuario,
                rol_actual=rol_actual,
                datos=datos,
                roles=ROLES_PERMITIDOS,
            ), 400

        actualizar_usuario(usuario, datos)
        actualizar_asignacion_rol(usuario, rol_actual, datos)

        if guardar_cambios():
            flash("Usuario actualizado correctamente.", "success")
            return redirect(url_for("admin.listar_usuarios"))

        return render_template(
            "admin/formulario_usuario.html",
            modo="editar",
            usuario=usuario,
            rol_actual=rol_actual,
            datos=datos,
            roles=ROLES_PERMITIDOS,
        ), 400

    return render_template(
        "admin/formulario_usuario.html",
        modo="editar",
        usuario=usuario,
        rol_actual=rol_actual,
        datos=datos_desde_usuario(usuario, rol_actual),
        roles=ROLES_PERMITIDOS,
    )


@admin_bp.post("/usuarios/<int:id_usuario>/activar")
@sesion_requerida
@rol_requerido(ROL_ADMINISTRADOR)
def activar_usuario(id_usuario):
    usuario = db.get_or_404(Usuario, id_usuario)
    usuario.activo = True
    db.session.commit()
    flash("Usuario activado correctamente.", "success")
    return redirect(url_for("admin.listar_usuarios"))


@admin_bp.post("/usuarios/<int:id_usuario>/desactivar")
@sesion_requerida
@rol_requerido(ROL_ADMINISTRADOR)
def desactivar_usuario(id_usuario):
    usuario = db.get_or_404(Usuario, id_usuario)
    usuario.activo = False
    db.session.commit()
    flash("Usuario desactivado correctamente.", "success")
    return redirect(url_for("admin.listar_usuarios"))


def agregar_rol_a_usuarios(usuarios):
    return [
        {
            "usuario": usuario,
            "rol": encontrar_rol_de_usuario(usuario.id_usuario),
        }
        for usuario in usuarios
    ]


def obtener_datos_formulario_usuario():
    return {
        "nombres": request.form.get("nombres", "").strip(),
        "apellido_paterno": request.form.get("apellido_paterno", "").strip(),
        "apellido_materno": request.form.get("apellido_materno", "").strip(),
        "correo": request.form.get("correo", "").strip().lower(),
        "fecha_nacimiento": request.form.get("fecha_nacimiento", "").strip(),
        "password": request.form.get("password", ""),
        "rol": request.form.get("rol", "").strip().lower(),
        "matricula": request.form.get("matricula", "").strip(),
        "numero_empleado": request.form.get("numero_empleado", "").strip(),
        "especialidad": request.form.get("especialidad", "").strip(),
        "fecha_contratacion": request.form.get("fecha_contratacion", "").strip(),
        "nivel_acceso": request.form.get("nivel_acceso", "").strip(),
        "area_responsable": request.form.get("area_responsable", "").strip(),
    }


def datos_iniciales_usuario():
    return {
        "nombres": "",
        "apellido_paterno": "",
        "apellido_materno": "",
        "correo": "",
        "fecha_nacimiento": "",
        "password": "",
        "rol": ROL_ALUMNO,
        "matricula": "",
        "numero_empleado": "",
        "especialidad": "",
        "fecha_contratacion": "",
        "nivel_acceso": "1",
        "area_responsable": "",
    }


def datos_desde_usuario(usuario, rol):
    datos = datos_iniciales_usuario()
    datos.update(
        {
            "nombres": usuario.nombres,
            "apellido_paterno": usuario.apellido_paterno,
            "apellido_materno": usuario.apellido_materno,
            "correo": usuario.correo,
            "fecha_nacimiento": usuario.fecha_nacimiento.isoformat(),
            "rol": rol or "",
        }
    )

    if rol == ROL_ALUMNO:
        alumno = db.session.get(Alumno, usuario.id_usuario)
        datos["matricula"] = alumno.matricula if alumno else ""

    if rol == ROL_PROFESOR:
        profesor = db.session.get(Profesor, usuario.id_usuario)
        datos["numero_empleado"] = profesor.numero_empleado if profesor else ""
        datos["especialidad"] = profesor.especialidad if profesor else ""
        datos["fecha_contratacion"] = (
            profesor.fecha_contratacion.isoformat() if profesor else ""
        )

    if rol == ROL_ADMINISTRADOR:
        administrador = db.session.get(Administrador, usuario.id_usuario)
        datos["nivel_acceso"] = administrador.nivel_acceso if administrador else "1"
        datos["area_responsable"] = administrador.area_responsable if administrador else ""

    return datos


def validar_datos_para_crear_usuario(datos):
    errores = validar_datos_comunes(datos)

    if not datos["password"]:
        errores.append("La contraseña es obligatoria.")

    if Usuario.query.filter_by(correo=datos["correo"]).first():
        errores.append("Ya existe un usuario con ese correo.")

    errores.extend(validar_datos_de_rol(datos))
    return errores


def validar_datos_para_editar_usuario(datos, usuario):
    errores = validar_datos_comunes(datos)

    usuario_con_correo = Usuario.query.filter_by(correo=datos["correo"]).first()
    if usuario_con_correo and usuario_con_correo.id_usuario != usuario.id_usuario:
        errores.append("Ya existe otro usuario con ese correo.")

    errores.extend(validar_datos_de_rol(datos, usuario.id_usuario))
    return errores


def validar_datos_comunes(datos):
    errores = []

    if not datos["nombres"]:
        errores.append("El nombre es obligatorio.")

    if not datos["apellido_paterno"]:
        errores.append("El apellido paterno es obligatorio.")

    if not datos["apellido_materno"]:
        errores.append("El apellido materno es obligatorio.")

    if not datos["correo"]:
        errores.append("El correo es obligatorio.")

    if not convertir_fecha(datos["fecha_nacimiento"]):
        errores.append("La fecha de nacimiento no es válida.")

    if datos["rol"] not in ROLES_PERMITIDOS:
        errores.append("El rol seleccionado no es válido.")

    return errores


def validar_datos_de_rol(datos, id_usuario=None):
    if datos["rol"] == ROL_ALUMNO:
        return validar_datos_alumno(datos, id_usuario)

    if datos["rol"] == ROL_PROFESOR:
        return validar_datos_profesor(datos, id_usuario)

    if datos["rol"] == ROL_ADMINISTRADOR:
        return validar_datos_administrador(datos)

    return []


def validar_datos_alumno(datos, id_usuario=None):
    errores = []

    if not datos["matricula"]:
        errores.append("La matrícula es obligatoria para alumnos.")
        return errores

    alumno_con_matricula = Alumno.query.filter_by(matricula=datos["matricula"]).first()
    if alumno_con_matricula and alumno_con_matricula.id_usuario != id_usuario:
        errores.append("Ya existe un alumno con esa matrícula.")

    return errores


def validar_datos_profesor(datos, id_usuario=None):
    errores = []

    if not datos["numero_empleado"]:
        errores.append("El número de empleado es obligatorio para profesores.")

    if not convertir_fecha(datos["fecha_contratacion"]):
        errores.append("La fecha de contratación no es válida.")

    profesor_con_numero = Profesor.query.filter_by(
        numero_empleado=datos["numero_empleado"]
    ).first()
    if profesor_con_numero and profesor_con_numero.id_usuario != id_usuario:
        errores.append("Ya existe un profesor con ese número de empleado.")

    return errores


def validar_datos_administrador(datos):
    errores = []

    if not convertir_entero(datos["nivel_acceso"]):
        errores.append("El nivel de acceso debe ser un número entero positivo.")

    return errores


def construir_usuario(datos):
    return Usuario(
        nombres=datos["nombres"],
        apellido_paterno=datos["apellido_paterno"],
        apellido_materno=datos["apellido_materno"],
        correo=datos["correo"],
        fecha_nacimiento=convertir_fecha(datos["fecha_nacimiento"]),
        activo=True,
        password_hash=generate_password_hash(datos["password"]),
        ultimo_cambio_password=datetime.utcnow(),
    )


def actualizar_usuario(usuario, datos):
    usuario.nombres = datos["nombres"]
    usuario.apellido_paterno = datos["apellido_paterno"]
    usuario.apellido_materno = datos["apellido_materno"]
    usuario.correo = datos["correo"]
    usuario.fecha_nacimiento = convertir_fecha(datos["fecha_nacimiento"])

    if datos["password"]:
        usuario.password_hash = generate_password_hash(datos["password"])
        usuario.ultimo_cambio_password = datetime.utcnow()


def construir_asignacion_rol(datos):
    rol = datos["rol"]

    if rol == ROL_ALUMNO:
        return Alumno(matricula=datos["matricula"])

    if rol == ROL_PROFESOR:
        return Profesor(
            numero_empleado=datos["numero_empleado"],
            especialidad=datos["especialidad"] or None,
            fecha_contratacion=convertir_fecha(datos["fecha_contratacion"]),
        )

    if rol == ROL_ADMINISTRADOR:
        return Administrador(
            nivel_acceso=convertir_entero(datos["nivel_acceso"]),
            area_responsable=datos["area_responsable"] or None,
        )

    raise ValueError("Rol no válido")


def actualizar_asignacion_rol(usuario, rol_actual, datos):
    rol_nuevo = datos["rol"]

    if rol_actual != rol_nuevo:
        eliminar_asignacion_rol(usuario.id_usuario, rol_actual)
        asignacion_rol = construir_asignacion_rol(datos)
        asignacion_rol.id_usuario = usuario.id_usuario
        db.session.add(asignacion_rol)
    else:
        asignar_datos_especificos_de_rol(usuario.id_usuario, rol_nuevo, datos)


def eliminar_asignacion_rol(id_usuario, rol):
    if rol == ROL_ALUMNO:
        alumno = db.session.get(Alumno, id_usuario)
        if alumno:
            db.session.delete(alumno)

    if rol == ROL_PROFESOR:
        profesor = db.session.get(Profesor, id_usuario)
        if profesor:
            db.session.delete(profesor)

    if rol == ROL_ADMINISTRADOR:
        administrador = db.session.get(Administrador, id_usuario)
        if administrador:
            db.session.delete(administrador)



def asignar_datos_especificos_de_rol(id_usuario, rol, datos):
    if rol == ROL_ALUMNO:
        alumno = db.session.get(Alumno, id_usuario)
        alumno.matricula = datos["matricula"]

    if rol == ROL_PROFESOR:
        profesor = db.session.get(Profesor, id_usuario)
        profesor.numero_empleado = datos["numero_empleado"]
        profesor.especialidad = datos["especialidad"] or None
        profesor.fecha_contratacion = convertir_fecha(datos["fecha_contratacion"])

    if rol == ROL_ADMINISTRADOR:
        administrador = db.session.get(Administrador, id_usuario)
        administrador.nivel_acceso = convertir_entero(datos["nivel_acceso"])
        administrador.area_responsable = datos["area_responsable"] or None


def convertir_fecha(valor):
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def convertir_entero(valor):
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        return None

    if numero < 1:
        return None

    return numero


def mostrar_errores(errores):
    for error in errores:
        flash(error, "error")


def guardar_cambios():
    try:
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        flash(
            "No fue posible guardar los cambios porque existen datos relacionados o duplicados.",
            "error",
        )
        return False
