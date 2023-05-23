import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image

from pdf2image import convert_from_path

from threading import Thread
import os
from datetime import datetime


class Gui(ttk.Frame):

    def __init__(self, contenedor):
        super().__init__(contenedor)

        self.ASSETS_PATH = "assets/"
        self.DIR_ROOT = "convertidos"

        self.FORMATOS_SELECCION = ["Seleccione", "PNG", "JPEG", "JPG"]
        self.color = '#85D7E9'
        self.fuente = "Utopia 14 bold"

        self.filesPDF = None
        self.nombre = ""

        estiloFrame = ttk.Style()
        estiloFrame.configure("estilo_frame.TFrame", background=self.color)

        self.frame = ttk.Frame(self, style="estilo_frame.TFrame")

        self.canvas = tk.Canvas(self, background="white", highlightthickness=0)
        self.imagen = Image.open(rf'{self.ASSETS_PATH}pdf_to_image.png')
        self.loadImagen = ImageTk.PhotoImage(self.imagen)

        self.canvas.create_image(0, 0, image=self.loadImagen, anchor='nw')

        self.botonImagen = Image.open(self.ASSETS_PATH + "boton.png")
        self.botonImagenCargada = ImageTk.PhotoImage(self.botonImagen)

        self.abrir = tk.Button(
                            self.frame,
                            command=self.abrir_fichero,
                            image=self.botonImagenCargada,
                            bg=self.color,
                            activebackground=self.color,
                            highlightthickness=0,
                            borderwidth=0,
                            overrelief=None,
                            bd=-2,
                            cursor="hand2"
                        )

        self.labelFormato = tk.Label(
                                    self.frame,
                                    text="Formato imagen",
                                    bg=self.color,
                                    font=self.fuente,
                                )
        estiloCombobox = ttk.Style()
        estiloCombobox.configure(
            'comboboxStyle.TCombobox',
            selectbackground="transparent",
            selectforeground="black",
            padding=(10, 0, 10, 0)
        )
        self.dropmenu = ttk.Combobox(
                            self.frame,
                            state="readonly",
                            values=self.FORMATOS_SELECCION,
                            font=self.fuente,
                            style="comboboxStyle.TCombobox"
                        )
        self.dropmenu.current(0)

        self.convertir = tk.Button(
                                self.frame,
                                command=self.convertir,
                                font=self.fuente,
                                text="Convertir"
                            )

        self.place(relwidth=1, relheight=1)
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1/2)

        self.abrir.place(x=30, y=140)

        self.labelFormato.place(x=220, y=160, width=150, height=30)
        self.dropmenu.place(x=220, y=190, width=150, height=30)

        self.convertir.place(x=130, y=240, width=150, height=30)

    def convertir(self):
        if self.filesPDF is None:
            tk.messagebox.showinfo(
                    title="No ha seleccionado PDF",
                    message="Debe seleccionar al menos 1 PDF."
                )
        elif self.dropmenu.current() <= 0:
            tk.messagebox.showinfo(
                    title="Seleccione formato",
                    message="Debe seleccionar el formato del la imagen."
                )
        elif self.dropmenu.current() > 0 and self.filesPDF is not None:
            hilo = Thread(target=self.worker)
            hilo.start()

    def worker(self):
        self.convertir.config(state='disabled')
        self.convertir['text'] = 'Convirtiendo'

        if not os.path.exists(self.DIR_ROOT):
            os.mkdir(self.DIR_ROOT)

        formato = self.FORMATOS_SELECCION[self.dropmenu.current()].lower()

        for i in self.filesPDF:
            lista_ruta = i.name.split("/")[-1]
            filenombre = lista_ruta.replace(".pdf", "")
            directorio = f'{self.DIR_ROOT}/{filenombre}-imagenes'

            if not os.path.exists(directorio):
                os.mkdir(directorio)

            imagenes = convert_from_path(
                                i.name,
                                dpi=300,
                                fmt=f'{formato.lower()}'
                            )
            [
                imagenes[i].save(f'{directorio}/{filenombre}-{i}.{formato}')
                for i in range(len(imagenes))
            ]
        self.dropmenu.current(0)
        self.filesPDF = None
        self.convertir.config(state='normal')
        self.convertir['text'] = 'Convertir'
        tk.messagebox.showinfo(
                title="Finalizó",
                message=f"Guardados dentro de la carpeta '{self.DIR_ROOT}'"
            )

    def abrir_fichero(self):
        files = filedialog.askopenfiles(
                            filetypes=[("Archivos PDF", "*.pdf")],
                            title="Seleccione PDF"
                        )

        self.filesPDF = files


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('PDF a Imagen')
        self.geometry('400x300')
        self.resizable(width=False, height=False)


if __name__ == '__main__':
    app = App()
    gui = Gui(app)
    app.mainloop()
