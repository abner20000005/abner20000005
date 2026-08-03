from config.conexion import obtener_conexion
from modelos.usuario_admin import UsuarioAdmin

def listar_usuarios():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT u.Id_Usuario, u.Nombre_Usuario, u.Contrasena, u.Estado,
                   u.Id_Rol, r.Nombre_Rol
            FROM Usuarios u
            INNER JOIN Roles r ON u.Id_Rol = r.Id_Rol
            ORDER BY u.Nombre_Usuario
        """)
        return [UsuarioAdmin(*f) for f in cursor.fetchall()]
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conexion.close()

def obtener_roles():
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT Id_Rol, Nombre_Rol FROM Roles ORDER BY Nombre_Rol")
        return cursor.fetchall()
    except:
        return []
    finally:
        conexion.close()

def guardar_usuario(nombre, contrasena, estado, id_rol):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT Id_Usuario FROM Usuarios WHERE Nombre_Usuario = ?", (nombre,))
        if cursor.fetchone():
            return "duplicado"
        cursor.execute("""
            INSERT INTO Usuarios (Nombre_Usuario, Contrasena, Estado, Id_Rol)
            VALUES (?, ?, ?, ?)
        """, (nombre, contrasena, estado, id_rol))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()

def modificar_usuario(id_usuario, nombre, contrasena, estado, id_rol):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE Usuarios
            SET Nombre_Usuario=?, Contrasena=?, Estado=?, Id_Rol=?
            WHERE Id_Usuario=?
        """, (nombre, contrasena, estado, id_rol, id_usuario))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()

def eliminar_usuario(id_usuario):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Usuarios WHERE Id_Usuario = ?", (id_usuario,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conexion.close()