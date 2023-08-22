import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random
import string
import sqlite3
from ttkthemes import ThemedStyle

#pip install pillow
#pip install ttkthemes



# Función para centrar una ventana en pantalla
def centrar_ventana(ventana):
    ventana.update_idletasks()
    ancho_ventana = ventana.winfo_width()
    alto_ventana = ventana.winfo_height()
    x_pantalla = int((ventana.winfo_screenwidth() / 2) - (ancho_ventana / 2))
    y_pantalla = int((ventana.winfo_screenheight() / 2) - (alto_ventana / 2))
    ventana.geometry("+{}+{}".format(x_pantalla, y_pantalla))


# Función para generar una contraseña con los criterios dados
def generar_contrasena(longitud=12, incluir_letras=True, incluir_mayusculas=True, incluir_numeros=True, incluir_simbolos=True):
    # Crear un conjunto de caracteres basado en las opciones seleccionadas
    caracteres = ""
    if incluir_letras:
        caracteres += string.ascii_letters
    if incluir_mayusculas:
        caracteres += string.ascii_uppercase
    if incluir_numeros:
        caracteres += string.digits
    if incluir_simbolos:
        caracteres += string.punctuation

    # Si no hay caracteres válidos, mostrar un mensaje de error
    if not caracteres:
        raise ValueError("Debes incluir al menos un tipo de caracter (letras, números o símbolos)")

    # Generar la contraseña aleatoriamente
    contrasena = ''.join(random.choices(caracteres, k=longitud))
    return contrasena

# Función para generar una contraseña segura basada en las preferencias del usuario
def generar_contrasena_segura():
    # Obtener las preferencias del usuario
    longitud = int(longitud_entry.get())
    incluir_letras = letras_var.get()
    incluir_mayusculas = mayusculas_var.get()
    incluir_numeros = numeros_var.get()
    incluir_simbolos = simbolos_var.get()

    # Crear un conjunto de caracteres basado en las opciones seleccionadas
    caracteres = ""
    if incluir_letras:
        caracteres += string.ascii_lowercase
    if incluir_mayusculas:
        caracteres += string.ascii_uppercase
    if incluir_numeros:
        caracteres += string.digits
    if incluir_simbolos:
        caracteres += string.punctuation

    # Mostrar un mensaje de error si no hay caracteres válidos seleccionados
    if caracteres == "":
        messagebox.showerror("Error", "Debe seleccionar al menos un tipo de caracteres para generar la contraseña.")
        return

    # Generar la contraseña segura
    contrasena_generada = ''.join(random.choices(caracteres, k=longitud))
    contrasena_text.delete(1.0, tk.END)
    contrasena_text.insert(tk.END, contrasena_generada)

# Función para guardar una contraseña en la base de datos
def guardar_contrasena():
    # Obtener la contraseña generada
    contrasena = contrasena_text.get("1.0", tk.END).strip()
    if not contrasena:
        messagebox.showerror("Error", "No hay contraseña generada para guardar.")
        return

    # Crear una ventana emergente para guardar la contraseña
    def abrir_formulario_guardar():
        # Crear y configurar la ventana
        ventana_guardar = tk.Toplevel(ventana)
        ventana_guardar.title("Guardar Contraseña")
        ventana_guardar.geometry("300x300")
        ventana_guardar.attributes("-toolwindow", True)
        centrar_ventana(ventana_guardar)

        # Variables para almacenar los datos del formulario
        sitio_var = tk.StringVar()
        usuario_var = tk.StringVar()
        clave_var = tk.StringVar(value=contrasena)  # Configurar la contraseña generada

        # Etiquetas y campos de entrada para el formulario
        sitio_label = ttk.Label(ventana_guardar, text="Sitio:")
        sitio_label.pack(pady=5)
        sitio_entry = ttk.Entry(ventana_guardar, textvariable=sitio_var)
        sitio_entry.pack(pady=5)

        usuario_label = ttk.Label(ventana_guardar, text="Usuario:")
        usuario_label.pack(pady=5)
        usuario_entry = ttk.Entry(ventana_guardar, textvariable=usuario_var)
        usuario_entry.pack(pady=5)

        clave_label = ttk.Label(ventana_guardar, text="Clave:")
        clave_label.pack(pady=5)
        clave_entry = ttk.Entry(ventana_guardar, textvariable=clave_var, show="*")
        clave_entry.pack(pady=5)

        # Función para guardar los datos del formulario en la base de datos
        def guardar_datos():
            sitio = sitio_var.get()
            usuario = usuario_var.get()
            clave = clave_var.get()

            if not sitio or not usuario or not clave:
                messagebox.showerror("Error", "Por favor, ingrese el sitio, usuario y clave.")
                return

            # Guardar los datos en la base de datos SQLite
            conexion = sqlite3.connect("contrasenas.db")
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO contrasenas (sitio, usuario, clave) VALUES (?, ?, ?)", (sitio, usuario, clave))
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", "Contraseña guardada exitosamente.")
            ventana_guardar.destroy()

        # Botón para guardar los datos del formulario
        guardar_boton = ttk.Button(ventana_guardar, text="Guardar", command=guardar_datos)
        guardar_boton.pack(pady=10)

    # Abrir la ventana de guardar contraseña
    abrir_formulario_guardar()

