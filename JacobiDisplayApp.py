import tkinter as tk
from tkinter import ttk
from MetodoJacobi import JacobiMethod

class JacobiDisplayApp():
    def __init__(self, master, app_instance):
        self.master = master
        self.app_instance = app_instance
        self.master.resizable(True, True)
        self.master.geometry("880x720")
        self.interface()

    def interface(self):
        # ESTILOS
        self.master.configure(bg="#CECECF")
        self.entry_bg = "#ffffff"  
        self.entry_fg = "#000000"  
        self.entry_font = ("Arial", 10)  
        

        # LABEL ETIQUETAS
        self.label_frame = tk.LabelFrame(self.master)
        self.label_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.button_frame = tk.Frame(self.label_frame)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        self.equation_one = tk.Entry(self.button_frame, font=self.entry_font, bg=self.entry_bg, fg=self.entry_fg, width=25)
        self.equation_one.pack(side=tk.LEFT, padx=50, pady=8)
        self.label_equation_one = tk.Label(self.label_frame, text="Ecuación 1")
        self.label_equation_one.pack(side=tk.LEFT, padx=80, fill=tk.X)

        self.equation_two = tk.Entry(self.button_frame, font=self.entry_font, bg=self.entry_bg, fg=self.entry_fg, width=25)
        self.equation_two.pack(side=tk.RIGHT, padx=50, pady=8)
        self.label_equation_three = tk.Label(self.label_frame, text="Ecuación 3")
        self.label_equation_three.pack(side=tk.RIGHT, padx=80, fill=tk.X)

        self.equation_three = tk.Entry(self.button_frame, font=self.entry_font, bg=self.entry_bg, fg=self.entry_fg, width=25)
        self.equation_three.pack(side=tk.BOTTOM, padx=80, pady=8)
        self.label_equation_two = tk.Label(self.label_frame, text="Ecuación 2")
        self.label_equation_two.pack(side=tk.BOTTOM, padx=70, fill=tk.X)

        self.combobox_label_frame = tk.LabelFrame(self.master)
        self.combobox_label_frame.pack(fill=tk.BOTH)

        self.entry_error = tk.Entry(self.combobox_label_frame, font=self.entry_font, bg=self.entry_bg, fg=self.entry_fg)
        self.entry_error.pack(side=tk.RIGHT, padx=20)
        self.label_iterations = tk.Label(self.combobox_label_frame, text="Seleccione la cantidad de iteraciones:")
        self.label_iterations.pack(side=tk.LEFT, fill=tk.X, padx=30)
        
        self.combobox_iterations = ttk.Combobox(self.combobox_label_frame, values=[i for i in range(1, 1001)])
        self.combobox_iterations.pack(side=tk.LEFT, padx=30)
        self.label_errors = tk.Label(self.combobox_label_frame, text="Ingrese el error deseado:")
        self.label_errors.pack(side=tk.RIGHT, fill=tk.X, padx=35)
        
        self.solve_button = tk.Button(self.master, text="Resolver", command= lambda: self.solver(), font=("Arial", 12, "bold"), bg="#1D3987", fg="white")
        self.solve_button.pack(side=tk.BOTTOM, fill=tk.X, padx=25, pady=8)
        self.solver_frame = tk.Frame()
        self.solver_frame.pack(fill=tk.BOTH, padx=25, pady=25)
        
        self.text_widget = tk.Text(self.solver_frame, 
                                   wrap=tk.WORD, 
                                   width=40, 
                                   height=80, 
                                   bg="#265A23",
                                   fg="#FFF",
                                   padx=8,
                                   pady=8
                                   )
        self.text_widget.pack(fill=tk.BOTH, expand=True)  # Expand to fill the frame
        self.text_widget.config(wrap=tk.WORD)
    def solver(self):
        self.text_widget.delete('1.0', tk.END)
        valueError = ""
        jacobi_solve = JacobiMethod()

        # Create the Text widget within the solver method

        # Example usage: Insert some text into the widget
        #self.text_widget.insert(tk.END, jacobi_solve.ejecucion("10x+y+2z=3","4x+6y-z=9","-2x+3y+8z=51",0.06,0))    
 
        
        if(self.entry_error.get() == ""):
            print("Hi1")
            valueError = "0"
        else:
            print("hi2")
            valueError = self.entry_error.get()

        self.text_widget.insert(tk.END, jacobi_solve.ejecucion(
            self.equation_one.get(),
            self.equation_two.get(),
            self.equation_three.get(),
            float(valueError),
            int(self.combobox_iterations.get()))
        )