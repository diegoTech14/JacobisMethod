import re
import numpy as np 
import sympy as sp

contador = 0
igualdades = ["", "", ""]
despejes = ["", "", ""]

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
    print(matriz[0])
    despejes[0]=despejar_incognitas(obtener_cocientes(obtener_valores(matriz[0])), int(igualdades[0][1:]), 0)
    despejes[1]=despejar_incognitas(obtener_cocientes(obtener_valores(matriz[1])), int(igualdades[1][1:]), 1)  
    despejes[2]=despejar_incognitas(obtener_cocientes(obtener_valores(matriz[2])), int(igualdades[2][1:]), 2)

    print(despejes)
formar_matriz("2x-89z-4y=10",
              "-6y-4z+10x=11",
              "-2z+6y-9x=14")