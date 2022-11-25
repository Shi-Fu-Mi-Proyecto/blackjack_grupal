#IMPORTACIONES
import random


#VARIABLES
SI = ("s", "si", "y", "yes", "1")

cartas = { 
    chr(0x1f0a1): 11, 
    chr(0x1f0a2): 2, 
    chr(0x1f0a3): 3, 
    chr(0x1f0a4): 4, 
    chr(0x1f0a5): 5, 
    chr(0x1f0a6): 6, 
    chr(0x1f0a7): 7, 
    chr(0x1f0a8): 8, 
    chr(0x1f0a9): 9, 
    chr(0x1f0aa): 10, 
    chr(0x1f0ab): 10, 
    chr(0x1f0ad): 10, 
    chr(0x1f0ae): 10, 
} 




lista_cartas = list(cartas.keys())

J = [] #lista vacía con las cartas del jugador
C = [] #lista vacía con las cartas del croupier


#FUNCIONES
def pedir_entrada_si_o_no(mensaje):
    try:
        entrada = input(mensaje).lower()
        if entrada in SI:
            return True
    except:
        return False


def valor_carta(carta):
    return cartas[carta] # devuelve el valor asociado a la carta

def puntuacion_cartas(lista):
    return sum( [valor_carta(lista_cartas[c]) for c in lista] )


def comprobar_ganador(J,C):
    if puntuacion_cartas(J) > puntuacion_cartas(C): #el jugador tiene mayor puntuación que el croupier
        if puntuacion_cartas(J) <= 21:
            print("Tienes más puntos que el croupier. HAS GANADO")
        
    elif puntuacion_cartas(J) < puntuacion_cartas(C): #el croupier tiene mayor puntuación que el jugador
        if puntuacion_cartas(C) <= 21: #y su puntuación es <= 21
            print("El croupier tiene más puntos. HAS PERDIDO")
        else: #si el croupier se pasa de 21, el jugador gana
            print("El croupier se ha pasado. HAS GANADO")
    
    elif puntuacion_cartas(J) == puntuacion_cartas(C):
        print('Tenéis los mismos puntos. EMPATE')


def repartir_carta_disponible(lista):
    '''
    Esta funcion devuelve una carta aleatoria que no este en la lista dada
    -INPUT -------------
    lista : list
        lista de indices de cartas ya repartidas
    -OUTPUT ------------
    carta : int
        indice de la carta elegida al azar
    '''
    while True: #bucle para asegurarnos de que la carta no está en la lista
        carta = random.randint(0, len(lista_cartas)-1) #cogemos el índice de una carta al azar
        if carta not in lista: #comprobamos que no está en la lista
            return carta #si es así, nos la quedamos


def repartir_dos_cartas_al_jugador():
    '''
    Esta funcion devuelve una lista de dos cartas aleatorias
    -INPUT -------------
    -OUTPUT ------------
    ( c1, c2 ) : list
        c1 : int
            indice de la carta1 en la coleccion
        c2 : int
            indice de la carta2 en la coleccion
    '''
    seleccion = [] #lista vacía en la que vamos a meter las cartas seleccionadas al azar
    carta1 = random.randint(0, len(lista_cartas)-1) 
        #elegir al azar uno de los indices de la coleccion de cartas
        #randint(a,b) es un numero aleatorio N tq a <= N <= b
    seleccion.append(carta1) #la añadimos a la lista de cartas seleccionadas

    #carta2 tiene que ser distinta de carta1
    carta2 = repartir_carta_disponible(seleccion) 
    seleccion.append(carta2) #añadimos la carta2 a la lista de cartas seleccionadas
    
    return seleccion #lista con los indices de las dos cartas que han tocado


def repartir_dos_cartas_al_croupier(J):
    '''
    Esta funcion devuelve una lista de dos cartas aleatorias para el croupier
    -INPUT -------------
    J : list
        lista de indices de cartas que ya se le han repartido al jugador
    -OUTPUT ------------
    ( c1, c2 ) : list
        c1 : int
            indice de la carta1 en la coleccion
        c2 : int
            indice de la carta2 en la coleccion
    '''
    seleccion = []
    cartas_no_disponibles = [] #lista donde vamos a meter las cartas que ya se han repartido
    cartas_no_disponibles.extend(J) #las cartas ya repartidas al jugador no están disponibles

    #se reparte la 1º cartas
    carta1 = repartir_carta_disponible(cartas_no_disponibles)
    seleccion.append(carta1)
    cartas_no_disponibles.append(carta1) #añadimos carta1 a la lista de cartas que ya se han repartido

    #se reparte la 2º carta
    carta2 = repartir_carta_disponible(cartas_no_disponibles)
    seleccion.append(carta2)

    return seleccion


