from flask import Blueprint, render_template, request, session, redirect, url_for
from models.Usuario import Usuario
from models.Alumno import Alumno
from models.Profesor import Profesor
from models.Administrador import Administrador
from models import db
from werkzeug.security import check_password_hash

login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('login.dashboard'))

    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')

        usuario = db.session.query(Usuario).filter_by(
            correo=correo
        ).first()

        if usuario and check_password_hash(usuario.password_hash, password):

            # Guardar en sesión (cookie)
            session['user_id'] = usuario.id_usuario

            # Detectar rol
            if db.session.get(Administrador, usuario.id_usuario):
                session['rol'] = 'administrador'
            elif db.session.get(Profesor, usuario.id_usuario):
                session['rol'] = 'profesor'
            elif db.session.get(Alumno, usuario.id_usuario):
                session['rol'] = 'alumno'

            return redirect(url_for('login.dashboard'))

        return render_template('error.html')

    return render_template('login.html')

@login_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    if session['rol'] == 'administrador':
        return render_template('admin.html')
    elif session['rol'] == 'profesor':
        return render_template('profesor.html')
    elif session['rol'] == 'alumno':
        return render_template('alumno.html')

    return render_template('error.html')
@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.login'))