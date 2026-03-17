import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class AplicacionOCR:
    def __init__(self, root):
        self.root = root
        self.root.title("Actividad OCR")
        self.root.geometry("1180x760")
        self.root.configure(bg="#0f172a")
        self.root.resizable(False, False)

        self.ruta_imagen = None
        self.imagen_original = None
        self.imagen_gris = None
        self.imagen_preprocesada = None

        self.color_fondo = "#0f172a"
        self.color_panel = "#111827"
        self.color_panel_sec = "#1f2937"
        self.color_boton = "#2563eb"
        self.color_boton_hover = "#1d4ed8"
        self.color_texto = "#f8fafc"
        self.color_subtexto = "#cbd5e1"
        self.color_caja = "#e5e7eb"

        self.crear_interfaz()

    def crear_interfaz(self):
        encabezado = tk.Frame(self.root, bg=self.color_fondo, height=90)
        encabezado.pack(fill="x", pady=(12, 0))

        titulo = tk.Label(
            encabezado,
            text="Sistema OCR con Python",
            font=("Segoe UI", 24, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        )
        titulo.pack()

        subtitulo = tk.Label(
            encabezado,
            text="Carga de imágenes, preprocesamiento y extracción de texto con PyTesseract",
            font=("Segoe UI", 10),
            bg=self.color_fondo,
            fg=self.color_subtexto
        )
        subtitulo.pack(pady=(4, 0))

        barra_botones = tk.Frame(self.root, bg=self.color_fondo)
        barra_botones.pack(pady=18)

        self.crear_boton(barra_botones, "Cargar imagen", self.cargar_imagen, 0)
        self.crear_boton(barra_botones, "Mostrar original", self.mostrar_original, 1)
        self.crear_boton(barra_botones, "Convertir a grises", self.mostrar_grises, 2)
        self.crear_boton(barra_botones, "Preprocesar imagen", self.mostrar_preprocesada, 3)
        self.crear_boton(barra_botones, "Extraer texto", self.extraer_texto, 4)
        self.crear_boton(barra_botones, "Salir", self.salir, 5, color="#dc2626", hover="#b91c1c")

        contenedor = tk.Frame(self.root, bg=self.color_fondo)
        contenedor.pack(fill="both", expand=True, padx=20, pady=10)

        panel_imagenes = tk.Frame(contenedor, bg=self.color_fondo)
        panel_imagenes.pack(fill="x")

        self.panel_original = self.crear_panel_imagen(panel_imagenes, "Imagen original", 0)
        self.panel_procesada = self.crear_panel_imagen(panel_imagenes, "Imagen procesada", 1)

        panel_texto = tk.Frame(
            contenedor,
            bg=self.color_panel,
            bd=0,
            highlightthickness=1,
            highlightbackground="#334155"
        )
        panel_texto.pack(fill="both", expand=True, pady=(18, 0))

        titulo_texto = tk.Label(
            panel_texto,
            text="Texto detectado",
            font=("Segoe UI", 13, "bold"),
            bg=self.color_panel,
            fg=self.color_texto
        )
        titulo_texto.pack(anchor="w", padx=16, pady=(14, 6))

        self.label_ruta = tk.Label(
            panel_texto,
            text="No se ha cargado ninguna imagen.",
            font=("Segoe UI", 9),
            bg=self.color_panel,
            fg=self.color_subtexto,
            anchor="w",
            justify="left"
        )
        self.label_ruta.pack(fill="x", padx=16, pady=(0, 8))

        frame_text = tk.Frame(panel_texto, bg=self.color_panel)
        frame_text.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        scrollbar = tk.Scrollbar(frame_text)
        scrollbar.pack(side="right", fill="y")

        self.texto_resultado = tk.Text(
            frame_text,
            height=12,
            font=("Consolas", 11),
            bg="#020617",
            fg="#e2e8f0",
            insertbackground="white",
            relief="flat",
            wrap="word",
            yscrollcommand=scrollbar.set,
            padx=12,
            pady=12
        )
        self.texto_resultado.pack(fill="both", expand=True)
        scrollbar.config(command=self.texto_resultado.yview)

    def crear_boton(self, parent, texto, comando, columna, color=None, hover=None):
        color = color or self.color_boton
        hover = hover or self.color_boton_hover

        boton = tk.Label(
            parent,
            text=texto,
            font=("Segoe UI", 10, "bold"),
            bg=color,
            fg="white",
            width=18,
            height=2,
            cursor="hand2",
            relief="flat"
        )
        boton.grid(row=0, column=columna, padx=7)

        boton.bind("<Button-1>", lambda e: comando())
        boton.bind("<Enter>", lambda e: boton.config(bg=hover))
        boton.bind("<Leave>", lambda e: boton.config(bg=color))

    def crear_panel_imagen(self, parent, titulo, columna):
        panel = tk.Frame(
            parent,
            bg=self.color_panel,
            width=550,
            height=300,
            highlightthickness=1,
            highlightbackground="#334155"
        )
        panel.grid(row=0, column=columna, padx=10)
        panel.grid_propagate(False)

        label_titulo = tk.Label(
            panel,
            text=titulo,
            font=("Segoe UI", 13, "bold"),
            bg=self.color_panel,
            fg=self.color_texto
        )
        label_titulo.pack(pady=(12, 8))

        area = tk.Frame(
            panel,
            bg=self.color_panel_sec,
            width=500,
            height=230,
            highlightthickness=1,
            highlightbackground="#475569"
        )
        area.pack(pady=(0, 12))
        area.pack_propagate(False)

        label_imagen = tk.Label(
            area,
            bg=self.color_panel_sec
        )
        label_imagen.place(relx=0.5, rely=0.5, anchor="center")

        return label_imagen

    def cargar_imagen(self):
        ruta = filedialog.askopenfilename(
            title="Seleccione una imagen",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not ruta:
            return

        img = cv2.imread(ruta)
        if img is None:
            messagebox.showerror("Error", "No se pudo cargar la imagen.")
            return

        self.ruta_imagen = ruta
        self.imagen_original = img
        self.imagen_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, self.imagen_preprocesada = cv2.threshold(self.imagen_gris, 150, 255, cv2.THRESH_BINARY)

        self.mostrar_en_label(self.imagen_original, self.panel_original)
        self.panel_procesada.config(image="")
        self.panel_procesada.image = None

        self.label_ruta.config(text=f"Imagen cargada: {self.ruta_imagen}")
        self.texto_resultado.delete("1.0", tk.END)
        self.texto_resultado.insert(tk.END, "La imagen se cargó correctamente.\nPuede aplicar el procesamiento o extraer el texto.")

    def mostrar_en_label(self, img_cv, label):
        if img_cv is None:
            return

        if len(img_cv.shape) == 2:
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_GRAY2RGB)
        else:
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

        img_pil = Image.fromarray(img_rgb)
        img_pil.thumbnail((480, 210))

        img_tk = ImageTk.PhotoImage(img_pil)
        label.config(image=img_tk)
        label.image = img_tk

    def mostrar_original(self):
        if self.imagen_original is None:
            messagebox.showwarning("Aviso", "Primero debe cargar una imagen.")
            return
        self.mostrar_en_label(self.imagen_original, self.panel_original)

    def mostrar_grises(self):
        if self.imagen_gris is None:
            messagebox.showwarning("Aviso", "Primero debe cargar una imagen.")
            return
        self.mostrar_en_label(self.imagen_gris, self.panel_procesada)
        self.texto_resultado.delete("1.0", tk.END)
        self.texto_resultado.insert(tk.END, "La imagen fue convertida a escala de grises.")

    def mostrar_preprocesada(self):
        if self.imagen_preprocesada is None:
            messagebox.showwarning("Aviso", "Primero debe cargar una imagen.")
            return
        self.mostrar_en_label(self.imagen_preprocesada, self.panel_procesada)
        self.texto_resultado.delete("1.0", tk.END)
        self.texto_resultado.insert(tk.END, "Se aplicó umbralización para mejorar la lectura del OCR.")

    def extraer_texto(self):
        if self.imagen_preprocesada is None:
            messagebox.showwarning("Aviso", "Primero debe cargar una imagen.")
            return

        texto = pytesseract.image_to_string(self.imagen_preprocesada, lang="eng").strip()

        self.mostrar_en_label(self.imagen_preprocesada, self.panel_procesada)
        self.texto_resultado.delete("1.0", tk.END)

        if texto:
            self.texto_resultado.insert(tk.END, texto)
        else:
            self.texto_resultado.insert(tk.END, "No se detectó texto en la imagen.")

    def salir(self):
        cv2.destroyAllWindows()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionOCR(root)
    root.mainloop()