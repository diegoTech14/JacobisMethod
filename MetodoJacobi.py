import re
import numpy as np 
import sympy as sp
import tabulate as tb

class JacobiMethod:
    def __init__(self):
        self.contador = 0
        self.igualdades = ["", "", ""]
        self.despejes = ["", "", ""]
        self.x_jacobi = 0
        self.y_jacobi = 0
        self.z_jacobi = 0
        self.var = ["x", "y", "z"]
        self.jacobi_iteraciones=[]
        self.salida = ""
    
    #Metodos de impresion
    def imprimirIteraciones(self):
        self.salida += "\n"
        self.salida += (tb.tabulate(self.jacobi_iteraciones,headers=["Iteracion","X","Y","Z","Error X","Error Y","Error Z"],tablefmt="fancy_grid",floatfmt=(".0f",".7f",".7f",".7f",".2f",".2f",".2f")))
    
    def imprirFormulas(self):
        formulas = []
        formulas.append(self.despejes)
        self.salida += "\n"
        self.salida += (tb.tabulate(formulas,headers=["Formula X","Formula Y","Formula Z"],tablefmt="fancy_grid"))
    
    def ordenar_ecuacion(self,ecuacion, variables):
        ecuacion_ordenada = [0, 0, 0, 0]  # SE CREA UN VECTOR [X,Y,Z,C], DE MANERA QUE SI FALTA ALGUNA VARIABLE, LA MISMA QUEDA EN 0 POR DEFECTO
        for termino in ecuacion:  # LA ECUACION LLEGA EN ESTA FORMA ['-2x', 'z', '3y', '20']
            if termino[-1] == str(variables[0]):  # CON EL [-1] ME POSICIONO EN EL ÚLTIMO CARACTER DEL STRING OBTENIDO DEL ELEMENTO DEL VECTOR EXTRAIDO EN EL FOR "-2x" -> "x"
                if termino[:-1] == "-":  # CON EL [:-1] ME POSICIONO EN LOS CARATERES DEL STRING OBTENIDO DEL ELEMENTO DEL VECTOR EXTRAIDO EN EL FOR OMITIENDO LA ULTIMA POSICION  "-2x" -> "-2"
                    ecuacion_ordenada[0] = -1
                    continue
                if termino[:-1] == "":  # SI NO HAY UN VALOR ANTES DEL ÚLTIMO, ME GENERA UN CARACTER VACÍO "z" -> ""
                    ecuacion_ordenada[0] = 1  # SE GENERA UN 1 REPRESENTANDO QUE SOLO EXISTE LA VARIABLE
                    continue
                ecuacion_ordenada[0] = int(termino[:-1])  # SI LA VARIABLE NO ESTÁ SOLA O EN ESTAS FORMAS "-x" - "y", ENTONCES AGREGAMOS EL VALOR QUE LAS ACOMPAÑA A LA ECUACIÓN ORDENADA
            if termino[-1] == str(variables[1]):
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

    def separar_terminos_ecuacion(self,string_ecuacion):
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

    #Regresa la incognita X,Y,Z de la ecuacion
    def incognitas(self, ecuacion):
        variables = sorted(re.findall('[a-zA-Z]', ecuacion))  # Crea una lista de las variables contenidas en la ecuación ingresada
        vars = ["x", "y", "z"]  # Forma por defecto de la ecuación
        frag_ecuacion = ecuacion.split("=")  # Separamos la ecuación mediante el signo de igual
        izquierda = frag_ecuacion[0].strip()  # Borramos los espacios en blanco solo de la parte izquierda de la ecuación
        parte_ecuacion = izquierda.split()  # Separamos las partes restantes de la ecuación
        for partes in parte_ecuacion:
            for i, variable in enumerate(variables):
                if(variable in partes):
                    if vars[i] not in variables:  # Buscamos si las variables X, Y, Z están presentes en las variables
                        vars[i] = "0"  # Si no están, ponemos un 0
        return vars

    #Obtiene el valor de la igualdad de las ecuaciones
    def obtener_igualdad(self,list):
        igualdad = ""
        bandera = False    
        for elemento in list: 
            if(elemento == "="): 
                bandera = True
            if(bandera):
                igualdad += elemento #Agrega el elemento a las igualdades en caso de que se encuentre el =
        return igualdad

    #Realiza el despeje de las incognitas
    #recibe una lista de la ecuaciones, las igualdades y las incognitas
    def despejar_incognitas(self,list, igualdad, bandera,incognitas):
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

    #Realiza el ordenamiento de la matriz
    #Recibe la matriz y la variables
    def ordenar_matriz(self, matriz, variables):
        variables_symbols = ''.join(map(str, variables))
        self.contador
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
                        polinomio += str(fila[i]) + variables_symbols[0]
                if(i == 1):
                    if fila[i] == 0:  # Agregar un signo más para elementos positivos
                        polinomio += "+" + str(fila[i]) + variables_symbols[i]
                    elif fila[i] > 0:
                        polinomio += "+" + str(fila[i]) + variables_symbols[i]
                    else:
                        polinomio += str(fila[i]) + variables_symbols[1]
                if(i == 2):
                    if fila[i] == 0:  # Agregar un signo más para elementos positivos
                        polinomio += "+" + str(fila[i]) + variables_symbols[i]
                    elif fila[i] > 0:
                        polinomio += "+" + str(fila[i]) + variables_symbols[i]
                    else:
                        polinomio += str(fila[i]) + variables_symbols[2]
            matrizFinal.append(polinomio + self.igualdades[indices_maximos[self.contador]])
            polinomio = ""
            self.contador += 1
        return matrizFinal
  
    #Crea la matriz mediante las ecuaciones ingresadas
    #Recibe tres ecuaciones dependientes de las variables x,y,z              
    def formar_matriz(self,ec1,ec2,ec3):
        matriz=[]
        for i in range(3):
            if i == 0:
                matriz.append(self.ordenar_ecuacion(self.separar_terminos_ecuacion(ec1),self.incognitas(ec1))[:3])
            elif i == 1:
                matriz.append(self.ordenar_ecuacion(self.separar_terminos_ecuacion(ec2),self.incognitas(ec2))[:3])
            elif i == 2:
                matriz.append(self.ordenar_ecuacion(self.separar_terminos_ecuacion(ec3),self.incognitas(ec3))[:3])
            
            #Se obtiene la igualdad perteneciente a cada ecuacion y se ingresa en la lista de igualdades       
        self.igualdades[0] = self.obtener_igualdad(ec1)
        self.igualdades[1] = self.obtener_igualdad(ec2)
        self.igualdades[2] = self.obtener_igualdad(ec3)
        #Reordenamos la matriz para mantener los mayores valores en la diagonal principal
        matriz = self.ordenar_matriz(matriz,self.var)
        self.salida += str(matriz)+"\n"
        #Creamos los despejes o formulas pertencientes a la cada ecuacion mediante la matriz, las igualdades y las incognitas de cada ecuacion 
        self.despejes[0]=self.despejar_incognitas(self.ordenar_ecuacion(self.separar_terminos_ecuacion(matriz[0]),self.incognitas(ec1)), int(self.igualdades[0][1:]), 0,self.incognitas(ec1))
        self.despejes[1]=self.despejar_incognitas(self.ordenar_ecuacion(self.separar_terminos_ecuacion(matriz[1]),self.incognitas(ec2)), int(self.igualdades[1][1:]), 1,self.incognitas(ec2))  
        self.despejes[2]=self.despejar_incognitas(self.ordenar_ecuacion(self.separar_terminos_ecuacion(matriz[2]),self.incognitas(ec3)), int(self.igualdades[2][1:]), 2,self.incognitas(ec3))

    #Realiza el calculo del error de lass iteraciones
    #Recibe un valor anterior y un valor actual
    def calcularError(self,valorAnterior,aproximacion):
        error = np.abs((float(valorAnterior)-float(aproximacion))) #Aplicamos la formula | anterior - actual(aproximacion) |
        error = float(f"{error:.8f}") #Truncamos el error con un maximo de 8 decimales
        return error

    #Realiza la conversion de la formula de string a una ecuacion matematica
    #Recibe la ecuacion, los valores y los simbolos de la ecuacion  
    def sustiuir(self,ecuacion,valor1,valor2,simb1,simb2):
        cadena = ecuacion
        expresion = sp.simplify(cadena) #Convierte la cadena a una ecuacion matematica
        result = expresion.subs({simb1: valor1, simb2: valor2}) #Sustituye el valor las incognitas y resuelve la ecuaciones
        return result

    #Convierte las fracciones a usa valor decimal
    #Recibe el numero
    def decimal(self,num):
        if "/" in str(num): #Busca si el signo / se encuentra en el numero recibido
            try:
                #Si el signo se encuentra realiza la operacion
                fraccion = float(num) 
                return fraccion    
            except ValueError:
                return f"La fraccion {num} no es una fraccion valida"
        else: #En caso de que no este el signo se devuelve el numero
            return num 

    #Simula las operaciones del metodo de jacobi
    #Recibe el numero de iteraciones y el error maximo   
    def jacobi(self,error_max,iteraciones):
        # Valores iniciales para las iteraciones por defecto se comienza en cero
        self.x_jacobi = 0
        self.y_jacobi = 0
        self.z_jacobi = 0
        #Formulas de los despejes
        x_form = self.despejes[0]
        y_form = self.despejes[1]
        z_form = self.despejes[2]
        self.imprirFormulas()
        if (iteraciones == 0 and error_max == 0): #En caso de que se ingresen 0 iteraciones y 0 en error se da el mensaje de error
            self.salida += ("\nNo se establecieron los paremetros necesarios")
        if (iteraciones > 0 and error_max > 0): # Condicion Unica ejecuta el metodo tanto por error como por iteraciones
            self.jacobi(error_max,0) #Realiza el metodo con el error
            self.jacobi_iteraciones = [] #vaciamos la lista
            self.jacobi(0,iteraciones) #Realiza el metodo con la iteraciones
            #Cambia los valores ingresado para detener los ciclos
            iteraciones = -1
            error_max = -1
            self.jacobi_iteraciones = []
        if iteraciones > 0 and error_max < 0: # Ciclo con iteraciones
            self.salida += "\n\nCondicion de parada -> "+ str(iteraciones) + " iteraciones"
            list = [1,self.x_jacobi,self.y_jacobi,self.y_jacobi]
            self.jacobi_iteraciones.append(list)
            for i in range(1,iteraciones): # El ciclo se realiza hasta la iteraciones ingresada iniciando en 1
                #Calculamos la X,Y,Z con las forumlas y los valores anteriores a la iteracion actual
                x_new = self.decimal(self.sustiuir(x_form,self.y_jacobi,self.z_jacobi,self.var[1],self.var[2]))
                y_new = self.decimal(self.sustiuir(y_form,self.x_jacobi,self.z_jacobi,self.var[0],self.var[2]))
                z_new = self.decimal(self.sustiuir(z_form,self.x_jacobi,self.y_jacobi,self.var[0],self.var[1]))
                if(self.x_jacobi != 0 and self.y_jacobi != 0 and self.z_jacobi != 0): #Realizamos el calculo de errores si los valores X,Y,Z son diferentes a 0
                    error_x = self.calcularError(self.x_jacobi,x_new)*100
                    error_y = self.calcularError(self.y_jacobi,y_new)*100
                    error_z = self.calcularError(self.z_jacobi,z_new)*100
                    #Reasignamos X,Y,Z con los valores actuales y repetimos el ciclo
                self.x_jacobi = x_new
                self.y_jacobi = y_new
                self.z_jacobi = z_new
                if(len(str(self.x_jacobi))>6 or len(str(self.y_jacobi))>6 or len(str(self.z_jacobi))>6 and i > 2):
                    list = [i+1,float(self.x_jacobi),float(self.y_jacobi),float(self.z_jacobi),error_x,error_y,error_z]
                else:
                   list = [i+1,self.x_jacobi,self.y_jacobi,self.z_jacobi]
                self.jacobi_iteraciones.append(list)
            self.imprimirIteraciones()
        if iteraciones == 0 and error_max > 0: # Ciclo con error minimo
            self.salida += "\nCondicion de parada -> \tError menor a:" +str(error_max)
            list = [1,self.x_jacobi,self.y_jacobi,self.y_jacobi]
            self.jacobi_iteraciones.append(list)
            error_x = 0
            error_y = 0
            error_z = 0
            i = 0
            while True: #El ciclo se ejecuta con la sentencia While True porque no exite una condicion de para directa
                i+=1 #Aumentamos el contador de iteraciones
                #Calculamos la X,Y,Z con las forumlas y los valores anteriores a la iteracion actual
                x_new = self.decimal(self.sustiuir(x_form,self.y_jacobi,self.z_jacobi,self.var[1],self.var[2]))
                y_new = self.decimal(self.sustiuir(y_form,self.x_jacobi,self.z_jacobi,self.var[0],self.var[2]))
                z_new = self.decimal(self.sustiuir(z_form,self.x_jacobi,self.y_jacobi,self.var[0],self.var[1]))
                if(self.x_jacobi != 0 and self.y_jacobi != 0 and self.z_jacobi != 0): #Realizamos el calculo de errores si los valores X,Y,Z son diferentes a 0
                    error_x = self.calcularError(self.x_jacobi,x_new)*100
                    error_y = self.calcularError(self.y_jacobi,y_new)*100
                    error_z = self.calcularError(self.z_jacobi,z_new)*100
                    if ((error_x < error_max) and (error_y < error_max) and (error_z < error_max)):
                        #Si los tres errores son menores al maximo asignamos los valores de X,Y,Z y rompemos el bucle
                        self.x_jacobi = x_new
                        self.y_jacobi = y_new
                        self.z_jacobi = z_new
                        list = [i+1,float(self.x_jacobi),float(self.y_jacobi),float(self.z_jacobi),error_x,error_y,error_z]
                        self.jacobi_iteraciones.append(list)
                        self.imprimirIteraciones()
                        break
                    #Reasignamos X,Y,Z con los valores actuales y repetimos el ciclo
                self.x_jacobi = x_new
                self.y_jacobi = y_new
                self.z_jacobi = z_new
                if(i>20): #Maximo de iteraciones establecido para la convergencia del metodo una vez llegado aqui se finaliza por defecto
                    break
                if(len(str(self.x_jacobi))>6 or len(str(self.y_jacobi))>6 or len(str(self.z_jacobi))>6 and i > 2):
                    list = [i+1,float(self.x_jacobi),float(self.y_jacobi),float(self.z_jacobi),error_x,error_y,error_z]
                else:
                   list = [i+1,self.x_jacobi,self.y_jacobi,self.z_jacobi]
                self.jacobi_iteraciones.append(list)
    #Se encarga de toda la ejecucion del programa
    #Recibe las 3 ecuaciones, el error o las iteraciones
    def ejecucion(self,ecuacion1,ecuacion2,ecuacion3,error_maximo,iteraciones):
        self.formar_matriz(ecuacion1,ecuacion2,ecuacion3)
        self.jacobi(error_maximo,iteraciones)
        return self.salida

jacobi_solve = JacobiMethod()
print(jacobi_solve.ejecucion("10x+y+2z=3","4x+6y-z=9","-2x+3y+8z=51",0,0))