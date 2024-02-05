import re
import numpy as np 
import sympy as sp

contador = 0
igualdades = ["", "", ""]
despejes = ["", "", ""]
x_jacobi = 0;
y_jacobi = 0;
z_jacobi = 0;

def obtener_valores(ecuacion):
    list = [int(numero) for numero in re.findall(r"-?\d+\.?\d*",ecuacion)]
    return list

def obtener_variables(ecuacion):
    list_var = re.findall('[a-zA-Z]',ecuacion)
    return sorted(list_var)

def obtener_mayor(list):
    listadosNumero = [num for num in list[:3]]
    print(max(listadosNumero))

def obtener_cocientes(list):
    cocientes = [num for num in list[:3]]
    return cocientes

def obtener_igualdad(list):
    igualdad = ""
    bandera = False

    for elemento in list:
        if(elemento == "="):
            bandera = True
        if(bandera):
            igualdad += elemento

    return igualdad

def matriz_var(ecuacion):
    var_matriz = []
    var_matriz.append(obtener_variables(ecuacion))
    print(var_matriz)


def despejar_incognitas(list, igualdad, bandera):
    x, y, z = sp.symbols('x y z')

    ecuacion = list[0]*x+list[1]*y+list[2]*z
    solucion = None
    ecuacion = sp.Eq(ecuacion, igualdad)
    variable = None

    if(bandera == 0):
        variable = x
    elif(bandera == 1):
        variable = y
    elif(bandera == 2):
        variable = z
    
    solucion = sp.solve(ecuacion, variable, dict=True)
    
    return solucion[0][variable]

def ordenar_matriz(matriz):
    global contador
    polinomio = ""
    matrizFinal = []
    matriz = np.array(matriz)

    indices_maximos = np.argmax(matriz, axis=1)
    
    matriz = matriz[np.argsort(indices_maximos)]
    
    for fila in matriz:
        for i in range(len(fila)):
            if(i == 0):
                polinomio += str(fila[i])+"x"
            if(i == 1):
                if(fila[i] > 0):
                    polinomio += "+"+str(fila[i])+"y"
                else:
                    polinomio += str(fila[i])+"y"
            if(i == 2):
                if(fila[i] > 0):
                    polinomio += "+"+str(fila[i])+"z"
                else:
                    polinomio += str(fila[i])+"z"
        matrizFinal.append(polinomio+igualdades[indices_maximos[contador]])
        polinomio = ""
        contador += 1

    return matrizFinal
    
                
def formar_matriz(ec1,ec2,ec3):
    matriz=[]
    for i in range(3):
        if i == 0:
            matriz.append(obtener_cocientes(obtener_valores(ec1)))
        elif i == 1:
            matriz.append(obtener_cocientes(obtener_valores(ec2)))
        elif i == 2:
            matriz.append(obtener_cocientes(obtener_valores(ec3)))

    igualdades[0] = obtener_igualdad(ec1)
    igualdades[1] = obtener_igualdad(ec2)
    igualdades[2] = obtener_igualdad(ec3)
    
    matriz = ordenar_matriz(matriz)
    despejes[0]=despejar_incognitas(obtener_cocientes(obtener_valores(matriz[0])), int(igualdades[0][1:]), 0)
    despejes[1]=despejar_incognitas(obtener_cocientes(obtener_valores(matriz[1])), int(igualdades[1][1:]), 1)  
    despejes[2]=despejar_incognitas(obtener_cocientes(obtener_valores(matriz[2])), int(igualdades[2][1:]), 2)

def calcularError(valorAnterior,aproximacion):
    error = np.abs((float(valorAnterior)-float(aproximacion)))
    error = float(f"{error:.8f}")
    return error
  
def sustiuir(ecuacion,valor1,valor2,simb1,simb2):
    cadena = ecuacion;
    expresion = sp.simplify(cadena)
    result = expresion.subs({simb1: valor1, simb2: valor2})
    return result

def decimal(num):
    if "/" in str(num):
        try:
            fraccion = float(num)
            return fraccion    
        except ValueError:
            return f"La fraccion {num} no es una fraccion valida"
    else:
        return num 
    
def jacobi(x_in,y_in,z_in,error_max,iteraciones):
    # Valores iniciales para las iteraciones
    x_jacobi = x_in
    y_jacobi = y_in
    z_jacobi = z_in
    #Formulas de los despejes
    x_form = '(3-y-2*z)/10'
    y_form = '(9-4*x+z)/6'
    z_form = '(51+2*x-3*y)/8'
    print(x_form)
    print(y_form)
    print(z_form)
    print(f"Iteracion 0: X:{x_jacobi} \tY:{y_jacobi} \tZ:{z_jacobi}");
    for i in range(1,iteraciones):
        x_new = decimal(sustiuir(x_form,y_jacobi,z_jacobi,"y","z"))
        y_new = decimal(sustiuir(y_form,x_jacobi,z_jacobi,"x","z"))
        z_new = decimal(sustiuir(z_form,x_jacobi,y_jacobi,"x","y"))
        if(x_jacobi != 0 and y_jacobi != 0 and z_jacobi != 0):
            error_x = calcularError(x_jacobi,x_new)
            error_y = calcularError(y_jacobi,y_new)
            error_z = calcularError(z_jacobi,z_new)
            if ((error_x < error_max and error_y < error_max and error_z < error_max)):
                return f"La ecuacion convergio en la Iteracion {i}: X:{x_jacobi} Error X:{error_x} Y:{y_jacobi} Error Y:{error_y} Z:{z_jacobi} Error Z:{error_z}"
        x_jacobi = x_new
        y_jacobi = y_new
        z_jacobi = z_new
        if(len(str(x_jacobi))>6 or len(str(y_jacobi))>6 or len(str(z_jacobi))>6):
            print(f"Iteración {i}: X: {x_jacobi:.7f}\tY: {y_jacobi:.7f}\tZ: {z_jacobi:.7f}\tErrores: X: {error_x*100:.2f}% \tY:{error_y*100:.2f}% \tZ:{error_z*100:.2f}%") 
        else:
          print(f"Iteración {i}: X: {x_jacobi}\tY: {y_jacobi}\tZ: {z_jacobi}")

formar_matriz("10x+y+2z=3",
              "4x+6y-z=9",
              "-2x+3y+8z=51")

jacobi(0,0,0,0.02,6)

#calcularError("-0.04569484","-0.04518692")