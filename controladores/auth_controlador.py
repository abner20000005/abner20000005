from config.conexion import obtener_conexion
from modelos.usuario import Usuario

def iniciar_sesion(usuario, contrasena):
    conexion = obtener_conexion()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT u.Id_Usuario, u.Nombre_Usuario, u.Id_Rol, r.Nombre_Rol, u.Estado
            FROM Usuarios u
            INNER JOIN Roles r ON u.Id_Rol = r.Id_Rol
            WHERE u.Nombre_Usuario = ? AND u.Contrasena = ? AND u.Estado = 'Activo'
        """, (usuario, contrasena))

        fila = cursor.fetchone()
        if fila:
            return Usuario(fila[0], fila[1], fila[2], fila[3], fila[4])
        return None
    except Exception as e:
        print(f"Error en login: {e}")
        return None
    finally:
        conexion.close()