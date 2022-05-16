from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import PyPDF2
import os

# Packages
# PyPDF2


def proceso():
    name_file = entry.get()
    if str(name_file) != "":
        filesPDF = filedialog.askopenfiles(filetypes=[("Pdf files", "*.pdf")], title="Seleccione dos o más PDF.")
        if len(filesPDF) != 0:
            pdfmerger = PyPDF2.PdfFileMerger()
            for i in range(len(filesPDF)):
                pdfmerger.append(filesPDF[i].name)
            if ".pdf" not in str(name_file).lower():
                pdfmerger.write(f"{name_file}.pdf")
            else:
                pdfmerger.write(name_file)
            pdfmerger.close()
            messagebox.showinfo(message="Listo!")
    else:
        messagebox.showinfo(message="Ingrese un nombre para el archivo final.")


def about():
    bs = Tk()
    bs.title("")
    label = Label(bs, text="Github - kurotom")
    bs.grid()
    label.grid()
    bs.mainloop()


def salir():
    base.quit()



instruccion = """
* Se ordenarán alfabeticamente
los PDF seleccionados.

* Se agregarán al
final del primer PDF.
"""


base = Tk()
base.title("Merge PDF")

frame = Frame(base)

nameLable = Label(frame, text="Nombre del PDF Generado")
entry = Entry(frame, text="Nombre", justify="center", width=30)
boton1 = Button(frame, text="Abrir PDFs", command=proceso)

salir = Button(frame, text="Salir", command=salir)
aboutBoton = Button(frame, text="!", command=about)

label = Label(frame, text=instruccion)

frame.pack(pady=30)
nameLable.grid(column=1)
entry.grid(column=1)
boton1.grid(column=1)
label.grid(column=1)
salir.grid(row=4, column=0)
aboutBoton.grid(row=4, column=2)
base.geometry("400x320")
base.update()
base.resizable(width=0, height=0)
base.mainloop()
