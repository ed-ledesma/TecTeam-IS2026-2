-- Tabla usuario
CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    fecha_nacimiento DATE NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    password_hash VARCHAR(255) NOT NULL,
    ultimo_cambio_password DATETIME,
    ultimo_acceso DATETIME
);

-- Tabla profesor
CREATE TABLE profesor (
    id_usuario INT PRIMARY KEY,
    numero_empleado VARCHAR(50) NOT NULL UNIQUE,
    especialidad VARCHAR(100),
    fecha_contratacion DATE NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

-- Tabla administrador
CREATE TABLE administrador (
    id_usuario INT PRIMARY KEY,
    nivel_acceso INT NOT NULL,
    area_responsable VARCHAR(100),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

-- Tabla alumno
CREATE TABLE alumno (
    id_usuario INT PRIMARY KEY,
    matricula VARCHAR(50) NOT NULL UNIQUE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

-- Tabla curso
CREATE TABLE curso (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    id_profesor INT NOT NULL,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    idioma VARCHAR(50),
    nivel VARCHAR(50),
    modalidad VARCHAR(50),
    cupo_maximo INT,
    estado_curso VARCHAR(50),
    FOREIGN KEY (id_profesor) REFERENCES profesor(id_usuario)
);

-- Tabla material
CREATE TABLE material (
    id_material INT AUTO_INCREMENT PRIMARY KEY,
    id_curso INT NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    tipo_material VARCHAR(50),
    url_archivo VARCHAR(255),
    visible BOOLEAN DEFAULT TRUE,
    fecha_publicacion DATETIME,
    FOREIGN KEY (id_curso) REFERENCES curso(id_curso)
);

-- Tabla inscripcion
CREATE TABLE inscripcion (
    id_alumno INT,
    id_curso INT,
    fecha_inscripcion DATETIME,
    estado_inscripcion VARCHAR(50),
    PRIMARY KEY (id_alumno, id_curso),
    FOREIGN KEY (id_alumno) REFERENCES alumno(id_usuario),
    FOREIGN KEY (id_curso) REFERENCES curso(id_curso)
);