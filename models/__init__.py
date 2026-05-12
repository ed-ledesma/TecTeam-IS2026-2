from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

from models.Usuario import Usuario
from models.Idioma import Idioma
from models.Administrador import Administrador
from models.Profesor import Profesor
from models.Alumno import Alumno
from models.Curso import Curso
from models.Inscripcion import Inscripcion
from models.Material import Material
from models.NivelAlumno import NivelAlumno
