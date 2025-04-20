import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from modelos import GestorNotas
from validaciones import Validador

class SistemaGestionNotas:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Notas")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Inicializar gestor de notas
        self.gestor = GestorNotas()
        
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.tab_inicio = ttk.Frame(self.notebook)
        self.tab_listar = ttk.Frame(self.notebook)
        self.tab_agregar = ttk.Frame(self.notebook)
        self.tab_consultar = ttk.Frame(self.notebook)
        self.tab_modificar = ttk.Frame(self.notebook)
        self.tab_eliminar = ttk.Frame(self.notebook)
        self.tab_exportar = ttk.Frame(self.notebook)
        
        # Añadir pestañas al notebook
        self.notebook.add(self.tab_inicio, text="Inicio")
        self.notebook.add(self.tab_listar, text="Listar")
        self.notebook.add(self.tab_agregar, text="Agregar")
        self.notebook.add(self.tab_consultar, text="Consultar")
        self.notebook.add(self.tab_modificar, text="Modificar")
        self.notebook.add(self.tab_eliminar, text="Eliminar")
        self.notebook.add(self.tab_exportar, text="Exportar Eliminados")
        
        # Configurar cada pestaña
        self.configurar_tab_inicio()
        self.configurar_tab_listar()
        self.configurar_tab_agregar()
        self.configurar_tab_consultar()
        self.configurar_tab_modificar()
        self.configurar_tab_eliminar()
        self.configurar_tab_exportar()
        
        # Añadir evento al cambiar de pestaña para refrescar datos
        self.notebook.bind("<<NotebookTabChanged>>", self.actualizar_tab_actual)
    
    def actualizar_tab_actual(self, event=None):
        """Actualiza los datos de la pestaña actual."""
        tab_idx = self.notebook.index(self.notebook.select())
        
        # Actualizar según la pestaña seleccionada
        if tab_idx == 0:  # Inicio
            self.actualizar_estadisticas()
        elif tab_idx == 1:  # Listar
            self.listar_registros()
        elif tab_idx == 6:  # Exportar Eliminados
            self.listar_registros_eliminados()
    
    def configurar_tab_inicio(self):
        # Pestaña de inicio - Bienvenida
        lbl_titulo = ttk.Label(self.tab_inicio, text="Sistema de Gestión de Notas", font=("Arial", 18, "bold"))
        lbl_titulo.pack(pady=40)
        
        lbl_descripcion = ttk.Label(self.tab_inicio, text="Bienvenido al sistema de gestión de notas.\nUtilice las pestañas para navegar por las diferentes opciones.", font=("Arial", 12))
        lbl_descripcion.pack(pady=20)
        
        # Estadísticas básicas
        frame_stats = ttk.LabelFrame(self.tab_inicio, text="Estadísticas")
        frame_stats.pack(pady=20, padx=20, fill="x")
        
        self.lbl_estudiantes = ttk.Label(frame_stats, text="Total de estudiantes: 0")
        self.lbl_estudiantes.pack(anchor="w", padx=10, pady=5)
        
        self.lbl_promedio = ttk.Label(frame_stats, text="Promedio general: 0.0")
        self.lbl_promedio.pack(anchor="w", padx=10, pady=5)
        
        self.lbl_max_nota = ttk.Label(frame_stats, text="Nota más alta: 0")
        self.lbl_max_nota.pack(anchor="w", padx=10, pady=5)
        
        self.lbl_min_nota = ttk.Label(frame_stats, text="Nota más baja: 0")
        self.lbl_min_nota.pack(anchor="w", padx=10, pady=5)
        
        # Actualizar estadísticas
        self.actualizar_estadisticas()
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas en la pestaña de inicio."""
        stats = self.gestor.obtener_estadisticas()
        
        self.lbl_estudiantes.config(text=f"Total de estudiantes: {stats['total_estudiantes']}")
        self.lbl_promedio.config(text=f"Promedio general: {stats['promedio_general']}")
        self.lbl_max_nota.config(text=f"Nota más alta: {stats['nota_maxima']}")
        self.lbl_min_nota.config(text=f"Nota más baja: {stats['nota_minima']}")
    
    def configurar_tab_listar(self):
        # Pestaña de listar - Tabla con todos los registros + Ordenamiento
        lbl_titulo = ttk.Label(self.tab_listar, text="Listado de Estudiantes", font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=10)
        
        # Frame para opciones de ordenamiento
        frame_ordenar = ttk.LabelFrame(self.tab_listar, text="Ordenar datos")
        frame_ordenar.pack(fill="x", padx=20, pady=5)
        
        # Criterio de ordenamiento
        lbl_criterio = ttk.Label(frame_ordenar, text="Ordenar por:")
        lbl_criterio.grid(row=0, column=0, padx=5, pady=5)
        
        self.combo_criterio = ttk.Combobox(frame_ordenar, values=["ID", "Nombre", "Apellido", "Asignatura", "Nota"])
        self.combo_criterio.current(0)  # Seleccionar el primer elemento por defecto
        self.combo_criterio.grid(row=0, column=1, padx=5, pady=5)
        
        # Tipo de orden
        self.rb_orden = tk.StringVar(value="asc")
        rb_asc = ttk.Radiobutton(frame_ordenar, text="Ascendente", variable=self.rb_orden, value="asc")
        rb_asc.grid(row=0, column=2, padx=5, pady=5)
        
        rb_desc = ttk.Radiobutton(frame_ordenar, text="Descendente", variable=self.rb_orden, value="desc")
        rb_desc.grid(row=0, column=3, padx=5, pady=5)
        
        # Botón para ordenar
        btn_ordenar = ttk.Button(frame_ordenar, text="Ordenar", command=self.ordenar_registros)
        btn_ordenar.grid(row=0, column=4, padx=5, pady=5)
        
        # Tabla
        frame_tabla = ttk.Frame(self.tab_listar)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear treeview (tabla)
        self.treeview = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Apellido", "Asignatura", "Nota"), show="headings")
        
        # Definir encabezados
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Nombre", text="Nombre")
        self.treeview.heading("Apellido", text="Apellido")
        self.treeview.heading("Asignatura", text="Asignatura")
        self.treeview.heading("Nota", text="Nota")
        
        # Definir anchos de columna
        self.treeview.column("ID", width=50)
        self.treeview.column("Nombre", width=150)
        self.treeview.column("Apellido", width=150)
        self.treeview.column("Asignatura", width=150)
        self.treeview.column("Nota", width=50)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar elementos
        self.treeview.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón para refrescar
        btn_refrescar = ttk.Button(self.tab_listar, text="Refrescar", command=self.listar_registros)
        btn_refrescar.pack(pady=10)
        
        # Cargar registros iniciales
        self.listar_registros()
    
    def listar_registros(self):
        """Muestra todos los registros en la tabla."""
        # Limpiar tabla
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # Obtener registros
        registros = self.gestor.obtener_registros()
        
        # Insertar registros en la tabla
        for registro in registros:
            self.treeview.insert("", "end", values=(
                registro["ID"],
                registro["Nombre"],
                registro["Apellido"],
                registro["Asignatura"],
                registro["Nota"]
            ))
    
    def ordenar_registros(self):
        """Ordena los registros según el criterio seleccionado."""
        criterio = self.combo_criterio.get()
        ascendente = self.rb_orden.get() == "asc"
        
        # Limpiar tabla
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # Obtener registros ordenados
        registros = self.gestor.ordenar_registros(criterio, ascendente)
        
        # Insertar registros en la tabla
        for registro in registros:
            self.treeview.insert("", "end", values=(
                registro["ID"],
                registro["Nombre"],
                registro["Apellido"],
                registro["Asignatura"],
                registro["Nota"]
            ))
    
    def configurar_tab_agregar(self):
        # Pestaña de agregar - Formulario
        lbl_titulo = ttk.Label(self.tab_agregar, text="Agregar Nuevo Estudiante", font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=10)
        
        # Frame del formulario
        frame_form = ttk.Frame(self.tab_agregar)
        frame_form.pack(fill="both", padx=50, pady=20)
        
        # Nota sobre ID automático
        lbl_id_auto = ttk.Label(frame_form, text="El ID se generará automáticamente", font=("Arial", 10, "italic"))
        lbl_id_auto.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        
        # Nombre
        lbl_nombre = ttk.Label(frame_form, text="Nombre:")
        lbl_nombre.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_nombre = ttk.Entry(frame_form, width=30)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Validación en tiempo real
        vcmd_nombre = (self.root.register(self.validar_nombre), '%P')
        self.entry_nombre.config(validate="key", validatecommand=vcmd_nombre)
        self.lbl_error_nombre = ttk.Label(frame_form, text="", foreground="red")
        self.lbl_error_nombre.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        
        # Apellido
        lbl_apellido = ttk.Label(frame_form, text="Apellido:")
        lbl_apellido.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_apellido = ttk.Entry(frame_form, width=30)
        self.entry_apellido.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Validación en tiempo real
        vcmd_apellido = (self.root.register(self.validar_apellido), '%P')
        self.entry_apellido.config(validate="key", validatecommand=vcmd_apellido)
        self.lbl_error_apellido = ttk.Label(frame_form, text="", foreground="red")
        self.lbl_error_apellido.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        
        # Asignatura
        lbl_asignatura = ttk.Label(frame_form, text="Asignatura:")
        lbl_asignatura.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_asignatura = ttk.Entry(frame_form, width=30)
        self.entry_asignatura.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        # Validación en tiempo real
        vcmd_asignatura = (self.root.register(self.validar_asignatura), '%P')
        self.entry_asignatura.config(validate="key", validatecommand=vcmd_asignatura)
        self.lbl_error_asignatura = ttk.Label(frame_form, text="", foreground="red")
        self.lbl_error_asignatura.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        
        # Nota
        lbl_nota = ttk.Label(frame_form, text="Nota (0-50):")
        lbl_nota.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.entry_nota = ttk.Entry(frame_form, width=30)
        self.entry_nota.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        # Validación en tiempo real
        vcmd_nota = (self.root.register(self.validar_nota), '%P')
        self.entry_nota.config(validate="key", validatecommand=vcmd_nota)
        self.lbl_error_nota = ttk.Label(frame_form, text="", foreground="red")
        self.lbl_error_nota.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        
        # Botón para guardar
        btn_guardar = ttk.Button(frame_form, text="Guardar", command=self.guardar_estudiante)
        btn_guardar.grid(row=5, column=0, columnspan=2, pady=20)
    
    def validar_nombre(self, valor):
        """Valida el nombre en tiempo real."""
        if valor == "":
            self.lbl_error_nombre.config(text="")
            return True
        
        if Validador.validar_texto_alfabetico(valor):
            self.lbl_error_nombre.config(text="")
            return True
        else:
            self.lbl_error_nombre.config(text="Solo letras y espacios")
            return True  # Devuelve True para permitir la edición pero muestra el error
    
    def validar_apellido(self, valor):
        """Valida el apellido en tiempo real."""
        if valor == "":
            self.lbl_error_apellido.config(text="")
            return True
        
        if Validador.validar_texto_alfabetico(valor):
            self.lbl_error_apellido.config(text="")
            return True
        else:
            self.lbl_error_apellido.config(text="Solo letras y espacios")
            return True
    
    def validar_asignatura(self, valor):
        """Valida la asignatura en tiempo real."""
        if valor == "":
            self.lbl_error_asignatura.config(text="")
            return True
        
        if Validador.validar_alfanumerico(valor):
            self.lbl_error_asignatura.config(text="")
            return True
        else:
            self.lbl_error_asignatura.config(text="Caracteres no válidos")
            return True
    
    def validar_nota(self, valor):
        """Valida la nota en tiempo real."""
        if valor == "":
            self.lbl_error_nota.config(text="")
            return True
        
        es_valida, mensaje = Validador.validar_nota(valor)
        if es_valida:
            self.lbl_error_nota.config(text="")
        else:
            self.lbl_error_nota.config(text=mensaje)
        
        return True
    
    def guardar_estudiante(self):
        """Guarda un nuevo estudiante."""
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        asignatura = self.entry_asignatura.get().strip()
        nota = self.entry_nota.get().strip()
        
        # Validar campos
        es_valido, mensaje = Validador.validar_campos_estudiante(nombre, apellido, asignatura, nota)
        
        if not es_valido:
            messagebox.showerror("Error de validación", mensaje)
            return
        
        # Guardar estudiante
        if self.gestor.agregar_registro(nombre, apellido, asignatura, nota):
            messagebox.showinfo("Éxito", "Estudiante guardado correctamente")
            
            # Limpiar campos
            self.entry_nombre.delete(0, tk.END)
            self.entry_apellido.delete(0, tk.END)
            self.entry_asignatura.delete(0, tk.END)
            self.entry_nota.delete(0, tk.END)

        else:
            messagebox.showerror("Error", "No se pudo guardar el estudiante")
    
    def configurar_tab_consultar(self):
        # Pestaña de consultar - Búsqueda y resultados
        lbl_titulo = ttk.Label(self.tab_consultar, text="Consultar Estudiantes", font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=10)
        
        # Frame de búsqueda
        frame_busqueda = ttk.Frame(self.tab_consultar)
        frame_busqueda.pack(fill="x", padx=20, pady=10)
        
        # Tipo de búsqueda
        lbl_tipo = ttk.Label(frame_busqueda, text="Buscar por:")
        lbl_tipo.grid(row=0, column=0, padx=5, pady=5)
        
        self.combo_tipo_busqueda = ttk.Combobox(frame_busqueda, values=["ID", "Nombre", "Apellido", "Asignatura"])
        self.combo_tipo_busqueda.current(0)  # Seleccionar el primer elemento por defecto
        self.combo_tipo_busqueda.grid(row=0, column=1, padx=5, pady=5)
        
        # Término de búsqueda
        lbl_termino = ttk.Label(frame_busqueda, text="Término:")
        lbl_termino.grid(row=0, column=2, padx=5, pady=5)
        
        self.entry_termino_busqueda = ttk.Entry(frame_busqueda, width=30)
        self.entry_termino_busqueda.grid(row=0, column=3, padx=5, pady=5)
        
        # Botón de búsqueda
        btn_buscar = ttk.Button(frame_busqueda, text="Buscar", command=self.buscar_estudiantes)
        btn_buscar.grid(row=0, column=4, padx=5, pady=5)
        
        # Resultados
        frame_resultados = ttk.LabelFrame(self.tab_consultar, text="Resultados")
        frame_resultados.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Tabla de resultados
        self.treeview_resultados = ttk.Treeview(
            frame_resultados, 
            columns=("ID", "Nombre", "Apellido", "Asignatura", "Nota"), 
            show="headings"
        )
        
        # Definir encabezados
        self.treeview_resultados.heading("ID", text="ID")
        self.treeview_resultados.heading("Nombre", text="Nombre")
        self.treeview_resultados.heading("Apellido", text="Apellido")
        self.treeview_resultados.heading("Asignatura", text="Asignatura")
        self.treeview_resultados.heading("Nota", text="Nota")
        
        # Definir anchos de columna
        self.treeview_resultados.column("ID", width=50)
        self.treeview_resultados.column("Nombre", width=150)
        self.treeview_resultados.column("Apellido", width=150)
        self.treeview_resultados.column("Asignatura", width=150)
        self.treeview_resultados.column("Nota", width=50)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_resultados, orient="vertical", command=self.treeview_resultados.yview)
        self.treeview_resultados.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar elementos
        self.treeview_resultados.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def buscar_estudiantes(self):
        """Busca estudiantes según el criterio seleccionado."""
        criterio = self.combo_tipo_busqueda.get()
        termino = self.entry_termino_busqueda.get().strip()
        
        if not termino:
            messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda")
            return
        
        # Limpiar tabla de resultados
        for item in self.treeview_resultados.get_children():
            self.treeview_resultados.delete(item)
        
        # Realizar búsqueda
        resultados = self.gestor.buscar_registros(criterio, termino)
        
        if not resultados:
            messagebox.showinfo("Información", "No se encontraron resultados")
            return
        
        # Mostrar resultados
        for registro in resultados:
            self.treeview_resultados.insert("", "end", values=(
                registro["ID"],
                registro["Nombre"],
                registro["Apellido"],
                registro["Asignatura"],
                registro["Nota"]
            ))
    
    def configurar_tab_modificar(self):
        # Pestaña de modificar - Búsqueda y formulario
        lbl_titulo = ttk.Label(self.tab_modificar, text="Modificar Estudiante", font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=10)
        
        # Frame de búsqueda
        frame_busqueda = ttk.Frame(self.tab_modificar)
        frame_busqueda.pack(fill="x", padx=20, pady=10)
        
        # ID a modificar
        lbl_id = ttk.Label(frame_busqueda, text="ID del estudiante:")
        lbl_id.grid(row=0, column=0, padx=5, pady=5)
        
        self.entry_id_modificar = ttk.Entry(frame_busqueda, width=20)
        self.entry_id_modificar.grid(row=0, column=1, padx=5, pady=5)
        
        # Botón de búsqueda
        btn_buscar = ttk.Button(frame_busqueda, text="Buscar", command=self.cargar_estudiante_modificar)
        btn_buscar.grid(row=0, column=2, padx=5, pady=5)
        
        # Frame del formulario de edición
        self.frame_form_modificar = ttk.LabelFrame(self.tab_modificar, text="Editar datos")
        self.frame_form_modificar.pack(fill="both", padx=50, pady=20)
        
        # Campos del formulario
        # ID (solo lectura)
        lbl_id_ro = ttk.Label(self.frame_form_modificar, text="ID:")
        lbl_id_ro.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_id_ro = ttk.Entry(self.frame_form_modificar, width=30, state="readonly")
        self.entry_id_ro.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Nombre
        lbl_nombre = ttk.Label(self.frame_form_modificar, text="Nombre:")
        lbl_nombre.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_nombre_modificar = ttk.Entry(self.frame_form_modificar, width=30)
        self.entry_nombre_modificar.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Validación en tiempo real
        vcmd_nombre = (self.root.register(self.validar_nombre_modificar), '%P')
        self.entry_nombre_modificar.config(validate="key", validatecommand=vcmd_nombre)
        self.lbl_error_nombre_modificar = ttk.Label(self.frame_form_modificar, text="", foreground="red")
        self.lbl_error_nombre_modificar.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        
        # Apellido
        lbl_apellido = ttk.Label(self.frame_form_modificar, text="Apellido:")
        lbl_apellido.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_apellido_modificar = ttk.Entry(self.frame_form_modificar, width=30)
        self.entry_apellido_modificar.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Validación en tiempo real
        vcmd_apellido = (self.root.register(self.validar_apellido_modificar), '%P')
        self.entry_apellido_modificar.config(validate="key", validatecommand=vcmd_apellido)
        self.lbl_error_apellido_modificar = ttk.Label(self.frame_form_modificar, text="", foreground="red")
        self.lbl_error_apellido_modificar.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        
        # Asignatura
        lbl_asignatura = ttk.Label(self.frame_form_modificar, text="Asignatura:")
        lbl_asignatura.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_asignatura_modificar = ttk.Entry(self.frame_form_modificar, width=30)
        self.entry_asignatura_modificar.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        # Validación en tiempo real
        vcmd_asignatura = (self.root.register(self.validar_asignatura_modificar), '%P')
        self.entry_asignatura_modificar.config(validate="key", validatecommand=vcmd_asignatura)
        self.lbl_error_asignatura_modificar = ttk.Label(self.frame_form_modificar, text="", foreground="red")
        self.lbl_error_asignatura_modificar.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        
        # Nota
        lbl_nota = ttk.Label(self.frame_form_modificar, text="Nota (0-50):")
        lbl_nota.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.entry_nota_modificar = ttk.Entry(self.frame_form_modificar, width=30)
        self.entry_nota_modificar.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        # Validación en tiempo real
        vcmd_nota = (self.root.register(self.validar_nota_modificar), '%P')
        self.entry_nota_modificar.config(validate="key", validatecommand=vcmd_nota)
        self.lbl_error_nota_modificar = ttk.Label(self.frame_form_modificar, text="", foreground="red")
        self.lbl_error_nota_modificar.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        
        # Botón para actualizar
        self.btn_actualizar = ttk.Button(self.frame_form_modificar, text="Actualizar", command=self.actualizar_estudiante)
        self.btn_actualizar.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Inicialmente deshabilitar el formulario
        self.habilitar_formulario_modificar(False)
    
    def validar_nombre_modificar(self, valor):
        """Valida el nombre en tiempo real para modificar."""
        if valor == "":
            self.lbl_error_nombre_modificar.config(text="")
            return True
        
        if Validador.validar_texto_alfabetico(valor):
            self.lbl_error_nombre_modificar.config(text="")
            return True
        else:
            self.lbl_error_nombre_modificar.config(text="Solo letras y espacios")
            return True
    
    def validar_apellido_modificar(self, valor):
        """Valida el apellido en tiempo real para modificar."""
        if valor == "":
            self.lbl_error_apellido_modificar.config(text="")
            return True
        
        if Validador.validar_texto_alfabetico(valor):
            self.lbl_error_apellido_modificar.config(text="")
            return True
        else:
            self.lbl_error_apellido_modificar.config(text="Solo letras y espacios")
            return True
    
    def validar_asignatura_modificar(self, valor):
        """Valida la asignatura en tiempo real para modificar."""
        if valor == "":
            self.lbl_error_asignatura_modificar.config(text="")
            return True
        
        if Validador.validar_alfanumerico(valor):
            self.lbl_error_asignatura_modificar.config(text="")
            return True
        else:
            self.lbl_error_asignatura_modificar.config(text="Caracteres no válidos")
            return True
    
    def validar_nota_modificar(self, valor):
        """Valida la nota en tiempo real para modificar."""
        if valor == "":
            self.lbl_error_nota_modificar.config(text="")
            return True
        
        es_valida, mensaje = Validador.validar_nota(valor)
        if es_valida:
            self.lbl_error_nota_modificar.config(text="")
        else:
            self.lbl_error_nota_modificar.config(text=mensaje)
        
        return True
    
    def habilitar_formulario_modificar(self, habilitar=True):
        """Habilita o deshabilita el formulario de modificación."""
        estado = "normal" if habilitar else "disabled"
        
        self.entry_nombre_modificar.config(state=estado)
        self.entry_apellido_modificar.config(state=estado)
        self.entry_asignatura_modificar.config(state=estado)
        self.entry_nota_modificar.config(state=estado)
        self.btn_actualizar.config(state=estado)
    
    def cargar_estudiante_modificar(self):
        """Carga los datos del estudiante para modificar."""
        id_estudiante = self.entry_id_modificar.get().strip()
        
        if not id_estudiante:
            messagebox.showwarning("Advertencia", "Ingrese un ID")
            return
        
        # Buscar estudiante
        estudiante = self.gestor.obtener_registro_por_id(id_estudiante)
        
        if not estudiante:
            messagebox.showinfo("Información", "No se encontró un estudiante con ese ID")
            self.habilitar_formulario_modificar(False)
            return
        
        # Cargar datos en el formulario
        self.entry_id_ro.config(state="normal")
        self.entry_id_ro.delete(0, tk.END)
        self.entry_id_ro.insert(0, estudiante["ID"])
        self.entry_id_ro.config(state="readonly")
        
        self.entry_nombre_modificar.delete(0, tk.END)
        self.entry_nombre_modificar.insert(0, estudiante["Nombre"])
        
        self.entry_apellido_modificar.delete(0, tk.END)
        self.entry_apellido_modificar.insert(0, estudiante["Apellido"])
        
        self.entry_asignatura_modificar.delete(0, tk.END)
        self.entry_asignatura_modificar.insert(0, estudiante["Asignatura"])
        
        self.entry_nota_modificar.delete(0, tk.END)
        self.entry_nota_modificar.insert(0, estudiante["Nota"])
        
        # Habilitar formulario
        self.habilitar_formulario_modificar(True)
    
    def actualizar_estudiante(self):
        """Actualiza los datos del estudiante."""
        id_estudiante = self.entry_id_ro.get()
        nombre = self.entry_nombre_modificar.get().strip()
        apellido = self.entry_apellido_modificar.get().strip()
        asignatura = self.entry_asignatura_modificar.get().strip()
        nota = self.entry_nota_modificar.get().strip()
        
        # Validar campos
        es_valido, mensaje = Validador.validar_campos_estudiante(nombre, apellido, asignatura, nota)
        
        if not es_valido:
            messagebox.showerror("Error de validación", mensaje)
            return
        
        # Confirmar actualización
        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de actualizar este registro?")
        if not confirmar:
            return
        
        # Actualizar estudiante
        datos = {
            "ID": id_estudiante,
            "Nombre": nombre,
            "Apellido": apellido,
            "Asignatura": asignatura,
            "Nota": nota
        }
        
        if self.gestor.actualizar_registro(id_estudiante, datos):
            messagebox.showinfo("Éxito", "Estudiante actualizado correctamente")
            
            # Limpiar campos y deshabilitar formulario
            self.entry_id_modificar.delete(0, tk.END)
            self.entry_id_ro.config(state="normal")
            self.entry_id_ro.delete(0, tk.END)
            self.entry_id_ro.config(state="readonly")
            self.entry_nombre_modificar.delete(0, tk.END)
            self.entry_apellido_modificar.delete(0, tk.END)
            self.entry_asignatura_modificar.delete(0, tk.END)
            self.entry_nota_modificar.delete(0, tk.END)
            
            self.habilitar_formulario_modificar(False)
        else:
            messagebox.showerror("Error", "No se pudo actualizar el estudiante")
    
    def configurar_tab_eliminar(self):
        # Pestaña de eliminar - Búsqueda y confirmación
        lbl_titulo = ttk.Label(self.tab_eliminar, text="Eliminar Estudiante", font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=10)
        
        # Frame de tipo de búsqueda
        frame_tipo = ttk.Frame(self.tab_eliminar)
        frame_tipo.pack(fill="x", padx=20, pady=10)
        
        # Opciones de búsqueda
        lbl_opcion = ttk.Label(frame_tipo, text="Eliminar por:")
        lbl_opcion.pack(side="left", padx=5)
        
        self.rb_var_eliminar = tk.StringVar(value="ID")
        rb_id = ttk.Radiobutton(frame_tipo, text="ID", variable=self.rb_var_eliminar, value="ID")
        rb_id.pack(side="left", padx=10)
        
        rb_nombre = ttk.Radiobutton(frame_tipo, text="Nombre", variable=self.rb_var_eliminar, value="Nombre")
        rb_nombre.pack(side="left", padx=10)
        
        # Frame de búsqueda
        frame_busqueda = ttk.Frame(self.tab_eliminar)
        frame_busqueda.pack(fill="x", padx=20, pady=10)
        
        # Campo de búsqueda
        lbl_termino = ttk.Label(frame_busqueda, text="Término de búsqueda:")
        lbl_termino.grid(row=0, column=0, padx=5, pady=5)
        
        self.entry_termino_eliminar = ttk.Entry(frame_busqueda, width=30)
        self.entry_termino_eliminar.grid(row=0, column=1, padx=5, pady=5)
        
        # Botón de búsqueda
        btn_buscar = ttk.Button(frame_busqueda, text="Buscar", command=self.buscar_para_eliminar)
        btn_buscar.grid(row=0, column=2, padx=5, pady=5)
        
        # Resultados
        frame_resultados = ttk.LabelFrame(self.tab_eliminar, text="Resultados")
        frame_resultados.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Tabla de resultados
        self.treeview_eliminar = ttk.Treeview(
            frame_resultados, 
            columns=("ID", "Nombre", "Apellido", "Asignatura", "Nota"), 
            show="headings"
        )
        
        # Definir encabezados
        self.treeview_eliminar.heading("ID", text="ID")
        self.treeview_eliminar.heading("Nombre", text="Nombre")
        self.treeview_eliminar.heading("Apellido", text="Apellido")
        self.treeview_eliminar.heading("Asignatura", text="Asignatura")
        self.treeview_eliminar.heading("Nota", text="Nota")
        
        # Definir anchos de columna
        self.treeview_eliminar.column("ID", width=50)
        self.treeview_eliminar.column("Nombre", width=150)
        self.treeview_eliminar.column("Apellido", width=150)
        self.treeview_eliminar.column("Asignatura", width=150)
        self.treeview_eliminar.column("Nota", width=50)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_resultados, orient="vertical", command=self.treeview_eliminar.yview)
        self.treeview_eliminar.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar elementos
        self.treeview_eliminar.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón para eliminar
        btn_eliminar = ttk.Button(self.tab_eliminar, text="Eliminar seleccionado", command=self.eliminar_estudiante)
        btn_eliminar.pack(pady=10)
    
    def buscar_para_eliminar(self):
        """Busca estudiantes para eliminar."""
        criterio = self.rb_var_eliminar.get()
        termino = self.entry_termino_eliminar.get().strip()
        
        if not termino:
            messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda")
            return
        
        # Limpiar tabla de resultados
        for item in self.treeview_eliminar.get_children():
            self.treeview_eliminar.delete(item)
        
        # Realizar búsqueda
        resultados = self.gestor.buscar_registros(criterio, termino)
        
        if not resultados:
            messagebox.showinfo("Información", "No se encontraron resultados")
            return
        
        # Mostrar resultados
        for registro in resultados:
            self.treeview_eliminar.insert("", "end", values=(
                registro["ID"],
                registro["Nombre"],
                registro["Apellido"],
                registro["Asignatura"],
                registro["Nota"]
            ))
    
    def eliminar_estudiante(self):
        """Elimina el estudiante seleccionado."""
        # Verificar si hay un elemento seleccionado
        seleccion = self.treeview_eliminar.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un estudiante para eliminar")
            return
        
        # Obtener ID del estudiante seleccionado
        valores = self.treeview_eliminar.item(seleccion[0], "values")
        id_estudiante = valores[0]
        
        # Confirmar eliminación
        confirmar = messagebox.askyesno(
            "Confirmar eliminación", 
            f"¿Está seguro de eliminar el estudiante {valores[1]} {valores[2]}?"
        )
        
        if not confirmar:
            return
        
        # Eliminar estudiante
        if self.gestor.eliminar_registro(id_estudiante):
            messagebox.showinfo("Éxito", "Estudiante eliminado correctamente")
            
            # Actualizar tabla
            self.treeview_eliminar.delete(seleccion[0])
        else:
            messagebox.showerror("Error", "No se pudo eliminar el estudiante")
    
    def configurar_tab_exportar(self):
        # Pestaña para exportar registros eliminados
        lbl_titulo = ttk.Label(self.tab_exportar, text="Exportar Registros Eliminados", font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=10)
        
        # Información sobre registros eliminados
        frame_info = ttk.LabelFrame(self.tab_exportar, text="Registros Eliminados")
        frame_info.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Tabla de registros eliminados
        self.treeview_eliminados = ttk.Treeview(
            frame_info, 
            columns=("ID", "Nombre", "Apellido", "Asignatura", "Nota"), 
            show="headings"
        )
        
        # Definir encabezados
        self.treeview_eliminados.heading("ID", text="ID")
        self.treeview_eliminados.heading("Nombre", text="Nombre")
        self.treeview_eliminados.heading("Apellido", text="Apellido")
        self.treeview_eliminados.heading("Asignatura", text="Asignatura")
        self.treeview_eliminados.heading("Nota", text="Nota")
        
        # Definir anchos de columna
        self.treeview_eliminados.column("ID", width=50)
        self.treeview_eliminados.column("Nombre", width=150)
        self.treeview_eliminados.column("Apellido", width=150)
        self.treeview_eliminados.column("Asignatura", width=150)
        self.treeview_eliminados.column("Nota", width=50)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_info, orient="vertical", command=self.treeview_eliminados.yview)
        self.treeview_eliminados.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar elementos
        self.treeview_eliminados.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame para opciones de exportación
        frame_export = ttk.Frame(self.tab_exportar)
        frame_export.pack(fill="x", padx=20, pady=10)
        
        # Ruta del archivo
        lbl_ruta = ttk.Label(frame_export, text="Ruta de guardado:")
        lbl_ruta.grid(row=0, column=0, padx=5, pady=5)
        
        self.entry_ruta = ttk.Entry(frame_export, width=50)
        self.entry_ruta.grid(row=0, column=1, padx=5, pady=5)
        
        # Botón para seleccionar ruta
        btn_seleccionar = ttk.Button(frame_export, text="Examinar...", command=self.seleccionar_ruta)
        btn_seleccionar.grid(row=0, column=2, padx=5, pady=5)
        
        # Botón para exportar
        btn_exportar = ttk.Button(frame_export, text="Exportar a CSV", command=self.exportar_eliminados)
        btn_exportar.grid(row=1, column=1, pady=10)
        
        # Cargar registros eliminados
        self.listar_registros_eliminados()
    
    def listar_registros_eliminados(self):
        """Muestra todos los registros eliminados en la tabla."""
        # Limpiar tabla
        for item in self.treeview_eliminados.get_children():
            self.treeview_eliminados.delete(item)
        
        # Obtener registros
        registros = self.gestor.obtener_registros_eliminados()
        
        # Insertar registros en la tabla
        for registro in registros:
            self.treeview_eliminados.insert("", "end", values=(
                registro["ID"],
                registro["Nombre"],
                registro["Apellido"],
                registro["Asignatura"],
                registro["Nota"]
            ))
    
    def seleccionar_ruta(self):
        """Selecciona la ruta para guardar el archivo CSV."""
        ruta = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if ruta:
            self.entry_ruta.delete(0, tk.END)
            self.entry_ruta.insert(0, ruta)
    
    def exportar_eliminados(self):
        """Exporta los registros eliminados a un archivo CSV."""
        ruta = self.entry_ruta.get().strip()
        
        if not ruta:
            messagebox.showwarning("Advertencia", "Seleccione una ruta para guardar el archivo")
            return
        
        # Exportar registros
        if self.gestor.exportar_eliminados(ruta):
            messagebox.showinfo("Éxito", f"Registros exportados correctamente a:\n{ruta}")
        else:
            messagebox.showerror("Error", "No se pudieron exportar los registros")