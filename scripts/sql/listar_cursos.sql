SELECT
    c.id_curso,
    c.codigo,
    c.nombre,
    i.nombre AS idioma,
    CONCAT(u.nombres, ' ', u.apellido_paterno, ' ', u.apellido_materno) AS profesor,
    c.nivel_requerido,
    c.modalidad,
    c.cupo_maximo,
    c.estado_curso,
    COUNT(CASE WHEN ins.estado_inscripcion = 'activa' THEN 1 END) AS inscripciones_activas
FROM curso c
INNER JOIN idioma i ON i.id_idioma = c.id_idioma
INNER JOIN profesor p ON p.id_usuario = c.id_profesor
INNER JOIN usuario u ON u.id_usuario = p.id_usuario
LEFT JOIN inscripcion ins ON ins.id_curso = c.id_curso
GROUP BY
    c.id_curso,
    c.codigo,
    c.nombre,
    i.nombre,
    u.nombres,
    u.apellido_paterno,
    u.apellido_materno,
    c.nivel_requerido,
    c.modalidad,
    c.cupo_maximo,
    c.estado_curso
ORDER BY c.id_curso;
