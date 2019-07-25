
def enlista(num):
    '''Devuelve una lista con los digitos de un numero pasado por parámetro'''
    return list(map(int, str(num)))


def creciente(num):
    '''Devuelve True si el numero pasado por parámetro es creciente'''
    lista = enlista(num)
    creci = True
    # ciclo para la comparacion de digitos adyacentes
    for pos in range(0, len(str(num)) - 1):
        if lista[pos + 1] < lista[pos]:
            creci = False
            break
    return creci


def decreciente(num):
    '''Devuelve True si el numero pasado por parámetro es decreciente'''
    lista = enlista(num)
    decre = True
    # ciclo para la comparacion de digitos adyacentes
    for pos in range(0, len(str(num)) - 1):
        if lista[pos + 1] > lista[pos]:
            decre = False
            break
    return decre


def bouncy_99():
    '''Devuelve el primer número (mínimo) para el cual
       la proporción de números bouncy es exactamente el 99%'''
    i = 1  # variable que determina el total de numeros analizados
    j = 0  # variable que determina la posición consecutiva del bouncy
    k = 0  # variable que determina la proporción
    # ciclo que se ejecuta hasta que se cumpla la condición
    while k != 0.99:
        if not creciente(i):
            if not decreciente(i):
                j += 1  # incremento del consecutivo del bouncy
                k = j / i  # calculo de la proporción
                # condición de cumplimiento
                if k == 0.99:
                    # imprime: numero mínimo y proporción
                    print("El numero mínimo es: " + str(i) +
                          " con una proporción del: " + str(k))
                    break  # interrupción del ciclo

        i += 1  # incremento del total de numeros analizados


# llamada a la función
bouncy_99()

