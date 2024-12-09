#Hecho Por:
#-----Hector Alejandro Ortega Garcia
#Grupo: 7F
#Registro: 21310248
#Materia: Sistemas expertosP

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog, messagebox
import json
from PIL import Image, ImageTk

class GuiaSimbolosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Guía de Símbolos y Normas de Dibujo Técnico")
        self.root.geometry("1100x900")
        
        # Cargar base de conocimiento
        self.base_conocimiento = self.cargar_base_conocimiento("base_conocimiento.json")
        #print(self.base_conocimiento)
        self.simbolos = self.base_conocimiento.get("simbolos", [])

        # Estado del cuestionario
        self.preguntas = self.base_conocimiento.get("preguntas", [])
        self.respuestas = []
        self.pregunta_actual = 0

        # Interfaz inicial
        self.mostrar_menu()


    # Función para guardar un nuevo símbolo
    def guardar_simbolo(self, simbolo):

        base = self.base_conocimiento
        base["simbolos"].append(simbolo)
        with open("base_conocimiento.json", "w") as archivo:
            json.dump(base, archivo, indent=4)
        messagebox.showinfo("Éxito", "Símbolo agregado correctamente.") 
    # Función para abrir el formulario de añadir símbolo
    def agregar_simbolo(self):
        def guardar_datos():
            nombre = entry_nombre.get()
            descripcion = entry_descripcion.get("1.0", tk.END).strip()
            norma = entry_norma.get()
            categoria = entry_categoria.get()
            imagen = entry_imagen["text"]

            if not all([nombre, descripcion, norma, categoria, imagen]):
                messagebox.showerror("Error", "Por favor, completa todos los campos.")
                return

            nuevo_simbolo = {
                "nombre": nombre,
                "descripcion": descripcion,
                "norma": norma,
                "categoria": categoria,
                "imagen": imagen,
            }
            self.guardar_simbolo(nuevo_simbolo)
            ventana_agregar.destroy()

        def seleccionar_imagen():
            ruta_imagen = filedialog.askopenfilename(
                title="Seleccionar imagen",
                filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")]
            )
            if ruta_imagen:
                entry_imagen["text"] = ruta_imagen

        ventana_agregar = tk.Toplevel(root)
        ventana_agregar.title("Agregar Símbolo")
        ventana_agregar.geometry("400x400")

        tk.Label(ventana_agregar, text="Nombre:").pack(pady=5)
        entry_nombre = tk.Entry(ventana_agregar)
        entry_nombre.pack(fill="x", padx=20)

        tk.Label(ventana_agregar, text="Descripción:").pack(pady=5)
        entry_descripcion = tk.Text(ventana_agregar, height=5)
        entry_descripcion.pack(fill="x", padx=20)

        tk.Label(ventana_agregar, text="Norma:").pack(pady=5)
        entry_norma = tk.Entry(ventana_agregar)
        entry_norma.pack(fill="x", padx=20)

        tk.Label(ventana_agregar, text="Categoría:").pack(pady=5)
        entry_categoria = tk.Entry(ventana_agregar)
        entry_categoria.pack(fill="x", padx=20)

        tk.Label(ventana_agregar, text="Imagen:").pack(pady=5)
        entry_imagen = tk.Label(ventana_agregar, text="", relief="sunken", anchor="w")
        entry_imagen.pack(fill="x", padx=20)
        tk.Button(ventana_agregar, text="Seleccionar Imagen", command=seleccionar_imagen).pack(pady=5)

        tk.Button(ventana_agregar, text="Guardar", command=guardar_datos).pack(pady=20)

    def cargar_base_conocimiento(self, archivo):
        try:
            with open(archivo, "r", encoding="utf8") as file:
                return json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo {archivo}.")
            return {"simbolos": []}
        except json.JSONDecodeError:
            messagebox.showerror("Error", "El archivo JSON tiene un formato incorrecto.")
            return {"simbolos": []}

    def mostrar_menu(self):
        """Muestra el menú principal con las dos opciones."""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, bootstyle="primary")
        frame.pack(fill="both")
        ttk.Label(frame, text="Selecciona una opción:", font=("Arial", 16), bootstyle="inverse-primary").pack(pady=20)

        frame2 = ttk.Frame(self.root, bootstyle="light")
        frame2.pack(side="left", fill="y")

        frame_buscar = ttk.Frame(frame2, bootstyle = "light")
        frame_buscar.pack(pady=20)

        frame_cuest = ttk.Frame(frame2, bootstyle = "light")
        frame_cuest.pack(pady=20)

        ttk.Label(frame_buscar, text="¿Quieres buscar un símbolo en especifico?:", font=("Arial", 12), bootstyle = "inverse-light").pack(pady=5)
        ttk.Button(frame_buscar, text="Buscar un símbolo", bootstyle=SUCCESS, command=self.mostrar_busqueda).pack(pady=10)

        ttk.Label(frame_cuest, text="Haz nuestro cuestionario para guiarte en los\n simbolos que necesitas implementar en tu dibujo",font=("Arial", 12), justify="center", bootstyle = "inverse-light").pack(pady=5)
        ttk.Button(frame_cuest, text="Hacer el cuestionario", bootstyle=INFO, command=self.iniciar_cuestionario).pack(pady=10)
        # Cargar la imagen y redimensionarla para que se ajuste

        img = Image.open("imagenes/CAD.png")
        img.thumbnail((700, 500))  # Redimensionar para que quepa
        photo = ImageTk.PhotoImage(img)
        ttk.Label(self.root, image=photo).pack(side=RIGHT)
        self.img_ref = photo

        #ttk.Label(self.root, text="Agregar un nuevo simbolo de dibujo",font=("Arial", 16), justify="center").pack(pady=20)
        #ttk.Button(self.root, text="Agregar simbolo", bootstyle=PRIMARY, command=self.agregar_simbolo).pack(pady=10)
    
    def iniciar_cuestionario(self):
        """Inicia el cuestionario."""
        self.respuestas = []
        self.pregunta_actual = 0
        self.mostrar_pregunta()

    def on_frame_configure(self, event):
        """ Ajustar el scroll del canvas al tamaño del contenido. """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#---------------------------------------Funciones para el cuestionario-----------------------------------------------------------
    def mostrar_pregunta(self):
        """Muestra una pregunta del cuestionario."""
        for widget in self.root.winfo_children():
            widget.destroy()

        label_frame = ttk.Frame(self.root, bootstyle=PRIMARY)
        label_frame.pack(fill="both")
        ttk.Label(label_frame, text="Cuestionario", font=("Arial", 14), bootstyle="inverse_primary").pack(pady=10)

        frame_preguntas = ttk.Frame(self.root)
        frame_preguntas.pack(fill="both", padx=10, pady=10)

        self.variables = {}  # Almacena las variables asociadas a los Checkbuttons

        for i, pregunta in enumerate(self.preguntas):
            var = tk.BooleanVar()  # Crear una variable BooleanVar para cada pregunta
            self.variables[i] = var  # Guardar la variable en el diccionario con el índice de la pregunta como clave

            pregunta_frame = ttk.Frame(frame_preguntas)
            pregunta_frame.pack(fill="x", pady=5)

            ttk.Label(pregunta_frame, text=pregunta["pregunta"], font=("Arial", 12), anchor="w").pack(side="left", padx=5)
            ttk.Checkbutton(pregunta_frame, variable=var, bootstyle="success").pack(side="right", padx=5)

        # Botón para enviar las respuestas
        ttk.Button(
            self.root,
            text="Enviar",
            bootstyle="primary",
            command=self.registrar_respuestas,  # Referencia a la función, sin paréntesis
        ).pack(pady=10)

    def registrar_respuestas(self):
        """Registra las respuestas del usuario y las guarda en una lista."""
        self.respuestas = []  # Reinicia la lista de respuestas
        for i, var in self.variables.items():
            respuesta = var.get()  # Obtener el valor de la variable (True o False)
            self.respuestas.append(respuesta)  # Guardar la respuesta
            print(f"Pregunta {i + 1}: {'Sí' if respuesta else 'No'}")  # Imprimir para depuración

        # Aquí puedes realizar otras acciones con las respuestas
        print("Respuestas registradas:", self.respuestas)
        self.mostrar_resultados_cuestionario()

        #self.pregunta_actual += 1
        #self.mostrar_pregunta()

    def mostrar_resultados_cuestionario(self):
        """Muestra los resultados del cuestionario."""
        
        # Limpiar la interfaz para mostrar los resultados
        for widget in self.root.winfo_children():
            widget.destroy()

        simbolos_recomendados = []
        for idx, respuesta in enumerate(self.respuestas):
            if respuesta:
                simbolos_recomendados.extend(self.preguntas[idx]["respuesta_si"])

        simbolos_recomendados = list(set(simbolos_recomendados))  # Eliminar duplicados

        if simbolos_recomendados:
            label_frame = ttk.Frame(self.root, bootstyle=PRIMARY)
            label_frame.pack(fill="both")
            ttk.Label(label_frame, text="Símbolos recomendados:", font=("Arial", 14), bootstyle="inverse-primary").pack(pady=10)

            # Crear una lista de símbolos con sus nombres para el ComboBox
            simbolos_detalles = []

            for simbolo_nombre in simbolos_recomendados:
                simbolo = next(s for s in self.simbolos if s["nombre"] == simbolo_nombre)
                simbolos_detalles.append(simbolo)  # Guardamos el símbolo completo en lugar solo del nombre

                # Mostrar los símbolos recomendados
                ttk.Label(self.root, text=f"- {simbolo['nombre']}:", font=("Arial", 12)).pack(anchor="w", padx=20)


            # Crear el ComboBox para seleccionar un símbolo recomendado
            frame = ttk.Frame(self.root, bootstyle = "light")
            frame.pack(fill="both", side="bottom")
            ttk.Label(frame, text="Selecciona una opcion para mas detalles", font=("Arial", 14), bootstyle = "inverse-light").pack(anchor="w")
            self.combo_simbolos = ttk.Combobox(frame, font=("Arial", 12), state="readonly")
            self.combo_simbolos['values'] = [simbolo['nombre'] for simbolo in simbolos_detalles]
            self.combo_simbolos.pack(pady=10, fill="x", padx=20)

            # Cuando el usuario seleccione un símbolo, mostrar más detalles
            self.combo_simbolos.bind("<<ComboboxSelected>>", lambda event: self.mostrar_detalles_simbolo(simbolos_detalles))

        else:
            ttk.Label(self.root, text="No se encontraron recomendaciones.", font=("Arial", 14)).pack(pady=10)
            ttk.Button(self.root, text="Volver al menú", bootstyle=SECONDARY, command=self.mostrar_menu).pack(pady=20)
        
        # Botón para volver al menú
        ttk.Button(frame, text="Volver al menú", bootstyle=SECONDARY, command=self.mostrar_menu).pack(pady=20)

    def mostrar_detalles_simbolo(self, simbolos_detalles):
        """Muestra más detalles del símbolo seleccionado desde el ComboBox."""
        seleccionado = self.combo_simbolos.get()

        # Buscar el símbolo seleccionado en la lista de detalles
        simbolo = next(s for s in simbolos_detalles if s["nombre"] == seleccionado)

        # Limpiar el área de resultados previos
        for widget in self.root.winfo_children():
            widget.destroy()

        # Mostrar detalles del símbolo seleccionado
        frame = ttk.Frame(self.root, bootstyle = "info")
        frame.pack(fill="both")
        ttk.Label(frame, text=f"Nombre: {simbolo['nombre']}", font=("Arial", 12, "bold"), bootstyle = "inverse-info").pack(pady=20)
        ttk.Label(self.root, text=f"Descripción: \n{simbolo['descripcion']}", wraplength=700, justify="left", font = ("Arial", 12)).pack(anchor="w", padx=10)

        try:
            img = Image.open(f"imagenes/{simbolo['imagen']}")
            img.thumbnail((400, 400))  # Redimensionar para que quepa
            photo = ImageTk.PhotoImage(img)
            ttk.Label(self.root, image=photo).pack(anchor="center", pady=10)
            self.img_ref = photo
        except FileNotFoundError:
            ttk.Label(self.root, text="(Imagen no disponible)").pack(anchor="w")
        
        # Botón para volver a los resultados
        frame = ttk.Frame(self.root, bootstyle = "light")
        frame.pack(fill="both", side="bottom")
        ttk.Button(frame, text="Volver a los resultados", bootstyle=SECONDARY, command=self.mostrar_resultados_cuestionario).pack(pady =20)


