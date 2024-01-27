import tkinter as tk
from tkinter import Label, Tk
from PIL import Image, ImageTk


class Aplication(tk.Frame):
    # ----------------------------------------------------------------------
    def __init__(self, principal_frame=None):
        super().__init__(principal_frame)
        self.principal_frame = principal_frame
        self.pack()
        self.mainInterface()
    
    def mainInterface(self):
        self.principal_frame.title("Proyecto Métodos Numéricos")
        self.principal_frame.resizable(0, 0)
        self.principal_frame.geometry("680x420")

        # DICCIONARIO ESTILIZADOR PARA LOS ELEMENTOS GRAFICOS
        self.labels_style = {"font": ("Arial", 13, "bold"),
                             "fg": "yellow",
                             "bg": "gray",
                             "pady": 7,
                             "padx": 5,
                             "borderwidth": 1,
                             "relief": "solid"}
        self.buttons_style = {"font": ("Arial", 12, "bold"),
                              "fg": "white",
                              "bg": "blue",
                              "pady": 1,
                              "borderwidth": 2,
                              "relief": "solid"}
        self.efect_btn_style = {"font": ("Arial", 12, "bold"),
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
        
        self.background = Label( image=self._backgroud_image)
        self.background.place(x=0, y=0, relwidth=1, relheight=1)

        # ETIQUETAS
        # ANCHOR ES LA MANERA EN QUE QUIERO ACOMODAR EL ELEMENTO
        # EL "**" DESEMPAQUETA EL DICCIONARIO
        # ES DECIR, LO CONVIERTE EN PARAMETROS SEPARADOS POR COMA
        # ESTOS SON LEIDOS Y APLICADOS AL ELEMENTO DESEADO
        self.home_label = Label(self.principal_frame,
                                text="Bienvenido(a) al programa de cálculo de ecuaciones mediante el método de Jacobi, por favor seleccione la opción que desee:",
                                **self.labels_style)
        self.home_label.place(relx=0.5, rely=0.2, anchor="center")

        # BOTONES
        self.manual_btn = tk.Button(self.principal_frame,
                                    text="1. Ver manual de uso.",
                                    command=lambda: one(self),
                                    **self.buttons_style)
        self.manual_btn.place(x=5, rely=0.4, anchor="w")
        self.manual_btn.bind("<Enter>",lambda event: self.in_cursor_btn(event, 1))
        self.manual_btn.bind("<Leave>",lambda event: self.out_cursor_btn(event, 1))
        
        self.calc_btn = tk.Button(self.principal_frame, text="2. Calcular sistema de ecuaciones.",
                            command=lambda: two(self),
                                    **self.buttons_style)
        self.calc_btn.place(x=5, rely=0.5, anchor="w")
        self.calc_btn.bind("<Enter>",
                             lambda event: self.in_cursor_btn(event, 1))
        self.calc_btn.bind("<Leave>",
                             lambda event: self.out_cursor_btn(event, 1))



        self.exit_btn = tk.Button(self.principal_frame, text="Salir",
                                    command=lambda: self.principal_frame.destroy(),
                                    **self.buttons_style)
        self.exit_btn.config(bg="red")
        self.exit_btn.place(relx=0.5, rely=0.8, anchor="center")
        self.exit_btn.bind("<Enter>",
                             lambda event: self.in_cursor_btn(event, 0))
        self.exit_btn.bind("<Leave>",
                             lambda event: self.out_cursor_btn(event, 0))

# ----------------------------------------------------------------------

    # FUNCIONES DE ESTILIZADO
    def in_cursor_btn(self, event, tipo):
        if tipo == 0:
            event.widget.config(**self.efect_btn_style)
        else:
            event.widget.config(**self.efect_btn_style)
            
    def out_cursor_btn(self, event, tipo):
        if tipo == 0:
            event.widget.config(**self.buttons_style)
            event.widget.config(bg="red")
        else:
            event.widget.config(**self.buttons_style)

# ----------------------------------------------------------------------

    def reopen(self):
        self.principal_frame.destroy()
        root = Tk()
        app = Aplication(principal_frame=root)
        app.mainloop()

# ----------------------------------------------------------------------

            
root = Tk()
# SE CREA UNA INTERFAZ TEMPORAL PARA MANTENER LA APP ABIERTA
app = Aplication(principal_frame=root)
app.mainloop()
