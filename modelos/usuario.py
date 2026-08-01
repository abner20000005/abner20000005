"""
- Representa las entidades 'Usuarios' y 'Roles' de la base de datos.
- Contiene atributos como: id_usuario, nombre_usuario, contraseña, estado y id_rol.
- Se utiliza para la autenticación y control de permisos en la aplicación.
"""

INSERT INTO Roles (Nombre_Rol, Descripcion)
VALUES ('Administrador', 'Acceso total al sistema'),
       ('Bibliotecario', 'Gestión de libros y préstamos'),
       ('Encargado de reportes', 'Generación de informes');

INSERT INTO Usuarios (Nombre_Usuario, Contrasena, Estado, Id_Rol)
VALUES ('admin', '12345', 'Activo', 1),
       ('juan', 'abcde', 'Activo', 2),
       ('maria', 'qwerty', 'Inactivo', 3);