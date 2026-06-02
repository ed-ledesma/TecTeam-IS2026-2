# SGCI — Sistema de Gestión de Cursos de Idiomas

SGCI es una aplicación web desarrollada con **Python**, **Flask**, **SQLAlchemy** y **MySQL** para administrar cursos de idiomas. El sistema maneja usuarios con roles, cursos, profesores, alumnos, inscripciones y materiales didácticos.

El proyecto está organizado para trabajar por sprints. En el estado actual, la aplicación permite autenticación, control de acceso por rol, gestión administrativa de usuarios y gestión de cursos por parte del profesor.

---

## Tabla de contenido

- [Tecnologías usadas](#tecnologías-usadas)
- [Funcionalidades disponibles](#funcionalidades-disponibles)
- [Requisitos previos](#requisitos-previos)
- [Instalación desde cero](#instalación-desde-cero)
- [Configuración del archivo .env](#configuración-del-archivo-env)
- [Creación de la base de datos](#creación-de-la-base-de-datos)
- [Poblar datos de prueba](#poblar-datos-de-prueba)
- [Ejecutar la aplicación](#ejecutar-la-aplicación)
- [Credenciales de prueba](#credenciales-de-prueba)
- [Cómo probar el sistema](#cómo-probar-el-sistema)
- [Tests automatizados](#tests-automatizados)
- [Scripts útiles](#scripts-útiles)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Rutas principales](#rutas-principales)
- [Modelo general de datos](#modelo-general-de-datos)
- [Reglas de negocio implementadas](#reglas-de-negocio-implementadas)
- [Problemas comunes](#problemas-comunes)
- [Estado actual del proyecto](#estado-actual-del-proyecto)

---

## Tecnologías usadas

- Python 3.10 o superior
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- PyMySQL
- Werkzeug
- python-dotenv
- MySQL
- Pytest
- HTML, CSS y Jinja2

---

## Funcionalidades disponibles

### Administrador

El administrador puede:

- iniciar sesión;
- acceder a su dashboard administrativo;
- listar usuarios;
- crear administradores, profesores y alumnos;
- editar usuarios;
- activar y desactivar usuarios;
- consultar profesores registrados;
- consultar alumnos registrados.

### Profesor

El profesor puede:

- iniciar sesión;
- acceder a su dashboard;
- consultar sus cursos;
- crear cursos;
- editar cursos propios;
- ver el detalle de sus cursos;
- publicar cursos;
- cerrar cursos.

### Alumno

El alumno actualmente puede:

- iniciar sesión;
- acceder a su dashboard inicial.

Las funciones de inscripción, consulta de cursos disponibles y consulta de materiales están planeadas para los siguientes sprints.

---

## Requisitos previos

Antes de levantar el proyecto, asegúrate de tener instalado:

1. **Python 3.10 o superior**
2. **MySQL Server**
3. **MySQL Workbench**, DBeaver o cualquier cliente para ejecutar SQL
4. Git, si vas a clonar la repo
5. Un editor de código, por ejemplo VS Code

Puedes verificar Python con:

```bash
python --version
```

En algunos sistemas el comando puede ser:

```bash
python3 --version
```

Puedes verificar MySQL entrando a tu cliente o ejecutando:

```bash
mysql --version
```

---

## Instalación desde cero

### 1. Clonar o descargar el proyecto

Si tienes la repo en GitHub:

```bash
git clone URL_DE_TU_REPOSITORIO
cd NOMBRE_DE_LA_CARPETA
```

Si descargaste un ZIP, descomprímelo y entra a la carpeta raíz del proyecto, donde se encuentra el archivo `app.py`.

---

### 2. Crear un entorno virtual

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Windows CMD

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

Cuando el entorno virtual esté activo, deberías ver algo como esto al inicio de la terminal:

```text
(.venv)
```

---

### 3. Actualizar pip

```bash
python -m pip install --upgrade pip
```

---

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

Si todo sale bien, Flask, SQLAlchemy, PyMySQL y las demás dependencias quedarán instaladas dentro del entorno virtual.

---

## Configuración del archivo .env

El proyecto usa variables de entorno para conectarse a la base de datos y configurar la clave secreta de Flask.

Crea un archivo llamado `.env` en la raíz del proyecto, al mismo nivel que `app.py`.

Ejemplo:

```env
USERNAME=root
PASSWORD=tu_password_de_mysql
HOST=localhost
PORT=3306
DATABASE=sgci_db
SECRET_KEY=sgci_desarrollo_2026

ADMIN_CORREO=admin@sgci.com
ADMIN_PASSWORD=Admin12345

PROFESOR_CORREO=profesor@sgci.com
PROFESOR_PASSWORD=Profesor12345

ALUMNO_CORREO=alumno@sgci.com
ALUMNO_PASSWORD=Alumno12345
```

Si tu usuario `root` de MySQL no tiene contraseña, deja `PASSWORD` vacío:

```env
USERNAME=root
PASSWORD=
HOST=localhost
PORT=3306
DATABASE=sgci_db
SECRET_KEY=sgci_desarrollo_2026
```

> No subas el archivo `.env` a GitHub. Este archivo contiene credenciales locales.

---

## Creación de la base de datos

El proyecto incluye un archivo llamado:

```text
DB.sql
```

Este archivo crea las tablas principales del sistema.

### Opción A: desde MySQL Workbench o DBeaver

1. Abre tu cliente de base de datos.
2. Conéctate a MySQL.
3. Crea la base de datos:

```sql
CREATE DATABASE sgci_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

4. Selecciona la base de datos:

```sql
USE sgci_db;
```

5. Abre el archivo `DB.sql`.
6. Ejecuta todo el script.

---

### Opción B: desde terminal

Desde la raíz del proyecto, ejecuta:

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS sgci_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

Luego ejecuta el script:

```bash
mysql -u root -p sgci_db < DB.sql
```

Si tu usuario no tiene contraseña:

```bash
mysql -u root -e "CREATE DATABASE IF NOT EXISTS sgci_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root sgci_db < DB.sql
```

---

## Poblar datos de prueba

Después de crear la base de datos y las tablas, ejecuta el script de población:

```bash
python scripts/poblar_datos_prueba.py
```

Este script crea:

- un administrador;
- un profesor;
- un alumno;
- idiomas de prueba;
- cursos de prueba;
- materiales de prueba;
- una inscripción inicial;
- niveles iniciales del alumno.

El script también genera contraseñas usando hash seguro mediante Werkzeug. No inserta contraseñas en texto plano en la base de datos.

---

## Ejecutar la aplicación

Desde la raíz del proyecto, con el entorno virtual activo:

```bash
python app.py
```

La aplicación se levantará normalmente en:

```text
http://127.0.0.1:5000
```

También puedes entrar directamente al login:

```text
http://127.0.0.1:5000/login
```

---

## Credenciales de prueba

Si ejecutaste `scripts/poblar_datos_prueba.py`, puedes usar estas credenciales:

| Rol | Correo | Contraseña |
|---|---|---|
| Administrador | `admin@sgci.com` | `Admin12345` |
| Profesor | `profesor@sgci.com` | `Profesor12345` |
| Alumno | `alumno@sgci.com` | `Alumno12345` |

---

## Cómo probar el sistema

### 1. Probar login

Entra a:

```text
http://127.0.0.1:5000/login
```

Prueba iniciar sesión con cada usuario de prueba.

---

### 2. Probar administrador

Usa:

```text
admin@sgci.com
Admin12345
```

Después de iniciar sesión, deberías entrar al dashboard del administrador.

Rutas para probar:

```text
/admin/dashboard
/admin/usuarios
/admin/usuarios/crear
/admin/profesores
/admin/alumnos
```

Pruebas recomendadas:

- crear un alumno nuevo;
- crear un profesor nuevo;
- editar un usuario existente;
- desactivar un usuario;
- activar un usuario;
- verificar que profesores y alumnos aparecen en sus listados correspondientes.

---

### 3. Probar profesor

Usa:

```text
profesor@sgci.com
Profesor12345
```

Rutas para probar:

```text
/profesor/dashboard
/profesor/cursos
/profesor/cursos/crear
```

Pruebas recomendadas:

- crear un curso nuevo;
- verificar que el curso inicia como `borrador`;
- editar el curso;
- publicar el curso;
- cerrar el curso;
- intentar acceder a cursos de otro profesor si existen.

---

### 4. Probar alumno

Usa:

```text
alumno@sgci.com
Alumno12345
```

Ruta disponible actualmente:

```text
/alumno/dashboard
```

Las vistas de cursos disponibles, inscripción y materiales del alumno están pendientes para el siguiente sprint.

---

### 5. Probar control de acceso

Con sesión de alumno, intenta entrar a:

```text
/admin/dashboard
```

El sistema debe responder con error **403 Acceso no autorizado**.

Con sesión de profesor, intenta entrar a:

```text
/admin/usuarios
```

El sistema también debe bloquear el acceso.

Si entras a una ruta privada sin iniciar sesión, el sistema debe redirigirte al login.

---

## Tests automatizados

El proyecto incluye una suite de pruebas automatizadas con **pytest**. Estas pruebas cubren los casos de uso que ya están integrados en el sistema, excepto **Subir material**, que se mantiene pendiente según el estado actual del proyecto.

### Casos de uso cubiertos

Cada caso de uso tiene su propio archivo dentro de la carpeta `tests/`:

| Caso de uso | Archivo de test |
|---|---|
| Iniciar sesión | `tests/test_iniciar_sesion.py` |
| Crear cuenta | `tests/test_crear_cuenta.py` |
| Inscribir curso | `tests/test_inscribir_curso.py` |
| Consultar material | `tests/test_consultar_material.py` |
| Crear curso | `tests/test_crear_curso.py` |
| Publicar curso | `tests/test_publicar_curso.py` |
| Cerrar curso | `tests/test_cerrar_eliminar_curso.py` |
| Crear profesor | `tests/test_crear_profesor.py` |
| Consultar profesor | `tests/test_consultar_profesor.py` |
| Actualizar profesor | `tests/test_actualizar_profesor.py` |
| Eliminar profesor | `tests/test_eliminar_profesor.py` |
| Eliminar cuentas | `tests/test_eliminar_cuentas.py` |

> En el estado actual del sistema, "eliminar profesor" y "eliminar cuentas" se prueban como **desactivación de usuarios**, porque la aplicación no elimina físicamente esos registros.

### Cómo ejecutar los tests

Desde la raíz del proyecto, activa tu entorno virtual e instala las dependencias:

```bash
pip install -r requirements.txt
```

Luego ejecuta:

```bash
pytest
```

También puedes ejecutar un archivo específico:

```bash
pytest tests/test_iniciar_sesion.py
```

O ejecutar una prueba específica dentro de un archivo:

```bash
pytest tests/test_iniciar_sesion.py::test_login_admin_redirige_al_dashboard_admin
```

### Cómo funcionan

Los tests usan el cliente de pruebas de Flask, por lo que no levantan un servidor web real. En lugar de entrar desde el navegador, las pruebas hacen peticiones internas a las rutas del sistema, por ejemplo `GET /login`, `POST /login`, `POST /profesor/cursos/crear` o `POST /alumno/cursos/<id>/inscribir`.

La configuración de testing se encuentra en `tests/conftest.py`. Ahí se crea una aplicación Flask en modo prueba y se usa una base de datos **SQLite en memoria**:

```python
"SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
```

Esto significa que los tests no usan tu base de datos MySQL real, no necesitan ejecutar `DB.sql` y no modifican datos locales de desarrollo. Cada prueba inicia con una base limpia y al terminar se eliminan las tablas creadas para esa ejecución.

El archivo `tests/factories.py` contiene funciones auxiliares para crear datos de prueba de forma legible, como usuarios, alumnos, profesores, idiomas, cursos, inscripciones y materiales. Esto evita repetir demasiado código dentro de cada archivo de test.

En general, cada prueba sigue este flujo:

1. Crea los datos mínimos necesarios para el caso de uso.
2. Inicia sesión con el rol correspondiente cuando la ruta lo requiere.
3. Ejecuta la petición HTTP usando `client.get(...)` o `client.post(...)`.
4. Verifica la respuesta y, cuando aplica, consulta la base de datos para confirmar que el cambio se guardó correctamente.

Ejemplo simplificado:

```python
def test_profesor_puede_crear_curso(client, idioma):
    profesor = crear_profesor()
    db.session.commit()

    iniciar_sesion(client, profesor, ROL_PROFESOR)

    respuesta = client.post(
        "/profesor/cursos/crear",
        data=datos_formulario_curso(idioma),
        follow_redirects=True,
    )

    curso = Curso.query.filter_by(codigo="ING-A1-100").first()

    assert respuesta.status_code == 200
    assert curso is not None
    assert curso.estado_curso == "borrador"
```

### Archivos relacionados con testing

```text
tests/
├── conftest.py
├── factories.py
├── test_iniciar_sesion.py
├── test_crear_cuenta.py
├── test_inscribir_curso.py
├── test_consultar_material.py
├── test_crear_curso.py
├── test_publicar_curso.py
├── test_cerrar_eliminar_curso.py
├── test_crear_profesor.py
├── test_consultar_profesor.py
├── test_actualizar_profesor.py
├── test_eliminar_profesor.py
└── test_eliminar_cuentas.py

pytest.ini
```

`pytest.ini` indica que pytest debe buscar pruebas dentro de `tests/` y ejecutar archivos con nombre `test_*.py`.

### Nota sobre warnings al ejecutar los tests

Al ejecutar los tests puede aparecer una advertencia relacionada con `datetime.utcnow()`:

```bash
DeprecationWarning: datetime.datetime.utcnow() is deprecated
```

Esto no significa que los tests estén fallando. Mientras el resultado final sea similar a:

```bash
24 passed
```

la suite de pruebas se ejecutó correctamente.

El warning aparece porque algunas partes del proyecto usan `datetime.utcnow()` para guardar fechas en UTC, y en versiones recientes de Python esta forma de manejar fechas está marcada como obsoleta. El sistema sigue funcionando, pero Python recomienda usar fechas con información explícita de zona horaria.

Por ahora, estos warnings son informativos y no bloquean la ejecución de los tests.

---

## Scripts útiles

### Poblar datos de prueba

```bash
python scripts/poblar_datos_prueba.py
```

### Listar datos de prueba

```bash
python scripts/listar_datos_prueba.py
```

Este script muestra:

- usuarios registrados;
- roles;
- estado activo/inactivo;
- credenciales conocidas de prueba;
- cursos cargados;
- profesor responsable;
- estado de cada curso;
- inscripciones activas.

### Consultar usuarios desde SQL

Archivo:

```text
scripts/sql/listar_usuarios.sql
```

Puedes ejecutarlo en MySQL Workbench, DBeaver o consola.

### Consultar cursos desde SQL

Archivo:

```text
scripts/sql/listar_cursos.sql
```

---

## Estructura del proyecto

```text
sgci/
│
├── app.py
├── DB.sql
├── README.md
├── requirements.txt
├── pytest.ini
├── .env
│
├── controllers/
│   ├── admin.py
│   ├── alumno.py
│   ├── login.py
│   └── profesor.py
│
├── models/
│   ├── Administrador.py
│   ├── Alumno.py
│   ├── Curso.py
│   ├── Idioma.py
│   ├── Inscripcion.py
│   ├── Material.py
│   ├── NivelAlumno.py
│   ├── Profesor.py
│   ├── Usuario.py
│   └── __init__.py
│
├── templates/
│   ├── base.html
│   ├── error.html
│   ├── login.html
|   ├── registro.html
│   │
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── usuarios.html
│   │   ├── formulario_usuario.html
│   │   ├── profesores.html
│   │   └── alumnos.html
│   │
│   ├── profesor/
│   │   ├── cursos.html
│   │   ├── dashboard.html
│   │   ├── detalle_curso.html
│   │   ├── formulario_curso.html
│   │   └── formulario_material.html
│   │
│   └── alumno/
│       └── cursos.html
|		└── dashboard.html
|		└── detalle_curso.html
│
├── tests/
│   ├── conftest.py
│   ├── factories.py
│   └── test_*.py
│
├── utils/
│   ├── auth.py
│   └── niveles.py
│
└── scripts/
    ├── crear_administrador.py
    ├── poblar_datos_prueba.py
    ├── listar_datos_prueba.py
    └── sql/
        ├── listar_usuarios.sql
        └── listar_cursos.sql
```

---

## Rutas principales

### Autenticación

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Redirige al login o al dashboard |
| GET | `/login` | Muestra formulario de login |
| POST | `/login` | Procesa inicio de sesión |
| GET | `/logout` | Cierra sesión |
| GET | `/dashboard` | Redirige al dashboard según rol |

### Administrador

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/admin/dashboard` | Panel principal del administrador |
| GET | `/admin/usuarios` | Lista usuarios |
| GET | `/admin/usuarios/crear` | Formulario para crear usuario |
| POST | `/admin/usuarios/crear` | Guarda usuario nuevo |
| GET | `/admin/usuarios/<id>/editar` | Formulario para editar usuario |
| POST | `/admin/usuarios/<id>/editar` | Guarda cambios del usuario |
| POST | `/admin/usuarios/<id>/activar` | Activa usuario |
| POST | `/admin/usuarios/<id>/desactivar` | Desactiva usuario |
| GET | `/admin/profesores` | Lista profesores |
| GET | `/admin/alumnos` | Lista alumnos |

### Profesor

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/profesor/dashboard` | Panel principal del profesor |
| GET | `/profesor/cursos` | Lista cursos del profesor |
| GET | `/profesor/cursos/crear` | Formulario para crear curso |
| POST | `/profesor/cursos/crear` | Guarda curso nuevo |
| GET | `/profesor/cursos/<id>` | Detalle de curso |
| GET | `/profesor/cursos/<id>/editar` | Formulario para editar curso |
| POST | `/profesor/cursos/<id>/editar` | Guarda cambios del curso |
| POST | `/profesor/cursos/<id>/publicar` | Publica curso |
| POST | `/profesor/cursos/<id>/cerrar` | Cierra curso |

### Alumno

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/alumno/dashboard` | Panel inicial del alumno |

---

## Modelo general de datos

El sistema usa las siguientes tablas principales:

| Tabla | Propósito |
|---|---|
| `usuario` | Datos generales de todos los usuarios |
| `administrador` | Datos específicos del administrador |
| `profesor` | Datos específicos del profesor |
| `alumno` | Datos específicos del alumno |
| `idioma` | Catálogo de idiomas |
| `curso` | Cursos creados por profesores |
| `material` | Materiales asociados a cursos |
| `inscripcion` | Relación entre alumnos y cursos |
| `nivel_alumno` | Nivel del alumno por idioma |

Relaciones principales:

```text
usuario 1 ─── 1 administrador
usuario 1 ─── 1 profesor
usuario 1 ─── 1 alumno
profesor 1 ─── N curso
idioma 1 ─── N curso
curso 1 ─── N material
alumno N ─── N curso mediante inscripcion
alumno N ─── N idioma mediante nivel_alumno
```

---

## Reglas de negocio implementadas

### Usuarios

- El correo debe ser único.
- La contraseña se almacena con hash.
- Los usuarios inactivos no pueden iniciar sesión.
- Cada usuario debe tener un rol válido.
- El administrador puede crear usuarios por rol.
- El administrador puede activar o desactivar usuarios.

### Roles

- El administrador solo puede acceder a rutas administrativas.
- El profesor solo puede acceder a rutas de profesor.
- El alumno solo puede acceder a rutas de alumno.
- Las rutas privadas requieren sesión activa.

### Cursos

- Solo profesores pueden crear cursos.
- Un profesor solo puede ver y modificar sus propios cursos.
- Todo curso nuevo inicia en estado `borrador`.
- Un curso puede pasar a estado `publicado`.
- Un curso puede pasar a estado `cerrado`.
- Los cursos cerrados no se pueden publicar nuevamente desde la pantalla de profesor.

Estados de curso:

| Estado | Significado |
|---|---|
| `borrador` | Curso en preparación |
| `publicado` | Curso visible para inscripción |
| `cerrado` | Curso finalizado o no disponible |

---

## Problemas comunes

### Error: Access denied for user

Causa probable: las credenciales de `.env` no coinciden con tu usuario de MySQL.

Revisa:

```env
USERNAME=root
PASSWORD=tu_password_de_mysql
HOST=localhost
PORT=3306
DATABASE=sgci_db
```

---

### Error: Unknown database 'sgci_db'

Causa probable: no has creado la base de datos.

Solución:

```sql
CREATE DATABASE sgci_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Luego ejecuta `DB.sql`.

---

### Error: Table 'sgci_db.usuario' doesn't exist

Causa probable: creaste la base de datos, pero no ejecutaste `DB.sql`.

Solución:

```bash
mysql -u root -p sgci_db < DB.sql
```

---

### Error: SECRET_KEY no está definida

Causa probable: no existe `.env` o no tiene `SECRET_KEY`.

Solución:

```env
SECRET_KEY=sgci_desarrollo_2026
```

---

### Error relacionado con `Idioma` o relaciones de SQLAlchemy

Ejemplo:

```text
expression 'Idioma' failed to locate a name ('Idioma')
```

Causa probable: los modelos no se importaron correctamente en `models/__init__.py`.

Ese archivo debe importar los modelos principales:

```python
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
```

---

### El login dice credenciales inválidas

Revisa que hayas poblado la base de datos:

```bash
python scripts/poblar_datos_prueba.py
```

Luego usa las credenciales conocidas:

```text
admin@sgci.com / Admin12345
profesor@sgci.com / Profesor12345
alumno@sgci.com / Alumno12345
```

---

### No veo los usuarios en la base de datos

Ejecuta:

```bash
python scripts/listar_datos_prueba.py
```

O usa:

```sql
SELECT id_usuario, correo, activo FROM usuario;
```

---

## Estado actual del proyecto

El proyecto se encuentra en el estado equivalente a:

```text
Sprint 1 — Autenticación y roles: completado
Sprint 2 — Panel administrador y gestión de usuarios: completado
Sprint 3 — Gestión de cursos por profesor: completado
Sprint 4 — Vista de alumno e inscripción a cursos: completado
Sprint 5 — Materiales didácticos: completado
```

Actualmente el sistema se encuentra completo.

---

## Notas de seguridad

- Las contraseñas se guardan usando hash, no texto plano.
- El archivo `.env` no debe subirse al repositorio.
- No compartas credenciales reales en GitHub.
- Las credenciales incluidas en este README son solo para datos locales de prueba.

---

## Comandos rápidos

Instalación completa desde cero:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS sgci_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p sgci_db < DB.sql
python scripts/poblar_datos_prueba.py
python app.py
```

En Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS sgci_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p sgci_db < DB.sql
python scripts/poblar_datos_prueba.py
python app.py
```
