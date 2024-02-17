import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Label, BOTH, Tk
from PDFViewerApp import PDFViewerApp
from JacobiDisplayApp import JacobiDisplayApp


class Aplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.main_interface()  
# ----------------------------------------------------------------------
    # CREACION DE LA INTERFAZ GRAFICA
    def main_interface(self):
        self.master.title("Proyecto de Métodos Numéricos")
        self.master.iconbitmap("./images/icon.ico")
        self.master.resizable(0, 0)
        self.master.geometry("680x420")

        # DICCIONARIO ESTILIZADOR PARA LOS ELEMENTOS GRAFICOS
        self.labels_style = {"font": ("Arial", 13, "bold"),
                             "fg": "yellow",
                             "bg": "gray",
                             "pady": 7,
                             "padx": 5,
                             "borderwidth": 1,
                             "relief": "solid"}
        self.buttons_style = {"font": ("Arial", 11, "bold"),
                              "fg": "white",
                              "bg": "blue",
                              "pady": 1,
                              "borderwidth": 2,
                              "relief": "solid"}
        self.efect_btn_style = {"font": ("Arial", 11, "bold"),
                                "fg": "black",
                                "bg": "lightblue",
                                "pady": 1,
                                "borderwidth": 2,
                                "relief": "solid"}

        # IMAGEN DE FONDO 
        self.image = Image.open("./images/background.jpg")
        self.image = self.image.resize((680, 420))
        self._backgroud_image = ImageTk.PhotoImage(self.image)

        # FONDO PRINCIPAL SOBRE ETIQUETA
        # RELWIDTH Y RELHEIGHT SON POSICIONES RELATIVAS DEL ANCHO Y ALTO
        self.background = Label(image=self._backgroud_image)
        self.background.place(x=0, y=0, relwidth=1, relheight=1)

        # ETIQUETAS
        # ANCHOR ES LA MANERA EN QUE QUIERO ACOMODAR EL ELEMENTO
        # EL "**" DESEMPAQUETA EL DICCIONARIO
        # ES DECIR, LO CONVIERTE EN PARAMETROS SEPARADOS POR COMA
        # ESTOS SON LEIDOS Y APLICADOS AL ELEMENTO DESEADO
        self.home_label = Label(self.master,
                                text="Bienvenido(a) al programa de cálculo de ecuaciones lineales mediante el método de Jacobi",
                                **self.labels_style)
        self.home_label.config(font=("Calibri", 12, "bold"))
        self.home_label.place(relx=0.5, rely=0.2, anchor="center")

        # BOTONES
        self.manual_btn = tk.Button(self.master,
                                    text="1. Ver Historia del Método.",
                                    command=lambda: self.history_view(),
                                    **self.buttons_style)
        self.manual_btn.place(x=5, rely=0.4, anchor="w")
        self.manual_btn.bind("<Enter>",lambda event: self.in_cursor_btn(event, 1))
        self.manual_btn.bind("<Leave>",lambda event: self.out_cursor_btn(event, 1))
        
        self.calc_btn = tk.Button(self.master, text="2. Calcular sistema de ecuaciones.",
                            command=lambda: self.jacobi_solver(),
                                    **self.buttons_style)
        self.calc_btn.place(x=5, rely=0.5, anchor="w")
        self.calc_btn.bind("<Enter>",
                             lambda event: self.in_cursor_btn(event, 1))
        self.calc_btn.bind("<Leave>",
                             lambda event: self.out_cursor_btn(event, 1))

        self.exit_btn = tk.Button(self.master, text="Salir",
                                    command=lambda: self.master.destroy(),
                                    **self.buttons_style)
        self.exit_btn.config(bg="red")
        self.exit_btn.place(relx=0.5, rely=0.8, anchor="center")
        self.exit_btn.bind("<Enter>",
                             lambda event: self.in_cursor_btn(event, 0))
        self.exit_btn.bind("<Leave>",
                             lambda event: self.out_cursor_btn(event, 0))
# ----------------------------------------------------------------------
    def in_cursor_btn(self, event, tipo):
        if tipo == 0:
            event.widget.config(**self.efect_btn_style)
        else:
            event.widget.config(**self.efect_btn_style)
# ----------------------------------------------------------------------     
    def out_cursor_btn(self, event, tipo):
        if tipo == 0:
            event.widget.config(**self.buttons_style)
            event.widget.config(bg="red")
        else:
            event.widget.config(**self.buttons_style)
# ----------------------------------------------------------------------
    def reopen(self):
        root = Tk()
        app = Aplication(master=root)
        app.mainloop()
# ----------------------------------------------------------------------    
    def history_view(self):
        self.master.title("Historia del Método de Jacobi")
        self.clear_widgets()

        # CREANDO EL VISOR DE PDF
        pdf_viewer = PDFViewerApp(self.master, "PROYECTO METODOS NUMERICOS.pdf", app)
        pdf_viewer.canvas.pack(fill=BOTH, expand=True)
# ----------------------------------------------------------------------
    def jacobi_solver(self):
        self.master.title("Calculadora de Ecuaciones Lineales por el Método de Jacobi")
        self.clear_widgets()
        jacobi_viewer = JacobiDisplayApp(self.master, self)
        self.master.attributes('-fullscreen', True)
        self.master.geometry("1200x600")
        self.master.bind("<Escape>", lambda event: self.master.attributes("-fullscreen", not self.master.attributes("-fullscreen")))
        jacobi_viewer.pack(fill=BOTH, expand=True)
# ----------------------------------------------------------------------
    def clear_widgets(self):
        # ELIMINA TODOS LOS WIDGETS DE LA VENTANA PRINCIPAL
        for widget in self.master.winfo_children():
            widget.destroy() 
# ---------------------------------------------------------------------- 
root = Tk()
# SE CREA UNA INTERFAZ TEMPORAL PARA MANTENER EL APP ABIERTA
app = Aplication(master=root)
app.mainloop()
