import heapq

direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def distancia_manhattan(pos_actual, pos_fin):
    return abs(pos_actual[0] - pos_fin[0]) + abs(pos_actual[1] - pos_fin[1])

class Mapa:
    def __init__(self, filas=4, columnas=6):
        self.filas = filas
        self.columnas = columnas
        self.matriz = self.crear_matriz()
        self.obstaculos = set()

    def crear_matriz(self):
        alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWX'
        matriz = []
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                fila.append(alfabeto[i * self.columnas + j])
            matriz.append(fila)
        return matriz

    def agregar_obstaculo(self, letra):
        self.obstaculos.add(letra)

    def quitar_obstaculo(self, letra):
        self.obstaculos.discard(letra)

    def es_accesible(self, fila, columna):
        return self.matriz[fila][columna] not in self.obstaculos

    def imprimir(self, camino=None, inicio=None, fin=None):
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[0])):
                letra = self.matriz[i][j]
                if (i, j) == inicio:
                    print('\033[1;32m' + letra + '\033[0m', end=' ')  # Verde para inicio
                elif (i, j) == fin:
                    print('\033[1;31m' + letra + '\033[0m', end=' ')  # Rojo para fin
                elif camino and (i, j) in camino:
                    print('\033[1;33m' + letra + '\033[0m', end=' ')  # Amarillo para camino
                elif letra in self.obstaculos:
                    print('\033[1;34m' + letra + '\033[0m', end=' ')  # Azul para obstáculos
                else:
                    print(letra, end=' ')
            print()

class CalculadoraRutas:
    def __init__(self, mapa):
        self.mapa = mapa

    def obtener_obstaculos(self):
        while True:
            obstaculos = input("\nIngrese las letras para los obstáculos (máximo 8): ").strip().upper()
            if len(obstaculos) <= 8 and all(letra.isalpha() for letra in obstaculos):
                for letra in obstaculos:
                    self.mapa.agregar_obstaculo(letra)
                break
            else:
                print("Entrada inválida. Ingrese hasta 8 letras del alfabeto en inglés.")

    def manejar_obstaculos(self):
        self.obtener_obstaculos()
        self.mapa.imprimir()
        while True:
            eliminar = input("\nDesea eliminar los obstáculos? Responde con S / N: ").strip().upper()
            if eliminar == 'S':
                obstaculos = input("\nIngrese las letras de los obstáculos que desea eliminar: ").strip().upper()
                for letra in obstaculos:
                    self.mapa.quitar_obstaculo(letra)
                self.mapa.imprimir()
                agregar = input("\nDesea añadir obstáculos? Responde con S / N: ").strip().upper()
                if agregar == 'S':
                    self.obtener_obstaculos()
                    self.mapa.imprimir()
                break
            elif eliminar == 'N':
                break
            else:
                print("Respuesta inválida. Responda con S o N.")

    def obtener_puntos_usuario(self):
        while True:
            self.mapa.imprimir()
            inicio = input("\nIngrese la letra de inicio: ").strip().upper()
            fin = input("Ingrese la letra de fin: ").strip().upper()
            if self.validar_entrada(inicio) & self.validar_entrada(fin) and inicio != fin:
                pos_inicio = self.encontrar_posicion(inicio)
                pos_fin = self.encontrar_posicion(fin)
                if pos_inicio and pos_fin:
                    return pos_inicio, pos_fin
                else:
                    print("Las letras ingresadas no fueron encontradas en la matriz. Intente de nuevo.")
            else:
                print("Entrada inválida. Ingrese una única letra del alfabeto en inglés.")

    def validar_entrada(self, letra):
        return len(letra) == 1 and letra.isalpha() and letra not in ('Y', 'Z')

    def encontrar_posicion(self, letra):
        for i in range(self.mapa.filas):
            for j in range(self.mapa.columnas):
                if self.mapa.matriz[i][j] == letra:
                    return (i, j)
        return None

    def encontrar_camino_A_estrella(self, inicio, fin):
        fila_inicio, col_inicio = inicio
        fila_fin, col_fin = fin

        nodos_visitados = set()
        nodos_por_visitar = []

        heapq.heappush(nodos_por_visitar, (0, inicio, None))

        costo_acumulado = {inicio: 0}
        padre = {inicio: None}

        while nodos_por_visitar:
            _, pos_actual, _ = heapq.heappop(nodos_por_visitar)

            if pos_actual in nodos_visitados:
                continue

            nodos_visitados.add(pos_actual)

            if pos_actual == fin:
                camino = []
                while pos_actual:
                    camino.append(pos_actual)
                    pos_actual = padre[pos_actual]
                camino.reverse()
                return camino

            for direccion in direcciones:
                fila_nueva = pos_actual[0] + direccion[0]
                col_nueva = pos_actual[1] + direccion[1]
                nueva_pos = (fila_nueva, col_nueva)

                if not (0 <= fila_nueva < self.mapa.filas and 0 <= col_nueva < self.mapa.columnas):
                    continue

                if self.mapa.matriz[fila_nueva][col_nueva] in self.mapa.obstaculos or nueva_pos in nodos_visitados:
                    continue

                costo_nuevo = costo_acumulado[pos_actual] + 1

                if nueva_pos not in costo_acumulado or costo_nuevo < costo_acumulado[nueva_pos]:
                    costo_acumulado[nueva_pos] = costo_nuevo
                    prioridad = costo_nuevo + distancia_manhattan(nueva_pos, fin)
                    heapq.heappush(nodos_por_visitar, (prioridad, nueva_pos, pos_actual))
                    padre[nueva_pos] = pos_actual

        return None

# Ejecución del programa
mapa = Mapa()
calculadora = CalculadoraRutas(mapa)

calculadora.manejar_obstaculos()
inicio, fin = calculadora.obtener_puntos_usuario()
camino = calculadora.encontrar_camino_A_estrella(inicio, fin)

if camino:
    print("\nMatriz 4x6 con camino resaltado y obstáculos:")
    mapa.imprimir(camino=camino, inicio=inicio, fin=fin)
else:
    print("No se encontró un camino válido.")