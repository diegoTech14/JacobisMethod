import re

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
    return sorted(cocientes)

def obtener_igualdad(list):
    ig = [num for num in list[3:]]
    print(ig)

def matriz_var(ecuacion):
    var_matriz = []
    var_matriz.append(obtener_variables(ecuacion))
    print(var_matriz)

def formar_matriz(ec1,ec2,ec3):
    matriz=[]
    for i in range(3):
        if i == 0:
            matriz.append(obtener_cocientes(obtener_valores(ec1)))
        elif i == 1:
            matriz.append(obtener_cocientes(obtener_valores(ec2)))
        elif i == 2:
            matriz.append(obtener_cocientes(obtener_valores(ec3)))
    matriz_var(ec1)
    obtener_igualdad(obtener_valores(ec1))
    obtener_igualdad(obtener_valores(ec2))
    obtener_igualdad(obtener_valores(ec3))
    print(matriz)
    

formar_matriz("2x-89z+4y=10","4y-6z-10x=11","2z-6y-9x=14")