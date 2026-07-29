"""
- Establece la conexión entre Python y Microsoft SQL Server utilizando 'pyodbc'.
- Define las funciones para abrir, commit y cerrar conexiones de forma segura.
- Maneja excepciones de conexión a la base de datos.
"""
import pyodbc

def conectar():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=.\\SQLEXPRESS;"
        "DATABASE=Biblioteca360;"
        "UID=biblioteca;"
        "PWD=123456;"
    )