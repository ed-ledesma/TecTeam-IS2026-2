SELECT
    u.id_usuario AS id,
    CASE
        WHEN a.id_usuario IS NOT NULL THEN 'administrador'
        WHEN p.id_usuario IS NOT NULL THEN 'profesor'
        WHEN al.id_usuario IS NOT NULL THEN 'alumno'
        ELSE 'sin rol'
    END AS rol,
    CASE
        WHEN u.activo = 1 THEN 'activo'
        ELSE 'inactivo'
    END AS estado,
    u.correo,
    CASE
        WHEN u.correo = 'admin@sgci.com' THEN 'Admin12345'
        WHEN u.correo = 'profesor@sgci.com' THEN 'Profesor12345'
        WHEN u.correo = 'alumno@sgci.com' THEN 'Alumno12345'
        ELSE 'desconocida'
    END AS password_prueba,
    CONCAT(u.nombres, ' ', u.apellido_paterno, ' ', u.apellido_materno) AS nombre_completo,
    u.ultimo_acceso
FROM usuario u
LEFT JOIN administrador a ON a.id_usuario = u.id_usuario
LEFT JOIN profesor p ON p.id_usuario = u.id_usuario
LEFT JOIN alumno al ON al.id_usuario = u.id_usuario
ORDER BY u.id_usuario;
