import pyodbc

def obtener_conexion():
    try:
        conexion = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=Biblioteca360;"
            "UID=biblioteca;"
            "PWD=123456;"
        )
        return conexion
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None