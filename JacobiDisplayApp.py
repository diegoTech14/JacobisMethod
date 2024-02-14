import tkinter as tk
from tkinter import ttk


class JacobiDisplayApp:
    def __init__(self, master, app_instance):
        self.master = master
        self.app_instance = app_instance
        self.interface()

    def interface(self):
        # ESTILOS
        self.master.configure(bg="#f0f0f0")
        self.entry_bg = "#ffffff"  
        self.entry_fg = "#000000"  
        self.entry_font = ("Arial", 10)  

        # LABEL ETIQUETAS
        self.label_frame = tk.LabelFrame(self.master)
        self.label_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.button_frame = tk.Frame(self.label_frame)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        self.equation_one = tk.Entry(self.button_frame, font=self.entry_font, bg=self.entry_bg, fg=self.entry_fg)
        self.equation_one.pack(side=tk.LEFT, padx=50, pady=8, fill=tk.X)
        self.label_equation_one = tk.Label(self.label_frame, text="Ecuación 1")
        self.label_equation_one.pack(side=tk.LEFT, padx=80, fill=tk.X)

        self.equation_two = tk.Entry(self.button_frame, font=self.entry_font, bg=self.entry_bg, fg=self.entry_fg)
        self.equation_two.pack(side=tk.RIGHT, padx=50, pady=8, fill=tk.X)
        self.label_equation_three = tk.Label(self.label_frame, text="Ecuación 3")
        self.label_equation_three.pack(side=tk.RIGHT, padx=80, fill=tk.X)

        self.equation_three = tk.Entry(self.button_frame, font=self.entry_font, bg=self.entry_bg, fg=self.entry_fg)
        self.equation_three.pack(side=tk.BOTTOM, padx=25, pady=8, fill=tk.X)
        self.label_equation_two = tk.Label(self.label_frame, text="Ecuación 2")
        self.label_equation_two.pack(side=tk.BOTTOM, padx=70, fill=tk.X)

        self.combobox_frame = tk.Frame(self.master)
        self.combobox_frame.pack()
        self.combobox_label_frame = tk.LabelFrame(self.combobox_frame)
        self.combobox_label_frame.pack(fill=tk.BOTH)

        self.entry_error = tk.Entry(self.combobox_frame, font=self.entry_font, bg=self.entry_bg, fg=self.entry_fg)
        self.entry_error.pack(side=tk.RIGHT, fill=tk.Y, padx=20)
        self.label_iterations = tk.Label(self.combobox_label_frame, text="Seleccione la cantidad de iteraciones:")
        self.label_iterations.pack(side=tk.LEFT, fill=tk.X, padx=30)
        
        self.combobox_iterations = ttk.Combobox(self.combobox_frame, values=[i for i in range(1, 1001)])
        self.combobox_iterations.pack(side=tk.LEFT, fill=tk.Y, padx=30)
        self.label_errors = tk.Label(self.combobox_label_frame, text="Ingrese el error deseado:")
        self.label_errors.pack(side=tk.RIGHT, fill=tk.X, padx=35)
        
        self.solve_button = tk.Button(self.master, text="Resolver", command= lambda: self.solver(), font=("Arial", 12, "bold"), bg="blue", fg="white")
        self.solve_button.pack(side=tk.BOTTOM, fill=tk.X, padx=25, pady=8)
        self.solver_frame = tk.Frame(self.master)
        self.solver_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=25, pady=8)
        
    def solver(self):
        try:
            self.solver_datagrid.get_children()
            self.solver_datagrid.destroy()
            solver(self)
        except:
            cantidad_variables = 3
            
            print(self.entry_error.get())
            self.solver_datagrid = ttk.Treeview(self.solver_frame, columns=[str(i) for i in range(cantidad_variables+2)], show="headings")
            self.solver_datagrid.heading("0", text="Iteración")
            
            for i in range(cantidad_variables+1):
                self.solver_datagrid.heading(str(i+1), text='X'+chr(8320 + i))
            self.solver_datagrid.pack()
                
                
            resultados=[[1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
            [17, 18, 19, 20]]
            iteraciones = self.combobox_iterations.get()
            if iteraciones:
                iteraciones = int(iteraciones)
            else:
                iteraciones = len(resultados)
            for i in range(iteraciones):
                resultados[i] = [i]+resultados[i]
            for i in range(iteraciones):
                self.solver_datagrid.insert("", "end", values=resultados[i])


        
    
        

root = tk.Tk()
root.title("Jacobi Display App")
root.geometry("680x420")
app = JacobiDisplayApp(root, None)
root.mainloop()