def repartir_una_carta_mas(J, C):
    '''
    Esta funcion devuelve una carta aleatoria 
    teniendo en cuenta todas las que ya se han repartido
    -INPUT -------------
    J : list
        lista de indices de cartas que ya se le han repartido al jugador
    C : list
        lista de indices de cartas que ya se le han repartido al croupier
    -OUTPUT ------------
    carta : int
        indice de la carta elegida al azar
    '''
    #las cartas que ya se han repartido son las que tienen el jugador y el croupier
    cartas_no_disponibles = J + C

    return repartir_carta_disponible(cartas_no_disponibles)


def mostrar_cartas(lista):
    '''
    Esta funcion muestra las cartas (gráficas), dado una lista de indices de cartas
    -INPUT -------------
    lista : list
        lista de indices de cartas
    -OUTPUT ------------
    lista de cartas (gráficas)
    '''
    return [lista_cartas[c] for c in lista]



def accion_croupier(J, C):
    '''
    Esta funcion modeliza las acciones del croupier según las reglas del juego
    -INPUT -------------
    J : list
        lista de cartas del jugador
    C : list
        lista de cartas del croupier
    -OUTPUT ------------
    cartas del croupier actualizadas
    '''
    #si el croupier tiene 16 o menos, se le reparte una carta
    if puntuacion_cartas(C) >= 17:
        print('El croupier se planta.')
    else:
        C.append( repartir_una_carta_mas(J,C) )
        print('El croupier saca otra carta. Las cartas del croupier ahora son:', mostrar_cartas(C), '. Su puntuación es:', puntuacion_cartas(C))



def jugar():
    #se reparten dos cartas visibles al jugador
    global J
    J.extend( repartir_dos_cartas_al_jugador() ) #añadimos las dos cartas repartidas al azar a la lista de cartas del jugador
    print('Tus cartas son: ', mostrar_cartas(J), '. Tu puntuación es: ', puntuacion_cartas(J))
    
    #se reparten dos cartas al croupier
    global C
    C.extend( repartir_dos_cartas_al_croupier(J) ) #añadimos las dos cartas repartidas al azar a la lista de cartas del croupier
    print('Las cartas del croupier son: ', mostrar_cartas(C), '. Su puntuación es: ', puntuacion_cartas(C))

    #TURNO JUGADOR -----------------------------------------------------------------------------------
    #se pregunta al jugador si quiere otra carta, siempre que su puntuacion no pase de 21
    
    while pedir_entrada_si_o_no('¿Quieres otra carta? (s/n): ') == True: #mientras el jugador quiera otra carta
        J.append( repartir_una_carta_mas(J,C) ) #se le reparte una carta al azar
        print('Tus cartas ahora son: ', mostrar_cartas(J), '. Tu puntuación es: ', puntuacion_cartas(J))
        
        if puntuacion_cartas(J)<=21: #si su puntuacion no pasa de 21
            continue #volvemos a preguntar al jugador

        else: #si pt >21
            print('Te has pasado de 21. HAS PERDIDO')
            return #se sale de la función jugar()
            
    #cuando no quiera otra carta, y su puntuacion sea <=21, continuamos
    print('Te plantas con', puntuacion_cartas(J), 'puntos.')
    
    #TURNO CROUPIER -----------------------------------------------------------------------------------
    #el croupier debe sacar cartas siempre que su puntuacion sea <=16
    while puntuacion_cartas(C) < 17:
        accion_croupier(J, C)

    #COMPROBAR GANADOR
    comprobar_ganador(J, C)


def jugar_blackjack():
    global J
    global C
    print('Bienvenido al juego del Blackjack, el objetivo es conseguir una puntuación de 21 o lo más cercana posible.')
    print("Valor de cada carta: ")
    for carta in sorted(cartas.keys()):
        print("La carta {} vale {}".format(carta, cartas[carta]))
        
    jugar()
    while pedir_entrada_si_o_no('¿Quieres jugar otra partida? (s/n): ') == True:
        J=[]
        C=[]
        jugar()
    #si no quiere jugar otra partida, se sale del programa
    print('¡Hasta la próxima!')