#-----------------------------------------------------Funciones para busqueda-----------------------------------------------------------------------------------
    def mostrar_busqueda(self):
        """Muestra la interfaz de búsqueda."""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Etiqueta de búsqueda
        frame = ttk.Frame(self.root, bootstyle=SUCCESS)
        frame.pack(fill="both")
        ttk.Label(frame, text="Buscar símbolo:", font=("Arial", 14), bootstyle = "inverse-success").pack(pady=10)

        # Botón de búsqueda
        frame2 = ttk.Frame(self.root)
        frame2.pack(fill="both", pady=15)
        # Campo de búsqueda
        ttk.Label(frame2, text="Introduce el simbolo que deseas buscar", font=("Arial", 12)).pack(pady=5)
        self.entry_busqueda = ttk.Entry(frame2, font=("Arial", 12), bootstyle = "default")
        self.entry_busqueda.pack(pady=5, fill="x", padx=20)
        ttk.Button(frame2, text="Buscar", bootstyle=PRIMARY, command=self.buscar_simbolo).pack(pady=5)
        #Boton para regresar al menu principal
        ttk.Button(frame2, text="Regresar al menu", bootstyle=SECONDARY, command=self.mostrar_menu).pack(pady=5)

        # Frame principal para scrollbar
        self.frame_scroll = ttk.Frame(self.root)
        self.frame_scroll.pack(pady=10, fill="both", expand=True)

        # Canvas para hacer el frame desplazable
        self.canvas = ttk.Canvas(self.frame_scroll, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame_scroll, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Vincular scrollbar con canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame que contendrá los resultados dentro del canvas
        self.frame_resultados = ttk.Frame(self.canvas)
        self.frame_resultados.pack(fill="x")
        

        # Agregar el frame_resultados al canvas
        self.canvas.create_window((0, 0), window=self.frame_resultados)

        # Configurar el canvas para redimensionar automáticamente
        self.frame_resultados.bind("<Configure>", self.on_frame_configure)

    def buscar_simbolo(self):
        # Limpiar el frame de resultados
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()

        # Limpiar cualquier ComboBox existente
        if hasattr(self, 'combo_simbolos') and self.combo_simbolos.winfo_exists():
            self.combo_simbolos.destroy()

        if hasattr(self, 'label_selection') and self.label_selection.winfo_exists():
            self.label_selection.destroy()

        if hasattr(self, 'frame_opciones') and self.frame_opciones.winfo_exists():
            self.frame_opciones.destroy()

        # Obtener texto de búsqueda
        termino = self.entry_busqueda.get().lower()
        termino = termino.capitalize()

        # Buscar símbolos que coincidan
        resultados = [s for s in self.simbolos if termino in s["nombre"]]
        resultados2 = [s for s in self.simbolos if termino in s["categoria"]]
        print("Esete es el resultado 1\n", resultados)
        print("Este es el resultado 2\n", resultados2)

        # Mostrar resultados en la interfaz
        if resultados or resultados2:
            
            if resultados:
                simbolo_buscado = resultados[0]  # Tomamos el primer resultado
                print("Este es el simbolo buscado1:\n")
                categoria_buscada = simbolo_buscado['categoria'] # Obtener categoría del símbolo buscado

                # Mostrar información del símbolo buscado
                ttk.Label(self.frame_resultados, text=f"Nombre: {simbolo_buscado['nombre']}", font=("Arial", 12, "bold")).pack(anchor="w")
                ttk.Label(self.frame_resultados, text=f"Descripción: {simbolo_buscado['descripcion']}", wraplength=700, justify="left").pack(anchor="w", padx=10)

                # Mostrar imagen del símbolo
                try:
                    ttk.Label(self.frame_resultados, text="Norma: " + simbolo_buscado["norma"]).pack(anchor="w")
                    img = Image.open(f"imagenes/{simbolo_buscado['imagen']}")
                    img.thumbnail((400, 400))  # Redimensionar para que quepa
                    photo = ImageTk.PhotoImage(img)
                    ttk.Label(self.frame_resultados, image=photo).pack(anchor="center")
                    self.img_ref = photo
                except FileNotFoundError:
                    ttk.Label(self.frame_resultados, text="(Imagen no disponible)").pack(anchor="w")

                # Buscar otros símbolos en la misma categoría, excluyendo el símbolo buscado
                simbolos_relacionados = [s for s in self.simbolos if s['categoria'] == categoria_buscada and s['nombre'] != simbolo_buscado['nombre']]
            
            elif resultados2:
                simbolo_buscado = resultados2[0]  # Tomamos el primer resultado
                print("Este es el simbolo buscado2:\n")
                categoria_buscada = simbolo_buscado['categoria'] # Obtener categoría del símbolo buscado
                simbolos_relacionados = [s for s in self.simbolos if s['categoria'] == categoria_buscada]
                ttk.Label(self.frame_resultados, text=f"En la categoria de : {simbolo_buscado['categoria']} existen varios simbolos\nPor favor selecciona el de tu interés", font=("Arial", 12, "bold")).pack(side="right")

            # Actualizar el ComboBox con los símbolos relacionados
            if simbolos_relacionados:
                self.frame_opciones = ttk.Frame(self.root, style="light.TFrame")
                self.frame_opciones.pack(fill="both")

                self.combo_simbolos = ttk.Combobox(self.frame_opciones, font=("Arial", 12), state="readonly", style="info")
                self.combo_simbolos['values'] = [s['nombre'] for s in simbolos_relacionados]

                self.label_selection = ttk.Label(self.frame_opciones,bootstyle = "inverse-light", text="Seleccione un símbolo relacionado:", font=("Arial", 12))
                self.label_selection.pack(pady=10)
                
                self.combo_simbolos.pack(pady=5, fill="x", padx=20)
                self.combo_simbolos.bind("<<ComboboxSelected>>", self.mostrar_informacion_simbolo)
            else:
                self.combo_simbolos['values'] = []

            self.combo_simbolos.set('')  # Limpiar selección previa

        else:
            ttk.Label(self.frame_resultados, text="No se encontraron símbolos.", font=("Arial", 12)).pack(pady=10)
            

    def mostrar_informacion_simbolo(self, event):
        simbolo_seleccionado = self.combo_simbolos.get()

        if simbolo_seleccionado:
            # Buscar el símbolo seleccionado
            simbolo = next((s for s in self.simbolos if s['nombre'] == simbolo_seleccionado), None)

            categoria_buscada = simbolo['categoria'] # Obtener categoría del símbolo buscado
            simbolos_relacionados = [s for s in self.simbolos if s['categoria'] == categoria_buscada and s['nombre'] != simbolo['nombre']]
            self.combo_simbolos['values'] = [s['nombre'] for s in simbolos_relacionados]

            if simbolo:
                # Limpiar resultados anteriores
                for widget in self.frame_resultados.winfo_children():
                    widget.destroy()

                # Mostrar información del símbolo
                ttk.Label(self.frame_resultados, text=f"Nombre: {simbolo['nombre']}", font=("Arial", 12, "bold")).pack()
                ttk.Label(self.frame_resultados, text=f"Descripción: {simbolo['descripcion']}", wraplength=700, justify="left").pack()
                ttk.Label(self.frame_resultados, text="Norma: " + simbolo["norma"]).pack()

                # Mostrar imagen del símbolo
                try:
                    img = Image.open(f"imagenes/{simbolo['imagen']}")
                    img.thumbnail((400, 400))  # Redimensionar para que quepa
                    photo = ImageTk.PhotoImage(img)
                    ttk.Label(self.frame_resultados, image=photo).pack(anchor="center")
                    self.img_ref = photo
                except FileNotFoundError:
                    ttk.Label(self.frame_resultados, text="(Imagen no disponible)").pack(anchor="w")

            
# Ejecutar aplicación
root = ttk.Window(themename="cosmo")
app = GuiaSimbolosApp(root)
root.mainloop()
