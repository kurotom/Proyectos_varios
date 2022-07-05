from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from pyPillow import CompressIMG


def fileSelects():
    askfile = filedialog.askopenfilenames()
    if len(askfile) > 0:
        c = CompressIMG(file=askfile)
        c.convert()
        #
        messagebox.showinfo(title='', message='Listo')




class App(Tk):
    def __init__(self):
        super().__init__()

        self.geometry('350x200')
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.title('Images Tools')

        #   main frame
        frame1 = ttk.Frame(self, padding='10 10 10 10')
        frame1.grid(column=0, row=0, columnspan=5, rowspan=6)
        ####
        
        label = ttk.Label(frame1)
        label['text'] = 'Seleccione imágenes'
        label.grid()

        buttonFile = ttk.Button(frame1, width=10, text='Open', command=fileSelects)
        buttonFile.grid()


        quit = ttk.Button(frame1, width=10, text='Salir', command=self.quit)
        quit.grid(pady=(50,0))

    def quit(self):
        self.destroy()





if __name__ == '__main__':
    app = App()
    app.mainloop()
