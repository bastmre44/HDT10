#Hoja de Trabajo 10
#Algoritmos y Estructuras de Datos
#Integrantes:  Nina Nájera - 231088, Mishell Ciprian - 231169


# Definición de la clase Graph para representar un grafo y realizar operaciones sobre él
class Graph:
    def __init__(self, num_vertices):
        # Constructor de la clase Graph para inicializar el grafo con el número de vértices especificado
        self.num_vertices = num_vertices
        # Inicialización de la matriz de adyacencia con infinito para todas las aristas
        self.adj_matrix = [[float('inf')] * num_vertices for _ in range(num_vertices)]
        # Inicialización de la matriz next_matrix para almacenar los siguientes vértices en el camino más corto
        self.next_matrix = [[None] * num_vertices for _ in range(num_vertices)]
        # Establecimiento de la distancia de un vértice a sí mismo como 0 en la matriz de adyacencia
        for i in range(num_vertices):
            self.adj_matrix[i][i] = 0

    # Método para agregar una arista al grafo con su respectivo peso
    def add_edge(self, u, v, weight):
        self.adj_matrix[u][v] = weight
        self.next_matrix[u][v] = v

    # Algoritmo de Floyd-Warshall para encontrar los caminos más cortos entre todos los pares de vértices
    def floyd_warshall(self):
        dist = list(map(lambda i: list(map(lambda j: j, i)), self.adj_matrix))
        for k in range(self.num_vertices):
            for i in range(self.num_vertices):
                for j in range(self.num_vertices):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        self.next_matrix[i][j] = self.next_matrix[i][k]
        self.adj_matrix = dist

    # Método para obtener el camino más corto entre dos vértices dados
    def get_path(self, u, v):
        if self.next_matrix[u][v] is None:
            return []
        path = [u]
        while u != v:
            u = self.next_matrix[u][v]
            path.append(u)
        return path

    # Método para obtener el vértice que está en el centro del grafo
    def get_center(self):
        max_distances = [max(row) for row in self.adj_matrix]
        return max_distances.index(min(max_distances))

# Función para leer un grafo desde un archivo de texto
def read_graph(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    cities = {}
    index = 0
    edges = []

    # Procesamiento de cada línea del archivo
    for line in lines:
        parts = line.strip().split()
        city1, city2 = parts[0], parts[1]
        times = list(map(int, parts[2:6]))

        # Verificación de existencia de las ciudades en el diccionario 'cities'
        if city1 not in cities:
            cities[city1] = index
            index += 1
        if city2 not in cities:
            cities[city2] = index
            index += 1

        # Añadiendo la información de las aristas al grafo
        edges.append((cities[city1], cities[city2], times))

    num_vertices = len(cities)
    graph = Graph(num_vertices)

    for u, v, times in edges:
        graph.add_edge(u, v, times[0])  

    return graph, cities, edges

# Función principal del programa
def main():
    # Lectura del grafo desde un archivo de texto
    graph, cities, edges = read_graph('logistica.txt')
    # Aplicación del algoritmo de Floyd-Warshall para encontrar los caminos más cortos
    graph.floyd_warshall()

    # Diccionario para mapear los índices de los vértices a los nombres de las ciudades
    city_names = {index: name for name, index in cities.items()}

    while True:
        print("Opciones:")
        print("1. Consultar ruta más corta entre dos ciudades")
        print("2. Consultar la ciudad en el centro del grafo")
        print("3. Modificar el grafo")
        print("4. Salir")

        choice = int(input("Seleccione una opción: "))

        if choice == 1:
            # Opción para consultar la ruta más corta entre dos ciudades
            city1 = input("Ingrese ciudad origen: ")
            city2 = input("Ingrese ciudad destino: ")
            if city1 in cities and city2 in cities:
                path = graph.get_path(cities[city1], cities[city2])
                if path:
                    print("Ruta más corta:", " -> ".join(city_names[p] for p in path))
                    print("Distancia:", graph.adj_matrix[cities[city1]][cities[city2]])
                else:
                    print("No hay ruta entre las ciudades.")
            else:
                print("Ciudad no encontrada.")

        elif choice == 2:
            # Opción para consultar la ciudad en el centro del grafo
            center = graph.get_center()
            print("La ciudad en el centro del grafo es:", city_names[center])

        elif choice == 3:
            # Opción para modificar el grafo (interrupción de tráfico, nueva conexión, actualizar clima)
            print("Modificar el grafo:")
            print("a. Interrupción de tráfico entre ciudades")
            print("b. Nueva conexión entre ciudades")
            print("c. Actualizar clima entre ciudades")

            mod_choice = input("Seleccione una opción: ")

            if mod_choice == 'a':
                city1 = input("Ingrese ciudad origen: ")
                city2 = input("Ingrese ciudad destino: ")
                if city1 in cities and city2 in cities:
                    graph.add_edge(cities[city1], cities[city2], float('inf'))
                    graph.floyd_warshall()
                    print("Interrupción añadida y rutas recalculadas.")
                else:
                    print("Ciudad no encontrada.")

            elif mod_choice == 'b':
                city1 = input("Ingrese ciudad origen: ")
                city2 = input("Ingrese ciudad destino: ")
                normal_time = int(input("Ingrese tiempo con clima normal: "))
                if city1 in cities and city2 in cities:
                    graph.add_edge(cities[city1], cities[city2], normal_time)
                    graph.floyd_warshall()
                    print("Conexión añadida y rutas recalculadas.")
                else:
                    print("Ciudad no encontrada.")

            elif mod_choice == 'c':
                city1 = input("Ingrese ciudad origen: ")
                city2 = input("Ingrese ciudad destino: ")
                condition = input("Ingrese condición climática (normal, lluvia, nieve, tormenta): ")
                if city1 in cities and city2 in cities:
                    for edge in edges:
                        if edge[0] == cities[city1] and edge[1] == cities[city2]:
                            if condition == 'normal':
                                graph.add_edge(cities[city1], cities[city2], edge[2][0])
                            elif condition == 'lluvia':
                                graph.add_edge(cities[city1], cities[city2], edge[2][1])
                            elif condition == 'nieve':
                                graph.add_edge(cities[city1], cities[city2], edge[2][2])
                            elif condition == 'tormenta':
                                graph.add_edge(cities[city1], cities[city2], edge[2][3])
                            graph.floyd_warshall()
                            print("Clima actualizado y rutas recalculadas.")
                            break
                else:
                    print("No se encontró la ciudad que busca.")

        elif choice == 4:
            # Opción para salir del programa
            break

        else:
            print("Error, intente nuevamente.")

if __name__ == "__main__":
    main()
