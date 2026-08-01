from config.conexion import obtener_conexion 
from servicios.calculo_multas import calcular_multa_retraso, calcular_sancion_danio_perdida
from datetime import date # Necesario para la tabla PagosMultas

class SancionesControlador:
    
    def generar_sancion(self, id_lector, motivo, dias_retraso=0, precio_libro=0, nivel_danio=''):
        monto = 0
        if motivo == 'Retraso':
            monto = calcular_multa_retraso(dias_retraso)
        elif motivo in ['Daño', 'Pérdida']:
            monto = calcular_sancion_danio_perdida(precio_libro, nivel_danio)

        if monto > 0:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            try:
                # 1. Insertar respetando la tabla Sanciones
                sql_sancion = "INSERT INTO Sanciones (Id_Lector, Motivo, Monto, Estado) VALUES (%s, %s, %s, 'Pendiente')"
                cursor.execute(sql_sancion, (id_lector, motivo, monto))
                
                # 2. Bloquear al lector
                self.bloquear_lector(id_lector, cursor)
                
                conexion.commit()
                print(f"Sanción generada exitosamente. Lector {id_lector} bloqueado.")
            except Exception as e:
                print(f"Error al generar sanción: {e}")
                conexion.rollback()
            finally:
                cursor.close()
                conexion.close()

    def bloquear_lector(self, id_lector, cursor):
        # Actualiza el campo Estado de la tabla Lectores
        sql_bloqueo = "UPDATE Lectores SET Estado = 'Bloqueado' WHERE Id_Lector = %s"
        cursor.execute(sql_bloqueo, (id_lector,))

    def registrar_pago(self, id_sancion, id_lector):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        try:
            # 1. Obtener el monto de la sanción para guardarlo en el recibo de pago
            sql_monto = "SELECT Monto FROM Sanciones WHERE Id_Sancion = %s"
            cursor.execute(sql_monto, (id_sancion,))
            resultado = cursor.fetchone()
            
            if not resultado:
                print("Error: No existe esa sanción.")
                return False
                
            monto_sancion = resultado[0]
            fecha_hoy = date.today().strftime('%Y-%m-%d')

            # 2. Insertar en la tabla PagosMultas (NUEVO PASO POR TU SCRIPT SQL)
            sql_pago = "INSERT INTO PagosMultas (Fecha_Pago, Monto, Id_Sancion) VALUES (%s, %s, %s)"
            cursor.execute(sql_pago, (fecha_hoy, monto_sancion, id_sancion))
            
            # 3. Marcar la sanción como 'Pagado' en la tabla Sanciones
            sql_actualizar_sancion = "UPDATE Sanciones SET Estado = 'Pagado' WHERE Id_Sancion = %s"
            cursor.execute(sql_actualizar_sancion, (id_sancion,))
            
            # 4. Verificar si el lector tiene OTRAS sanciones pendientes
            sql_pendientes = "SELECT COUNT(*) FROM Sanciones WHERE Id_Lector = %s AND Estado = 'Pendiente'"
            cursor.execute(sql_pendientes, (id_lector,))
            sanciones_pendientes = cursor.fetchone()[0]
            
            # 5. Si ya no debe nada, desbloquear al lector
            if sanciones_pendientes == 0:
                sql_desbloqueo = "UPDATE Lectores SET Estado = 'Activo' WHERE Id_Lector = %s"
                cursor.execute(sql_desbloqueo, (id_lector,))
                print(f"Pago registrado en PagosMultas. El lector {id_lector} ha sido DESBLOQUEADO.")
            else:
                print(f"Pago registrado. Lector {id_lector} sigue bloqueado por multas pendientes.")
                
            conexion.commit()
            return True
            
        except Exception as e:
            print(f"Error al registrar el pago: {e}")
            conexion.rollback()
            return False
        finally:
            cursor.close()
            conexion.close()