import re
import numpy as np 
import sympy as sp

contador = 0
igualdades = ["", "", ""]
despejes = ["", "", ""]
x_jacobi = 0;
y_jacobi = 0;
z_jacobi = 0;


def ordenar_ecuacion(ecuacion):
    ecuacion_ordenada = [0,0,0,0] #SE CREA UN VECTOR [X,Y,Z,C], DE MANERA QUE SI FALTA ALGUNA VARIABLE, LA MISMA QUEDA EN 0 POR DEFECTO
    for termino in ecuacion: #LA ECUACION LLEGA EN ESTA FORMA ['-2x', 'z', '3y', '20']
        if termino[-1] == "x": #CON EL [-1] ME POSICIONO EN EL ÚLTIMO CARACTER DEL STRING OBTENIDO DEL ELEMENTO DEL VECTOR EXTRAIDO EN EL FOR "-2x" -> "x"
            if termino[:-1] == "-":#CON EL [:-1] ME POSICIONO EN LOS CARATERES DEL STRING OBTENIDO DEL ELEMENTO DEL VECTOR EXTRAIDO EN EL FOR OMITIENDO LA ULTIMA POSICION  "-2x" -> "-2"
                ecuacion_ordenada[0] = -1
                continue
            if termino[:-1] == "":#SI NO HAY UN VALOR ANTES DEL ÚLTIMO, ME GENERA UN CARACTER VACÍO "z" -> ""
                ecuacion_ordenada[0] = 1 #SE GENERA UN 1 REPRESENTANDO QUE SOLO EXISTE LA VARIABLE
                continue
            ecuacion_ordenada[0] = int(termino[:-1])#SI LA VARIABLE NO ESTÁ SOLA O EN ESTAS FORMAS "-x" - "y", ENTONCES AGREGAMOS EL VALOR QUE LAS ACOMPAÑA A LA ECUACIÓN ORDENADA
        if termino[-1] == "y":
            if termino[:-1] == "-":
                ecuacion_ordenada[1] = -1
                continue
            if termino[:-1] == "":
                ecuacion_ordenada[1] = 1
                continue
            ecuacion_ordenada[1] = int(termino[:-1])
        if termino[-1] == "z":
            if termino[:-1] == "-":
                ecuacion_ordenada[2] = -1
                continue
            if termino[:-1] == "":
                ecuacion_ordenada[2] = 1
                continue
            ecuacion_ordenada[2] = int(termino[:-1])
    ecuacion_ordenada[3] = int(ecuacion[-1])
    return ecuacion_ordenada #DEVUELVE EL VECTOR DIRECTOR DE LA ECUACIÓN
#print(ordenar_ecuacion(['x', '3z', '5y', '3']))


def separar_terminos_ecuacion(string_ecuacion):
    lista_ecuacion = []
    string_temp = ""
    for caracter in string_ecuacion:
        if caracter == "-": #SI EL CARACTER CORRESPONDE A UN NEGATIVO
            if string_temp == "": #VERIFICAMOS QUE EL STRING TEMPORAL ESTÉ VACÍO Y LE ASIGNAMOS UN NEGATIVO
                string_temp = "-" #SE LE ASIGNA UN NEGATIVO PORQUE AL TERMINAR DE VERIFICAR LOS IF, SE LE VA A AGREGAR EL TERMINO QUE COMPLETA ESE NEGATIVO
                continue
            lista_ecuacion += [string_temp]#EN CASO DE QUE EL STRING TEMP NO ESTÉ VACÍO, SE PROCEDE A AÑADIR EL STRING TEMPORAL FORMADO A LA LISTA DE LA ECUACION SEPARADA
            string_temp = "" #SE VUELVE A VACIAR EL STRING TEMPORAL PARA LLENARLO DE NUEVO
        if caracter == "+":
            lista_ecuacion += [string_temp]
            string_temp = ""
            continue
        if caracter == "=":
            lista_ecuacion += [string_temp]
            string_temp = ""
            continue
        string_temp += caracter #SI SE VERIFICA TODOS LOS IF Y NO HAY ALGUN SIGNO DE OPERACIÓN O IGUALDAD, SE LE AÑADE AL STRING TEMPORAL EL NUMERO O LETRA QUE CORRESPONDA
    lista_ecuacion += [string_temp] #AL TERMINAR EL FOR, SE AÑADE LO ÚLTIMO QUE SE AGREGÓ AL STRING TEMPORAL PARA NO DEJAR POR FUERA LOS ULTIMOS TERMINOS DE LA ECUACION
    return lista_ecuacion

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
    var_matriz.append(ordenar_ecuacion(separar_terminos_ecuacion(ecuacion)))
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
            matriz.append(ordenar_ecuacion(separar_terminos_ecuacion(ec1))[:3])
        elif i == 1:
            matriz.append(ordenar_ecuacion(separar_terminos_ecuacion(ec2))[:3])
        elif i == 2:
            matriz.append(ordenar_ecuacion(separar_terminos_ecuacion(ec3))[:3])
            
    igualdades[0] = obtener_igualdad(ec1)
    igualdades[1] = obtener_igualdad(ec2)
    igualdades[2] = obtener_igualdad(ec3)
    
    matriz = ordenar_matriz(matriz)
    
    print(matriz[0])
    despejes[0]=despejar_incognitas(ordenar_ecuacion(separar_terminos_ecuacion(matriz[0])), int(igualdades[0][1:]), 0)
    despejes[1]=despejar_incognitas(ordenar_ecuacion(separar_terminos_ecuacion(matriz[1])), int(igualdades[1][1:]), 1)  
    despejes[2]=despejar_incognitas(ordenar_ecuacion(separar_terminos_ecuacion(matriz[2])), int(igualdades[2][1:]), 2)

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
    x_form = despejes[0]
    y_form = despejes[1]
    z_form = despejes[2]
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

print("Despeje Automatizado")
formar_matriz("10x+y+2z=3",
             "4x+6y-z=9",
            "-2x+3y+8z=51")

jacobi(0,0,0,0.02,6)
