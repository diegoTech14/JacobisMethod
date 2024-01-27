#Teniendo la ecuacion Ax=b, se resuelve el sistema de ecuaciones lineales
#con el metodo de Jacobi
#Se requiere que la matriz A sea diagonalmente dominante
#
#Para este metodo se requiere que la matriz A sea diagonalmente dominante
#es decir, que el valor absoluto de cada elemento de la diagonal sea mayor
#al valor absoluto de la suma de los demas elementos de la fila
#
#Para la matriz:
#  3 -0.1 -0.2  7.85
#0.1    7  -0.3 -19.3
#0.3 -0.2   10   71.4
#
#El sistema de ecuaciones es:
#  3x1 -0.1x2 -0.2x3 =  7.85
#0.1x1    7x2  -0.3x3 = -19.3
#0.3x1 -0.2x2    10x3 =  71.4
#
#La solucion es:
#x1 = 3.000000
#x2 = -2.500000
#x3 = 7.000000
#
#El error relativo es:
#Error relativo:  0.000000
#
import numpy as np
import math

#Generame el algoritmo que resuelve todos los comentarios anteriores
def jacobi(A,b,x0,tol):
    #Obtenemos la matriz de coeficientes
    D = np.diag(np.diag(A))
    print(D,'D\n')
    #Obtenemos la matriz de coeficientes
    L = -np.tril(A,-1)
    print(L,'L\n')
    #Obtenemos la matriz de coeficientes
    U = -np.triu(A,1)
    print(U,'U\n')
    #Obtenemos la matriz de coeficientes
    T = np.dot(np.linalg.inv(D),(L+U))
    print(T,'T\n')
    #Obtenemos la matriz de coeficientes
    C = np.dot(np.linalg.inv(D),b)
    print(C,'C\n')
    #Obtenemos la matriz de coeficientes
    x1 = np.dot(T,x0)+C
    print(x1,'x1\n')
    #Obtenemos el error relativo
    error = np.linalg.norm(x1-x0)/np.linalg.norm(x1)
    #Si el error es menor que la tolerancia, terminamos
    if error<tol:
        return x1
    #Si no, volvemos a llamar a la funcion
    else:
        return jacobi(A,b,x1,tol)
#Todo lo anterior debe tener la posibilidad de mostrarse en la consola sin un print sino mediante un string acumulativo, como un registro de logs  
#Definimos la matriz A
A = np.array([[3,-0.1,-0.2],[0.1,7,-0.3],[0.3,-0.2,10]])
#Definimos el vector b
b = np.array([7.85,-19.3,71.4])
#Definimos el vector inicial
x0 = np.array([0,0,0])
#Definimos la tolerancia
tol = 0.0000001
#Llamamos a la funcion
x = jacobi(A,b,x0,tol)
#Mostramos el resultado
print("La solucion es:")
print("x1 =",x[0])
print("x2 =",x[1])
print("x3 =",x[2])
#Calculamos el error relativo
error = np.linalg.norm(np.dot(A,x)-b)/np.linalg.norm(b)
#Mostramos el error relativo
print("\nEl error relativo es:")
print("Error relativo: ",error)

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class JacobiSolver:
    def __init__(self, A, b, x0, tolerance=1e-6, max_iterations=100):
        self.A = A.astype(float)  # Convierte a tipo de dato float para permitir cálculos con decimales
        self.b = b.astype(float)
        self.x0 = x0.astype(float)
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.solution = None
        self.iterations = None

    def solve(self):
        # Implementa el método de Jacobi aquí
        n = len(self.b)
        x = np.copy(self.x0)
        x_new = np.zeros_like(x)

        iterations = 0
        while iterations < self.max_iterations:
            for i in range(n):
                sigma = np.dot(self.A[i, :n], x[:n])
                x_new[i] = (self.b[i] - sigma + self.A[i, i] * x[i]) / self.A[i, i]

            if np.linalg.norm(x_new - x) < self.tolerance:
                break

            x = np.copy(x_new)
            iterations += 1

        self.solution = x_new
        self.iterations = iterations

class JacobiGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Método de Jacobi")
        self.geometry("800x600")

        self.A = np.array([[4, 2, 8, 7], [2, 4, 2, 5], [6, 1, 4, 2], [4, 2, 1, 3]])
        self.b = np.array([1, 1, 4, 2])
        self.x0 = np.zeros_like(self.b)

        self.jacobi_solver = JacobiSolver(self.A, self.b, self.x0)

        self.create_widgets()

    def create_widgets(self):
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas = FigureCanvasTkAgg(self.plot_solution(), master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.solve_button = ttk.Button(self, text="Solve", command=self.solve_jacobi)
        self.solve_button.pack(side=tk.BOTTOM)

    def solve_jacobi(self):
        self.jacobi_solver.solve()
        self.update_plot()

    def update_plot(self):
        self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.plot_solution(), master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def plot_solution(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        if self.jacobi_solver.solution is not None:
            # Grafica la solución si está disponible
            x = np.arange(len(self.jacobi_solver.solution))
            ax.plot(x, self.jacobi_solver.solution, label='Solución')

            ax.set_xlabel('Iteraciones')
            ax.set_ylabel('Valor de la solución')
            ax.legend()
        else:
            # Muestra un mensaje indicando que la solución no está disponible
            ax.text(0.5, 0.5, 'Ejecuta el método de Jacobi primero', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

        return fig


if __name__ == "__main__":
    app = JacobiGUI()
    app.mainloop()
