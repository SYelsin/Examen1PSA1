import socket
import mysql.connector
import datetime


def is_payment_date_passed(payment_date):
    payment_date = datetime.datetime.strptime(payment_date, "%d-%m-%Y").date()
    today = datetime.date.today()
    return payment_date < today

def get_client_name(client_id):
    try:
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="pagos")
        mycursor = mysqldb.cursor()

        mycursor.execute("SELECT nombre FROM clientes WHERE id = %s", (client_id,))
        client_name = mycursor.fetchone()

        return client_name[0] if client_name else None
    except Exception as e:
        print(e)
    finally:
        mysqldb.close()

def update_payment(client_id, payment_amount, payment_date):
    try:
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="pagos")
        mycursor = mysqldb.cursor()

        mycursor.execute("SELECT cuota, monto FROM pagos WHERE id_cliente = %s AND estado = %s ORDER BY cuota ASC LIMIT 1", (client_id, 'P'))
        next_pending_payment = mycursor.fetchone()

        if next_pending_payment:
            cuota, pending_amount = next_pending_payment

            if float(payment_amount) >= pending_amount:
                mycursor.execute("UPDATE pagos SET estado = 'C', fecha_realizacion = %s WHERE id_cliente = %s AND cuota = %s", (payment_date, client_id, cuota))
                mysqldb.commit()
                return "Payment updated successfully"
            else:
                return "Payment amount is less than pending amount"
        else:
            return "No pending payments found"
    except Exception as e:
        print(e)
        mysqldb.rollback()
        return "Error updating payment"
    finally:
        mysqldb.close()


def search_in_database(search_value):
    # Connect to the database and perform the search
   try:
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="pagos")
        mycursor = mysqldb.cursor()

        try:
            search_value = int(search_value)
            mycursor.execute("SELECT clientes.id_cliente, clientes.nombre FROM clientes WHERE clientes.id_cliente = %s", (search_value,))
        except ValueError:
            mycursor.execute("SELECT clientes.id_cliente, clientes.nombre FROM clientes WHERE clientes.nombre = %s", (search_value,))

        client_info = mycursor.fetchone()

        if client_info:
            client_id, client_name = client_info
            mycursor.execute("SELECT pagos.monto, pagos.fecha_pago, pagos.cuota FROM pagos WHERE pagos.id_cliente = %s AND pagos.estado = 'P'", (client_id,))
            pending_payments = mycursor.fetchall()
            if pending_payments:
                payments_info = []
                for payment in pending_payments:
                    payment_amount, payment_date, cuota = payment
                    total_to_pay = payment_amount + 200 if is_payment_date_passed(payment_date) else 0
                    payments_info.append({
                        "payment_amount": payment_amount,
                        "payment_date": payment_date,
                        "cuota": cuota,
                        "recargo": 200,
                        "total_to_pay": total_to_pay,
                    })

                return {
                    "client_id": client_id,
                    "client_name": client_name,
                    "pending_payments": payments_info,
                    "payment_amount": payment_amount,
                    "payment_date": payment_date,
                    "cuota": cuota,
                    "recargo": 200,
                    "total_to_pay": total_to_pay,
                }
            else:
                return {
                "message": f"El cliente {client_name} no tiene cuotas pendientes",
            }
        else:
            return {
                "message": "El cliente no encontrado",
            }
   except Exception as e:
        print("Error: ", e)
        return "Error en la base de datos"
   finally:
        mysqldb.close()

def validate_login(username, password):
    try:
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="pagos")
        mycursor = mysqldb.cursor()

        mycursor.execute("SELECT username, password FROM usuarios WHERE username = %s", (username,))
        user_info = mycursor.fetchone()

        if user_info and user_info[1] == password:
            return True
        else:
            return False

    except Exception as e:
        print(e)
        return False
    finally:
        mysqldb.close()
        
# Definir la función historial con parámetros
def historial(id_cliente):
   try:
        # Conectar a la base de datos
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="pagos")
        mycursor = mysqldb.cursor()

        # Verificar si el cliente existe
        mycursor.execute("SELECT id_cliente FROM clientes WHERE id_cliente = %s", (id_cliente,))
        cliente = mycursor.fetchone()  # Obtener el resultado de la consulta

        if cliente is not None:
            # El cliente existe, obtener su historial de pagos
            mycursor.execute("SELECT id_cliente, cuota, monto, fecha_realizacion, ncuota, estado FROM pagos WHERE id_cliente = %s", (id_cliente,))
            historial = mycursor.fetchall()  # Obtener el historial de pagos
            return historial
        else:
            # El cliente no existe, devolver un mensaje de aviso
            return "El cliente  no existe"

   except Exception as e:
        print(e)
        return False
   finally:
        mysqldb.close()
        

