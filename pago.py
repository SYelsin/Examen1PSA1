import tkinter as tk
from tkinter import ttk
import socket
from PIL import Image, ImageTk
import datetime
from ttkbootstrap import Style
from tkinter import messagebox
import random
import string

# Generar una referencia única basada en números aleatorios y letras
def generate_reference():
    letters = string.ascii_uppercase
    random_letters = ''.join(random.choice(letters) for _ in range(6))
    return f"{random_letters}"


def search():
    search_value = e10.get()
    busqueda_data = f"search:{search_value}"
    client_socket.send(busqueda_data.encode())
    result = client_socket.recv(1024).decode()
   
    try:
        result_dict = eval(result)
        if result_dict.get("message"):
            # Procesa el mensaje personalizado
            messagebox.showinfo("Mensaje", result_dict["message"])
        else:
            # Procesa los resultados encontrados en la base de datos
            e1.config(text=result_dict.get("client_id", ""))
            e2.config(text=result_dict.get("client_name", ""))
            
            oldest_payment = result_dict.get("oldest_pending_payment", {})
            e3.config(text=oldest_payment.get("payment_amount", ""))
            e4.config(text=oldest_payment.get("payment_date", ""))
            e5.config(text=oldest_payment.get("cuota", ""))
            e8.config(text=oldest_payment.get("recargo", "200"))
            e9.config(text=oldest_payment.get("total_to_pay", "0"))
    except Exception as e:
        print(f"Error al procesar los resultados: {e}")


def show_ticket(client_id, nombre, cuota, payment_date, payment_amount, reference):
    ticket_window = tk.Toplevel()
    ticket_window.title("Ticket de Pago")
    
    # Encabezado e información de la empresa
    header_label = tk.Label(ticket_window, text="UTH", font=("Helvetica", 16, "bold"), fg="black")
    header_label.pack()

    company_info_label = tk.Label(ticket_window, text="Dirección: Calle 123, Choluteca", font=("Helvetica", 10), fg="black")
    company_info_label.pack()

    company_info_label = tk.Label(ticket_window, text="Teléfono: +504 95946795", font=("Helvetica", 10), fg="black")
    company_info_label.pack()

    company_info_label = tk.Label(ticket_window, text="Correo: info@uth.hn", font=("Helvetica", 10), fg="black")
    company_info_label.pack()

    separator = tk.Label(ticket_window, text="________________________________________________________", font=("Helvetica", 12), fg="black")
    separator.pack()
    ticket_label = tk.Label(ticket_window, text=f"Número de Referencia: {reference}", font=("Helvetica", 12), fg="black")
    ticket_label.pack()
    # Contenido del ticket
    ticket_label = tk.Label(ticket_window, text=f"Cliente ID: {client_id}", font=("Helvetica", 12), fg="black")
    ticket_label.pack()
    
    ticket_label = tk.Label(ticket_window, text=f"Nombre Cliente: {nombre}", font=("Helvetica", 12), fg="black")
    ticket_label.pack()
    
    ticket_label = tk.Label(ticket_window, text=f"Cuota: {cuota}", font=("Helvetica", 12), fg="black")
    ticket_label.pack()
    
    ticket_label = tk.Label(ticket_window, text=f"Fecha de Pago: {payment_date}", font=("Helvetica", 12), fg="black")
    ticket_label.pack()
    
    ticket_label = tk.Label(ticket_window, text=f"Monto Pagado: LPS. {payment_amount}", font=("Helvetica", 12), fg="black")
    ticket_label.pack()
    
    separator = tk.Label(ticket_window, text="________________________________________________________", font=("Helvetica", 12), fg="black")
    separator.pack()
    
   # Botón para imprimir
    print_button = tk.Button(
    ticket_window,
    text="Imprimir Ticket",
    command=lambda: print_ticket(client_id, cuota, payment_date, payment_amount, reference),
    width=15,  # Establece un ancho fijo
    height=2,  # Establece una altura fija
    font=("Helvetica", 12, "bold"),  # Fuente personalizada
    bg="lightblue",  # Color de fondo
    fg="black",  # Color del texto
)
    print_button.pack(pady=10)  # Agrega un espacio en la parte inferior

# Botón para cerrar el ticket
    close_button = tk.Button(
    ticket_window,
    text="Cerrar Ticket",
    command=ticket_window.destroy,
    width=15,  # Establece un ancho fijo
    height=2,  # Establece una altura fija
    font=("Helvetica", 12, "bold"),  # Fuente personalizada
    bg="red",  # Color de fondo
    fg="white",  # Color del texto
)
    close_button.pack(pady=10)
    ticket_window.geometry("300x500") 
def print_ticket(client_id, cuota, payment_date, payment_amount, reference):
    # Aquí puedes agregar el código para imprimir el ticket (depende del sistema operativo y la configuración de la impresora)
    print("Imprimiendo ticket...")


def update_payment():
    client_id = e1.cget("text")
    cuota = e5.cget("text")
    payment_amount = e6.get()
    payment_date = e7.get()
    nombre = e2.cget("text")
    try:
        # Generar una referencia única para esta transacción
        reference = generate_reference()
        
        # Crear la trama de datos que incluye la referencia y el sufijo (00 o 01)
        is_successful = True  # Indica si el pago es exitoso (ajusta según tu lógica)
        result_suffix = "00" if is_successful else "01"
        complete_reference = f"{reference}-{result_suffix}"
        
        # Crear la trama de datos que incluye la referencia
        pago_data = f"update:{client_id}:{cuota}:{payment_date}:{payment_amount}:{complete_reference}"

        client_socket.send(pago_data.encode())
        result = client_socket.recv(1024).decode()
        if is_successful:
            clear_fields()
            messagebox.showinfo("Información", "Pago registrado exitosamente")
            show_ticket(client_id, nombre, cuota,  payment_date, payment_amount, complete_reference)
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
    e6.delete(0, tk.END)
    e7.set(default_date)
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

tk.Label(root, text="Codigo o Nombre:").place(x=280, y=30)
e10 = tk.Entry(root)
e10.place(x=400, y=30)

search_icon = Image.open("images/search_icon.png")
search_icon = search_icon.resize((19, 19))
search_icon = ImageTk.PhotoImage(search_icon)

search_button = tk.Button(root, image=search_icon, command=search)
search_button.place(x=510, y=30)

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

tk.Label(root, text="Monto Pagado: LPS.").place(x=50, y=270)
e6 = tk.Entry(root)
e6.place(x=180, y=270)

tk.Label(root, text="Fecha:").place(x=550, y=270)
default_date = datetime.date.today().strftime("%d-%m-%Y")
e7 = ttk.Combobox(root, values=[default_date])
e7.set(default_date)
e7.place(x=600, y=270)

style = ttk.Style()
style.configure("Danger.TButton", foreground="red")

button = ttk.Button(root, text="Cancelar Pago", style="Danger.TButton", command=clear_fields)
button.place(x=230, y=370)

button = ttk.Button(root, text="Guardar Pago", command=update_payment)
button.place(x=450, y=370)

# Add new labels and entry widgets for surcharge and total payment
e8_label = tk.Label(info_frame, text="Recargo (LPS. 200):")
e8 = tk.Label(info_frame, text="200", font=font)
e9_label = tk.Label(info_frame, text="Total a Pagar:")
e9 = tk.Label(info_frame, text="0", font=font)

root.mainloop()
