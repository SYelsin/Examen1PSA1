import tkinter as tk
from tkinter import ttk
import socket
from PIL import Image, ImageTk
import datetime
from ttkbootstrap import Style
from tkinter import messagebox
def search():
    search_value = e10.get()
    b_data = f"reversion:{search_value}"
    client_socket.send(b_data.encode())
    result = client_socket.recv(1024).decode()
   
    try:
        result_dict = eval(result)
        if result_dict.get("message"):
            # Procesa el mensaje personalizado
            messagebox.showinfo("Mensaje", result_dict["message"])
        else:
            # Llenar la tabla con los resultados encontrados en la base de datos
            fill_table(result_dict)
            # Llenar los labels con el primer registro de la tabla (si hay resultados)
            selected_item = tree.selection()
            if selected_item:
                item_values = tree.item(selected_item)['values']
                e1.config(text=item_values[0])
                e2.config(text=item_values[1])
                e3.config(text=item_values[2])
                e4.config(text=item_values[3])
                e5.config(text=item_values[4])
    except Exception as e:
        print(f"Error al procesar los resultados: {e}")
def delete():
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)
        clear_fields()  # También limpia los campos después de la eliminación
def boton():
    delete()
    revertir_payment()
def fill_table(result_dict):
    # Borrar cualquier entrada previa en la tabla
    for row in tree.get_children():
        tree.delete(row)

    payments_info = result_dict.get("payments_info", [])  # Obtener la lista de pagos

    for index, payment in enumerate(payments_info, start=1):
        tree.insert("", "end", values=(
            result_dict.get("client_id", ""),
            result_dict.get("client_name", ""),
            payment.get("payment_amount", ""),
            payment.get("payment_date", ""),
            payment.get("cuota", ""),
            payment.get("referencia", "")
        ))

    
def on_tree_select(event):
    selected_item = tree.selection()
    if selected_item:
        item_values = tree.item(selected_item)['values']
        e1.config(text=item_values[0])
        e2.config(text=item_values[1])
        e3.config(text=item_values[2])
        e4.config(text=item_values[3])
        e5.config(text=item_values[4])
        global cliente_id,referencia
        cliente_id = e1.cget("text")
        referencia = item_values[5]

def revertir_payment():
    
  
    try:
        rever_data = f"revertir:{cliente_id}:{referencia}"
        client_socket.send(rever_data.encode())
        result = client_socket.recv(1024).decode()
        if result == "Payment updated successfully":
            clear_fields()
            messagebox.showinfo("Información", "Pago revertido exitosamente")
        else:
            messagebox.showerror("Error", result)
    except Exception as e:
        print(e)
    

def clear_fields():
    e1.config(text="")
    e2.config(text="")
    e3.config(text="")
    e4.config(text="")
    e5.config(text="")
    e10.delete(0, tk.END)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.0.107", 12345))

root = tk.Tk()
root.geometry("850x500")
root.title("Nuevo Pago")

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

center_window(root, 900, 520)
style = Style('darkly')
style.configure('TLabel', background='gray')
font = ("Arial", 20, "bold")
titulo_label = tk.Label(root, text="REVERSIÓN", font=font)
titulo_label.place(x=350, y=5)


tk.Label(root, text="Codigo o Nombre:").place(x=280, y=50)
e10 = tk.Entry(root)
e10.place(x=400, y=50)

search_icon = Image.open("images/search_icon.png")
search_icon = search_icon.resize((19, 19))
search_icon = ImageTk.PhotoImage(search_icon)

search_button = tk.Button(root, image=search_icon, command=search)
search_button.place(x=510, y=50)

info_frame = ttk.LabelFrame(root, text="Datos de Pago")
info_frame.place(x=150, y=100, width=520, height=150)

tk.Label(info_frame, text="Id Cliente:").grid(row=0, column=0, padx=10, pady=5)
tk.Label(info_frame, text="Nombre:").grid(row=0, column=2, padx=10, pady=5)
tk.Label(info_frame, text="Monto:").grid(row=1, column=0, padx=10, pady=5)
tk.Label(info_frame, text="Fecha de Pago:").grid(row=1, column=2, padx=10, pady=5)
tk.Label(info_frame, text="Cuota:").grid(row=2, column=0, padx=10, pady=5)

style = ttk.Style()
style.configure('Inverse.TLabel', foreground='lime', background='black', width=20)
font = ("Arial", 10, "bold")
style.configure('Inverse.TLabel.TLabel')
e1 = ttk.Label(info_frame, text="", style='Inverse.TLabel', font=font)
e1.grid(row=0, column=1, padx=10, pady=5)
e2 = ttk.Label(info_frame, text="", style='Inverse.TLabel', font=font)
e2.grid(row=0, column=3, padx=10, pady=5)
e3 = ttk.Label(info_frame, text="", style='Inverse.TLabel', font=font)
e3.grid(row=1, column=1, padx=10, pady=5)
e4 = ttk.Label(info_frame, text="", style='Inverse.TLabel', font=font)
e4.grid(row=1, column=3, padx=10, pady=5)
e5 = ttk.Label(info_frame, text="", style='Inverse.TLabel', font=font)
e5.grid(row=2, column=1, padx=10, pady=5)

style = ttk.Style()
style.configure("Danger.TButton", foreground="red")

button = ttk.Button(root, text="Cancelar Pago", style="Danger.TButton", command=clear_fields)
button.place(x=230, y=270)

button = ttk.Button(root, text="Revertir Pago", command=boton)
button.place(x=450, y=270)

# Crear la tabla
tree = ttk.Treeview(root, columns=("ID", "Nombre", "Monto", "Fecha de Pago", "Cuota", "Referencia"))

tree.heading("#1", text="ID")
tree.heading("#2", text="Nombre")
tree.heading("#3", text="Monto")
tree.heading("#4", text="Fecha de Pago")
tree.heading("#5", text="Cuota")
tree.heading("#6", text="Referencia")

tree.column("#0", width=80, anchor="center")
tree.column("#1", width=120, anchor="center")
tree.column("#2", width=170, anchor="center")
tree.column("#3", width=100, anchor="center")
tree.column("#4", width=100, anchor="center")
tree.column("#5", width=170, anchor="center")
tree.column("#6", width=170, anchor="center")
# Mostrar la tabla en la parte inferior central
tree.grid(row=4, column=0, columnspan=2, sticky="nsew")

# Configurar la selección en la tabla
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Hacer que la tabla esté centrada en la ventana
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

root.geometry("850x500")
root.title("Nuevo Pago")

center_window(root, 900, 520)

root.mainloop()
