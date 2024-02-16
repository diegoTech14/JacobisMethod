import re
import numpy as np 
import sympy as sp

contador = 0
igualdades = ["", "", ""]
despejes = ["", "", ""]
x_jacobi = 0
y_jacobi = 0
z_jacobi = 0
var = ["x","y","z"]

def ordenar_ecuacion(ecuacion,variables):
    ecuacion_ordenada = [0,0,0,0] #SE CREA UN VECTOR [X,Y,Z,C], DE MANERA QUE SI FALTA ALGUNA VARIABLE, LA MISMA QUEDA EN 0 POR DEFECTO
    for termino in ecuacion: #LA ECUACION LLEGA EN ESTA FORMA ['-2x', 'z', '3y', '20']
        if termino[-1] == str(variables[0]): #CON EL [-1] ME POSICIONO EN EL ÚLTIMO CARACTER DEL STRING OBTENIDO DEL ELEMENTO DEL VECTOR EXTRAIDO EN EL FOR "-2x" -> "x"
            if termino[:-1] == "-":#CON EL [:-1] ME POSICIONO EN LOS CARATERES DEL STRING OBTENIDO DEL ELEMENTO DEL VECTOR EXTRAIDO EN EL FOR OMITIENDO LA ULTIMA POSICION  "-2x" -> "-2"
                ecuacion_ordenada[0] = -1
                continue
            if termino[:-1] == "":#SI NO HAY UN VALOR ANTES DEL ÚLTIMO, ME GENERA UN CARACTER VACÍO "z" -> ""
                ecuacion_ordenada[0] = 1 #SE GENERA UN 1 REPRESENTANDO QUE SOLO EXISTE LA VARIABLE
                continue
            ecuacion_ordenada[0] = int(termino[:-1])#SI LA VARIABLE NO ESTÁ SOLA O EN ESTAS FORMAS "-x" - "y", ENTONCES AGREGAMOS EL VALOR QUE LAS ACOMPAÑA A LA ECUACIÓN ORDENADA
        if  termino[-1] == str(variables[1]):
            if termino[:-1] == "-":
                ecuacion_ordenada[1] = -1
                continue
            if termino[:-1] == "":
                ecuacion_ordenada[1] = 1
                continue
            ecuacion_ordenada[1] = int(termino[:-1])
        if termino[-1] == str(variables[2]):
            if termino[:-1] == "-":
                ecuacion_ordenada[2] = -1
                continue
            if termino[:-1] == "":
                ecuacion_ordenada[2] = 1
                continue
            ecuacion_ordenada[2] = int(termino[:-1])
    ecuacion_ordenada[3] = int(ecuacion[-1])
    return ecuacion_ordenada

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

def incognitas(ecuacion):
    variables = sorted(re.findall('[a-zA-Z]',ecuacion))
    vars = ["x","y","z"]
    frag_ecuacion = ecuacion.split("=")
    izquierda = frag_ecuacion[0].strip()
    parte_ecuacion = izquierda.split()
    for partes in parte_ecuacion:
        for i, variable in enumerate(variables):
            if(variable in partes):
                if vars[i] not in variables:
                    vars[i] = "0"
                else:
                    vars[i] = variables[i]
    return vars

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
    
def despejar_incognitas(list, igualdad, bandera,incognitas):
    for i in range(len(incognitas)):
        if isinstance(incognitas[i], str):
            incognitas[i] = sp.symbols(incognitas[i])
    ecuacion = list[0]*incognitas[0]+list[1]*incognitas[1]+list[2]*incognitas[2]
    solucion = None
    ecuacion = sp.Eq(ecuacion, igualdad)
    variable = None

    if(bandera == 0):
        variable = incognitas[0]
    elif(bandera == 1):
        variable = incognitas[1]
    elif(bandera == 2):
        variable = incognitas[2]
    
    solucion = sp.solve(ecuacion, variable, dict=True)
    return solucion[0][variable]


def ordenar_matriz(matriz,variables):
    variables_symbols = ''.join(map(str,variables))
    global contador
    polinomio = ""
    matrizFinal = []
    matriz = np.array(matriz)

    indices_maximos = np.argmax(matriz, axis=1)
    
    matriz = matriz[np.argsort(indices_maximos)]
    
    for fila in matriz:
        for i in range(len(fila)):
            if(i == 0):
                if fila[i] == 0:  # Agregar un signo más para elementos positivos
                    polinomio += "+" + str(fila[i]) + variables_symbols[i]
                else:
                    polinomio += str(fila[i])+variables_symbols[0]
            if(i == 1):
                if fila[i] == 0:  # Agregar un signo más para elementos positivos
                    polinomio += "+" + str(fila[i]) + variables_symbols[i]
                elif fila[i] > 0:
                    polinomio += "+" + str(fila[i]) + variables_symbols[i]
                else:
                    polinomio += str(fila[i])+variables_symbols[1]
            if(i == 2):
                if fila[i] == 0:  # Agregar un signo más para elementos positivos
                    polinomio += "+" + str(fila[i]) + variables_symbols[i]
                elif fila[i] > 0:
                    polinomio += "+" + str(fila[i]) + variables_symbols[i]
                else:
                    polinomio += str(fila[i])+variables_symbols[2]
        matrizFinal.append(polinomio+igualdades[indices_maximos[contador]])
        polinomio = ""
        contador += 1
    return matrizFinal  

def asingnarVar(inc):
    var.clear()
    for element in inc:
        var.append(element)
                
