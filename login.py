import tkinter
import tkinter as tk
from tkinter import ttk
import customtkinter
import socket
from tkinter import messagebox
import subprocess
from PIL import ImageTk,Image
from ttkbootstrap import Style
from datetime import datetime
# Funciones para ejecutar los módulos
def ejecutar_modulo1():
    subprocess.run(["python", "pago.py"])

def ejecutar_modulo2():
    subprocess.run(["python", "reversion.py"])

def ejecutar_modulo3():
    subprocess.run(["python", "historial.py"])
    


    
def login():
    try:
        username = entry1.get()
        password = entry2.get()
        global usuario 
        usuario = username
        login_data = f"login:{username}:{password}"
        # client_socket.send("login".encode())
        client_socket.send(login_data.encode())
        result = client_socket.recv(1024).decode()
        if result == "Login successful":
            client_socket.close()
            button_function()
        else:
            messagebox.showerror("Error", "Datos incorrectos")
            print("Error de inicio de sesión")

    except Exception as e:
        messagebox.showerror("Error", str(e))
    # finally:
    #     client_socket.close()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.0.107", 12345))

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green


app = customtkinter.CTk()  #creating cutstom tkinter window
app.title('Login')

# Dimensiones de la ventana
window_width = 600
window_height = 440

# Obtiene el ancho y alto de la pantalla
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Calcula la posición para centrar la ventana
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Establece la geometría de la ventana
app.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Centra la ventana en la pantalla
app.update_idletasks()




def button_function():
    app.destroy()            # destroy current window and creating new one 
    # Obtén el ancho y alto de la ventana
    w = tk.Tk()
    w.title('SISTEMA GESTION DE PAGOS')

    # Obtén el ancho y alto de la ventana
    window_width = 1280
    window_height = 720

    # Obtiene el ancho y alto de la pantalla
    screen_width = w.winfo_screenwidth()
    screen_height = w.winfo_screenheight()

    # Calcula la posición para centrar la ventana
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Establece la geometría de la ventana
    w.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Centra la ventana en la pantalla
    w.update_idletasks()
    # Cargar la imagen
    image = Image.open("./images/logo.png")
    photo = ImageTk.PhotoImage(image)
    def ejecutar_modulo4():
        w.destroy()
    def actualizar_hora():
        ahora = datetime.now()
        fecha.config(text=" " + ahora.strftime("%Y-%m-%d %H:%M:%S"))
        w.after(1000, actualizar_hora)

    fecha = tk.Label(w, text="Fecha y Hora ", font=("Helvetica", 12))
    fecha.pack(pady=10, padx=20, anchor="ne")
    user = tk.Label(w, text="Bienvenido " + usuario, font=("Helvetica", 12))
    user.pack(pady=0, padx=20, anchor="nw")

    frame = tk.Frame(w)
    frame.pack(expand=False, fill="both")

    # Mostrar el logo en el centro de la ventana
    logo_label = tk.Label(frame, image=photo)
    logo_label.photo = photo
    logo_label.pack()
    l = tk.Label(frame, text="FINANCES", font=("Helvetica", 12))
    l.pack(pady=10)
    actualizar_hora()
    # Crea un estilo con ttk y selecciona el tema "vapor"
    style = Style('darkly')

    # Función para cargar y redimensionar el icono
    def cargar_icono(ruta, size):
        icono = Image.open(ruta)
        icono = icono.resize(size)
        return ImageTk.PhotoImage(icono)

    # Cargar iconos
    icono_modulo1 = cargar_icono("images/pago.png", (64, 64))
    icono_modulo2 = cargar_icono("images/revertir.png", (64, 64))
    icono_modulo3 = cargar_icono("images/historial.png", (64, 64))
    icono_modulo4 = cargar_icono("images/salir.png", (64, 64))
    # Crear marcos para organizar los botones
    marco1 = tk.Frame(w)
    marco2 = tk.Frame(w)

    # Botones para ejecutar los módulos con iconos en una disposición de 2x2
    btn_modulo1 = tk.Button(
        marco1,
        text="Nuevo Pago",
        image=icono_modulo1,
        compound="top", 
        command=ejecutar_modulo1,
        height=100,  # Aumenta la altura del botón
        width=100  # Aumenta el ancho del botón
    )
    btn_modulo2 = tk.Button(
        marco1,
        text="Reversión",
        image=icono_modulo2,
        compound="top",
        command=ejecutar_modulo2,
        height=100,
        width=100
    )
    btn_modulo3 = tk.Button(
        marco2,
        text="Historial",
        image=icono_modulo3,
        compound="top",
        command=ejecutar_modulo3,
        height=100,
        width=100
    )
    btn_modulo4 = tk.Button(
        marco2,
        text="Salir",
        image=icono_modulo4,
        compound="top",
        command=ejecutar_modulo4,
        height=100,
        width=100
    )
    btn_modulo1.config(cursor="hand2")
    btn_modulo2.config(cursor="hand2")
    btn_modulo3.config(cursor="hand2")
    btn_modulo4.config(cursor="hand2")
    # Organiza los botones en la disposición deseada con espacio entre ellos
    btn_modulo1.grid(row=0, column=0, padx=20, pady=20)
    btn_modulo2.grid(row=0, column=1, padx=20, pady=20)
    btn_modulo3.grid(row=1, column=0, padx=20, pady=20)
    btn_modulo4.grid(row=1, column=1, padx=20, pady=20)
    # Crea un título arriba de los botones
    titulo = tk.Label(w, text="GESTIÓN DE PAGOS", font=("Helvetica", 20))
    titulo.pack(pady=20)

    # Organiza los marcos
    marco1.pack()
    marco2.pack()
    w.mainloop()
    


img1=ImageTk.PhotoImage(Image.open("./images/pattern.png"))
l1=customtkinter.CTkLabel(master=app,image=img1)
l1.pack()

#creating custom frame
frame=customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

l2=customtkinter.CTkLabel(master=frame, text="Iniciar Sesión",font=('Century Gothic',20))
l2.place(x=50, y=45)

entry1=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Usuario')
entry1.place(x=50, y=110)

entry2=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Contraseña', show="*")
entry2.place(x=50, y=165)



#Create custom button
button1 = customtkinter.CTkButton(master=frame, width=220, text="Login", command=login, corner_radius=6)
button1.place(x=50, y=240)


app.mainloop()