# Función para crear la tabla "contrasenas" en la base de datos si no existe
def crear_tabla():
    conexion = sqlite3.connect("contrasenas.db")
    cursor = conexion.cursor()

    # Crear la tabla "contrasenas" si aún no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS contrasenas (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      sitio TEXT NOT NULL,
                      usuario TEXT NOT NULL,
                      clave TEXT NOT NULL)''')

    conexion.commit()
    conexion.close()

# Función para copiar la contraseña seleccionada al portapapeles
def copiar_contrasena():
    item = tabla.focus()
    if not item:
        messagebox.showwarning("Advertencia", "Por favor, seleccione una contraseña para copiar.")
        return

    # Obtener la contraseña seleccionada y copiarla al portapapeles
    clave_seleccionada = tabla.item(item, "values")[3]
    ventana.clipboard_clear()
    ventana.clipboard_append(clave_seleccionada)
    messagebox.showinfo("Éxito", "La contraseña se ha copiado al portapapeles.")

# Función para eliminar la contraseña seleccionada de la base de datos y de la tabla
def eliminar_contrasena():
    item = tabla.focus()
    if not item:
        messagebox.showwarning("Advertencia", "Por favor, seleccione una contraseña para eliminar.")
        return

    # Obtener el ID de la contraseña seleccionada
    id_contraseña = tabla.item(item, "values")[0]

    # Conectar a la base de datos SQLite
    conexion = sqlite3.connect("contrasenas.db")
    cursor = conexion.cursor()

    # Eliminar la contraseña de la base de datos
    cursor.execute("DELETE FROM contrasenas WHERE id=?", (id_contraseña,))
    conexion.commit()
    conexion.close()

    # Eliminar la contraseña de la tabla
    tabla.delete(item)

    messagebox.showinfo("Éxito", "La contraseña ha sido eliminada exitosamente.")


# Función para cargar las contraseñas almacenadas en la base de datos en la tabla
def cargar_contraseñas():
    # Conectar a la base de datos SQLite
    conexion = sqlite3.connect("contrasenas.db")
    cursor = conexion.cursor()

    # Consultar las contraseñas guardadas en la tabla "contrasenas"
    cursor.execute("SELECT * FROM contrasenas")
    contrasenas = cursor.fetchall()

    conexion.close()

    # Borrar cualquier contenido previo de la tabla
    tabla.delete(*tabla.get_children())

    # Cargar las contraseñas en la tabla
    for contraseña in contrasenas:
        tabla.insert("", "end", values=contraseña)

# Función para habilitar o deshabilitar los botones de copiar y eliminar según la selección en la tabla
def agregar_botones(event):
    item = tabla.selection()
    if not item:
        copiar_button.config(state="disabled")
        eliminar_button.config(state="disabled")
    else:
        copiar_button.config(state="normal")
        eliminar_button.config(state="normal")

# Función para abrir el gestor de contraseñas en una nueva ventana
def abrir_gestor_contrasenas():
    ventana_gestor = tk.Toplevel(ventana)
    ventana_gestor.title("Gestor de Contraseñas")
    ventana_gestor.geometry("600x400")
    ventana_gestor.attributes("-toolwindow", True)
    centrar_ventana(ventana_gestor) 
    # Crear tabla para mostrar las contraseñas guardadas
    global tabla
    tabla = ttk.Treeview(ventana_gestor, columns=("ID", "Sitio", "Usuario", "Clave"), show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Sitio", text="Sitio")
    tabla.heading("Usuario", text="Usuario")
    tabla.heading("Clave", text="Clave")
    tabla.pack(pady=10)

    # Vincular el evento <<TreeviewSelect>> a la función agregar_botones
    tabla.bind("<<TreeviewSelect>>", agregar_botones)

    # Agregar botones para copiar y eliminar contraseñas
    global copiar_button
    global eliminar_button
    copiar_button = tk.Button(ventana_gestor, text="Copiar Contraseña", command=copiar_contrasena, state="disabled")
    eliminar_button = tk.Button(ventana_gestor, text="Eliminar Contraseña", command=eliminar_contrasena, state="disabled")
    copiar_button.pack(side="left", padx=5, pady=5)
    eliminar_button.pack(side="left", padx=5, pady=5)

    # Establecer el ancho de las columnas
    tabla.column("ID", width=30, anchor="center")
    tabla.column("Sitio", width=150)
    tabla.column("Usuario", width=150)
    tabla.column("Clave", width=200)

    # Cargar contraseñas en la tabla
    cargar_contraseñas()

# Función para habilitar o deshabilitar los botones de copiar y eliminar según la selección en la tabla
def habilitar_botones(tabla, copiar_button, eliminar_button):
    item = tabla.selection()
    if not item:
        copiar_button.config(state="disabled")
        eliminar_button.config(state="disabled")
    else:
        copiar_button.config(state="normal")
        eliminar_button.config(state="normal")

# Función para salir de la aplicación
def salir():
    ventana.quit()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Generador de contraseñas seguras - ISTG")
ventana.geometry("720x700")  # Establecer el tamaño de la ventana

# Centrar la ventana en la pantalla
ventana.update_idletasks()
ancho_ventana = ventana.winfo_width()
alto_ventana = ventana.winfo_height()
x_pantalla = int((ventana.winfo_screenwidth() / 2) - (ancho_ventana / 2))
y_pantalla = int((ventana.winfo_screenheight() / 2) - (alto_ventana / 2))
ventana.geometry("+{}+{}".format(x_pantalla, y_pantalla))

# Bloquear el cambio de tamaño del formulario
ventana.resizable(False, False)

# Aplicar tema Material Design
style = ThemedStyle(ventana)
style.set_theme("arc")  # Seleccionar el tema "arc" (Material Design)

# Crear el menú
menu_principal = tk.Menu(ventana)
ventana.config(menu=menu_principal)

# Agregar opciones al menú
menu_archivo = tk.Menu(menu_principal, tearoff=0)
menu_principal.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Gestor de contraseñas - ISTG", command=abrir_gestor_contrasenas)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=ventana.quit)

# Campos del formulario (dispuestos verticalmente)
titulo_label = ttk.Label(ventana, text="Gestor de contraseñas - ISTG", font=('Arial', 18, 'bold'))
titulo_label.pack(pady=10)

# Cargar y agregar el logo al formulario
try:
    logo_img = Image.open("logo.png")
    logo_img = logo_img.resize((200, 200), Image.LANCZOS)  # Ajustar el tamaño del logo
    logo_img = ImageTk.PhotoImage(logo_img)

    logo_label = ttk.Label(ventana, image=logo_img)
    logo_label.pack(pady=10)
except FileNotFoundError:
    print("Error: No se pudo cargar el logo.")
    logo_label = ttk.Label(ventana, text="Logo no encontrado")
    logo_label.pack(pady=10)

# Opciones de generación de contraseñas
opciones_frame = ttk.Frame(ventana)
opciones_frame.pack(pady=10)

longitud_label = ttk.Label(opciones_frame, text="Longitud de la contraseña:")
longitud_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
longitud_entry = ttk.Entry(opciones_frame)
longitud_entry.grid(row=0, column=1, padx=5, pady=5)
longitud_entry.insert(0, "12")  # Valor predeterminado para la longitud

letras_var = tk.BooleanVar(value=True)
letras_checkbox = ttk.Checkbutton(opciones_frame, text="Incluir letras minúsculas", variable=letras_var)
letras_checkbox.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

mayusculas_var = tk.BooleanVar(value=True)
mayusculas_checkbox = ttk.Checkbutton(opciones_frame, text="Incluir letras mayúsculas", variable=mayusculas_var)
mayusculas_checkbox.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

numeros_var = tk.BooleanVar(value=True)
numeros_checkbox = ttk.Checkbutton(opciones_frame, text="Incluir números", variable=numeros_var)
numeros_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

simbolos_var = tk.BooleanVar(value=True)
simbolos_checkbox = ttk.Checkbutton(opciones_frame, text="Incluir símbolos", variable=simbolos_var)
simbolos_checkbox.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

# Botón para generar la contraseña segura
generar_boton = ttk.Button(ventana, text="Generar contraseña segura", command=generar_contrasena_segura)
generar_boton.pack(pady=10)

# Caja de texto para mostrar la contraseña generada
contrasena_label = ttk.Label(ventana, text="Contraseña generada:", font=('Arial', 14))
contrasena_label.pack()
contrasena_text = tk.Text(ventana, height=1, wrap=tk.WORD, font=('Arial', 14))
contrasena_text.pack(pady=10)

# Botón para guardar la contraseña
guardar_boton = ttk.Button(ventana, text="Guardar contraseña", command=guardar_contrasena)
guardar_boton.pack(pady=10)

# Crear tabla "contrasenas" en la base de datos si no existe
crear_tabla()

# Funciones para copiar, eliminar y cargar contraseñas en la tabla
tabla = None
copiar_button = None
eliminar_button = None

# Crear botón para abrir el gestor de contraseñas en una nueva ventana
abrir_gestor_button = ttk.Button(ventana, text="Abrir Gestor de Contraseñas", command=abrir_gestor_contrasenas)
abrir_gestor_button.pack(pady=10)

# Crear el botón para salir de la aplicación
salir_button = ttk.Button(ventana, text="Salir", command=salir)
salir_button.pack(pady=10)

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