def formar_matriz(ec1,ec2,ec3):
    matriz=[]
    for i in range(3):
        if i == 0:
            matriz.append(ordenar_ecuacion(separar_terminos_ecuacion(ec1),incognitas(ec1))[:3])
        elif i == 1:
            matriz.append(ordenar_ecuacion(separar_terminos_ecuacion(ec2),incognitas(ec2))[:3])
        elif i == 2:
            matriz.append(ordenar_ecuacion(separar_terminos_ecuacion(ec3),incognitas(ec3))[:3])
            
    igualdades[0] = obtener_igualdad(ec1)
    igualdades[1] = obtener_igualdad(ec2)
    igualdades[2] = obtener_igualdad(ec3)
    matriz = ordenar_matriz(matriz,var)
    despejes[0]=despejar_incognitas(ordenar_ecuacion(separar_terminos_ecuacion(matriz[0]),incognitas(ec1)), int(igualdades[0][1:]), 0,incognitas(ec1))
    despejes[1]=despejar_incognitas(ordenar_ecuacion(separar_terminos_ecuacion(matriz[1]),incognitas(ec2)), int(igualdades[1][1:]), 1,incognitas(ec2))  
    despejes[2]=despejar_incognitas(ordenar_ecuacion(separar_terminos_ecuacion(matriz[2]),incognitas(ec3)), int(igualdades[2][1:]), 2,incognitas(ec3))

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
    
def jacobi(error_max,iteraciones):
    # Valores iniciales para las iteraciones
    x_jacobi = 0
    y_jacobi = 0
    z_jacobi = 0
    #Formulas de los despejes
    x_form = despejes[0]
    y_form = despejes[1]
    z_form = despejes[2]
    if (iteraciones == 0 and error_max == 0):
        ValueError("No se establecieron los paremetro necesarios")
    if (iteraciones > 0 and error_max > 0): # Condicion Unica ejecuta el metodo tanto por error como por iteraciones
        jacobi(error_max,0)
        jacobi(0,iteraciones)
        iteraciones = -1
        error_max = -1
    if iteraciones > 0: # Ciclo con iteraciones
        print("Condicion de Parada ->\t",iteraciones,"iteraciones")
        print(f"Iteracion 1: X:{x_jacobi} \tY:{y_jacobi} \tZ:{z_jacobi}")
        for i in range(1,iteraciones):
            x_new = decimal(sustiuir(x_form,y_jacobi,z_jacobi,var[1],var[2]))
            y_new = decimal(sustiuir(y_form,x_jacobi,z_jacobi,var[0],var[2]))
            z_new = decimal(sustiuir(z_form,x_jacobi,y_jacobi,var[0],var[1]))
            if(x_jacobi != 0 and y_jacobi != 0 and z_jacobi != 0):
                error_x = calcularError(x_jacobi,x_new)*100
                error_y = calcularError(y_jacobi,y_new)*100
                error_z = calcularError(z_jacobi,z_new)*100
            x_jacobi = x_new
            y_jacobi = y_new
            z_jacobi = z_new
            if(len(str(x_jacobi))>6 or len(str(y_jacobi))>6 or len(str(z_jacobi))>6):
                print(f"Iteración {i+1}: X: {x_jacobi:.8f}\tY: {y_jacobi:.8f}\tZ: {z_jacobi:.8f}\tErrores: {var[0]}: {error_x:.2f}% \t{var[1]}:{error_y:.2f}% \t{var[2]}:{error_z:.2f}%") 
            else:
                print(f"Iteración {i+1}: X: {x_jacobi}\tY: {y_jacobi}\tZ: {z_jacobi}")
    if iteraciones == 0: # Ciclo con error minimo
        print("Condicion de Parada ->\tError menor a",error_max,"%")
        print(f"Iteracion 0: X:{x_jacobi} \tY:{y_jacobi} \tZ:{z_jacobi}")
        error_x = 0
        error_y = 0
        error_z = 0
        i = 0
        while True:
            i+=1
            x_new = decimal(sustiuir(x_form,y_jacobi,z_jacobi,var[1],var[2]))
            y_new = decimal(sustiuir(y_form,x_jacobi,z_jacobi,var[0],var[2]))
            z_new = decimal(sustiuir(z_form,x_jacobi,y_jacobi,var[0],var[1]))
            if(x_jacobi != 0 and y_jacobi != 0 and z_jacobi != 0):
                error_x = calcularError(x_jacobi,x_new)*100
                error_y = calcularError(y_jacobi,y_new)*100
                error_z = calcularError(z_jacobi,z_new)*100
                if ((error_x < error_max) and (error_y < error_max) and (error_z < error_max)):
                    x_jacobi = x_new
                    y_jacobi = y_new
                    z_jacobi = z_new
                    print(f"Iteración {i}: X: {x_jacobi:.8f}\tY: {y_jacobi:.8f}\tZ: {z_jacobi:.8f}\tErrores: X: {error_x:.2f}% \tY:{error_y:.2f}% \tZ:{error_z:.2f}%")
                    break
            x_jacobi = x_new
            y_jacobi = y_new
            z_jacobi = z_new
            if(i>20):
                break
            if(len(str(x_jacobi))>6 or len(str(y_jacobi))>6 or len(str(z_jacobi))>6):
                print(f"Iteración {i}: X: {x_jacobi:.8f}\tY: {y_jacobi:.8f}\tZ: {z_jacobi:.8f}\tErrores: X: {error_x:.2f}% \tY:{error_y:.2f}% \tZ:{error_z:.2f}%") 
            else:
                print(f"Iteración {i}: X: {x_jacobi}\tY: {y_jacobi}\tZ: {z_jacobi}")

             
formar_matriz("10x+y+2z=3",
             "4x+6y-z=9",
            "-2x+3y+8z=51")

jacobi(25,0) # Recibe el error y la iteraciones