import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import socket
from tkinter import messagebox
def fill_table(data):
    new_window = tk.Toplevel(root)
    new_window.title("Historial de Cuotas")

    tree = ttk.Treeview(new_window, columns=("ID", "Monto", "Fecha", "Cuota", "Estado"))
    tree.heading("#1", text="Id Cliente")
    tree.heading("#2", text="Monto")
    tree.heading("#3", text="Fecha Realizacion")
    tree.heading("#4", text="Cuota")
    tree.heading("#5", text="Estado")
    tree.pack()

    for item in data:
        tree.insert('', 'end', values=item)

    for col in tree["columns"]:
        tree.column(col, anchor="center")

def clear_message():
    message_label.config(text="")

def show_message(message, color="red"):
    message_label.config(text=message, foreground=color)

def historial():
    id_cliente = client_id_entry.get()
    b_data = f"historial:{id_cliente}"
    client_socket.send(b_data.encode())
    result = client_socket.recv(1024).decode()
   
    if not result:  # Si el resultado está vacío
        messagebox.showinfo("Info", "No se recibieron datos del servidor.")
    else:
        try:
            result_list = eval(result)
            if isinstance(result_list, list):
                data = []
                for item in result_list:
                    data.append(
                        (item[0],  item[2], item[3], item[4], item[5])
                    )
                fill_table(data)
                clear_message()  # Limpiar el mensaje si se encontraron datos
            else:
                messagebox.showinfo("Error", "No se encontraron datos para el cliente.")
        except Exception as e:
             messagebox.showinfo("Error al procesar los resultados: {e}", "red")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.0.107", 12345))

root = tk.Tk()
root.title("Visualizar Historial de Cuotas")

style = Style(theme="darkly")
style.configure("TLabel", padding=5, font=("Helvetica", 14))
style.configure("TEntry", padding=5, font=("Helvetica", 14))
style.configure("TButton", padding=5, font=("Helvetica", 12))

client_id_label = ttk.Label(root, text="Código del Cliente:")
client_id_label.pack()

client_id_entry = ttk.Entry(root)
client_id_entry.pack()

show_history_button = ttk.Button(root, text="Mostrar Historial", command=historial)
show_history_button.pack(pady=10)

message_label = ttk.Label(root, text="", foreground="red")
message_label.pack()

root.geometry("400x250+{}+{}".format(root.winfo_screenwidth() // 2 - 200, root.winfo_screenheight() // 2 - 125))

root.mainloop()