def search_reversion(search_value):
    try:
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="pagos")
        mycursor = mysqldb.cursor()

        try:
            search_value = int(search_value)
            mycursor.execute("SELECT clientes.id_cliente, clientes.nombre FROM clientes WHERE clientes.id_cliente = %s", (search_value,))
        except ValueError:
            mycursor.execute("SELECT clientes.id_cliente, clientes.nombre FROM clientes WHERE clientes.nombre = %s", (search_value,))

        client_info = mycursor.fetchone()

        if client_info:
            client_id, client_name = client_info

            today = datetime.date.today()
            formatted_date = today.strftime("%d-%m-%Y")
            mycursor.execute("SELECT pagos.monto, pagos.fecha_pago, pagos.cuota FROM pagos WHERE pagos.id_cliente = %s AND pagos.estado = 'C' AND pagos.fecha_realizacion = %s", (client_id, formatted_date))

            pending_payments = mycursor.fetchall()

            if pending_payments:
                payments_info = []
                for payment in pending_payments:
                    payment_amount, payment_date, cuota = payment
                    total_to_pay = payment_amount + 200
                    payments_info.append({
                        "payment_amount": payment_amount,
                        "payment_date": payment_date,
                        "cuota": cuota,
                        "recargo": 200,
                        "total_to_pay": total_to_pay,
                    })

                return {
                    "client_id": client_id,
                    "client_name": client_name,
                    "payments_info": payments_info,  
                    "payment_amount": payment_amount,
                    "payment_date": payment_date,
                    "cuota": cuota,
                    "recargo": 200,
                    "total_to_pay": total_to_pay,
                }
            else:
                return {
                    "message": f"El cliente {client_name} no tiene cuotas que pueda revertir",
                }
        else:
            return {
                "message": "El cliente no encontrado",
            }
    except Exception as e:
        print("Error: ", e)
        return "Error en la base de datos"
    finally:
        mysqldb.close()

        
        
        
def revertir_payment(client_id, cuota):
    try:
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="pagos")
        mycursor = mysqldb.cursor()

        mycursor.execute("SELECT estado FROM pagos WHERE id_cliente = %s AND cuota = %s", (client_id, cuota))
        pago = mycursor.fetchall()
        
        
        mycursor.execute("UPDATE pagos SET estado = 'P' WHERE id_cliente = %s AND cuota = %s", (client_id, cuota))
        mysqldb.commit()
        return "Payment updated successfully"
            
       
    except Exception as e:
        print(e)
        mysqldb.rollback()
        return "Error updating payment"
    finally:
        mysqldb.close()

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024).decode()
            print(data)
            if not data:
                break
            if data == "search":
                search_value = client_socket.recv(1024).decode()
                # Perform the search using the provided value
                client_info = search_in_database(search_value)
                client_socket.send(str(client_info).encode())
            elif data == "update":
                client_id = client_socket.recv(1024).decode()
                payment_amount = client_socket.recv(1024).decode()
                payment_date =   client_socket.recv(1024).decode()
                # Handle payment update
                update_result = update_payment(client_id, payment_amount, payment_date)
                client_socket.send(update_result.encode())
            elif data == "login":
                login_data = client_socket.recv(1024).decode()
                user, passw = login_data.split(":")
                if validate_login(user, passw):
                    client_socket.send("Login successful".encode())
                else:
                    client_socket.send("Login failed".encode())
            elif data == "historial":
                id_cliente = client_socket.recv(1024).decode()
                historial_info = historial(id_cliente)
                # Convertir la información en una cadena JSON para enviarla
                import json
                client_socket.send(json.dumps(historial_info).encode())
                
            elif data == "reversion":
                 search_value = client_socket.recv(1024).decode()
                 client_info = search_reversion(search_value)
                 client_socket.send(str(client_info).encode())
                 print(client_info)
            elif data == "revertir":
                rever_data = client_socket.recv(1024).decode()
                cliente_id, cuota = rever_data.split(":")
                revertir_result = revertir_payment(cliente_id, cuota)
                client_socket.send(revertir_result.encode())
                
            
                

    except Exception as e:
        print(e)
    finally:
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 12345))
    server.listen(5)
    print("Server is listening for connections...")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    main()
