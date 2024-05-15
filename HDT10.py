#Hoja de Trabajo 10
#Algoritmos y Estructuras de Datos
#Integrantes:  Nina Nájera - 231088, Mishell Ciprian - 231169


# Definición de la clase Graph que representa un grafo y sus operaciones
class Graph:
    def __init__(self, num_vertices):
        # Constructor que inicializa la matriz de adyacencia y la matriz de siguiente nodo
        self.num_vertices = num_vertices
        self.adj_matrix = [[float('inf')] * num_vertices for _ in range(num_vertices)]
        self.next_matrix = [[None] * num_vertices for _ in range(num_vertices)]
        # Inicialización de la diagonal de la matriz de adyacencia con ceros
        for i in range(num_vertices):
            self.adj_matrix[i][i] = 0

    # Método para añadir una arista con su respectivo peso al grafo
    def add_edge(self, u, v, weight):
        self.adj_matrix[u][v] = weight
        self.next_matrix[u][v] = v

    # Algoritmo de Floyd-Warshall para encontrar los caminos más cortos
    def floyd_warshall(self):
        dist = list(map(lambda i: list(map(lambda j: j, i)), self.adj_matrix))
        for k in range(self.num_vertices):
            for i in range(self.num_vertices):
                for j in range(self.num_vertices):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        self.next_matrix[i][j] = self.next_matrix[i][k]
        self.adj_matrix = dist

    # Método para obtener el camino más corto entre dos nodos
    def get_path(self, u, v):
        if self.next_matrix[u][v] is None:
            return []
        path = [u]
        while u != v:
            u = self.next_matrix[u][v]
            path.append(u)
        return path

    # Método para obtener el centro del grafo
    def get_center(self):
        max_distances = [max(row) for row in self.adj_matrix]
        return max_distances.index(min(max_distances))

# Función para leer el grafo desde un archivo
def read_graph(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    cities = {}
    index = 0
    edges = []

    for line in lines:
        parts = line.strip().split()
        city1, city2 = parts[0], parts[1]
        times = list(map(int, parts[2:6]))

        if city1 not in cities:
            cities[city1] = index
            index += 1
        if city2 not in cities:
            cities[city2] = index
            index += 1

        edges.append((cities[city1], cities[city2], times))

    num_vertices = len(cities)
    graph = Graph(num_vertices)

    for u, v, times in edges:
        graph.add_edge(u, v, times[0])  

    return graph, cities, edges

# Función principal del programa
def main():
    # Lectura del grafo desde un archivo
    graph, cities, edges = read_graph('logistica.txt')
    # Ejecución del algoritmo de Floyd-Warshall para encontrar los caminos más cortos
    graph.floyd_warshall()

    # Creación de un diccionario para mapear los índices de los nodos a los nombres de las ciudades
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
            # Opción para modificar el grafo
            print("Modificar el grafo:")
            print("a. Interrupción de tráfico entre ciudades")
            print("b. Nueva conexión entre ciudades")
            print("c. Actualizar clima entre ciudades")

            mod_choice = input("Seleccione una opción: ")

            if mod_choice == 'a':
                # Opción para interrumpir el tráfico entre ciudades
                city1 = input("Ingrese ciudad origen: ")
                city2 = input("Ingrese ciudad destino: ")
                if city1 in cities and city2 in cities:
                    graph.add_edge(cities[city1], cities[city2], float('inf'))
                    graph.floyd_warshall()
                    print("Interrupción añadida y rutas recalculadas.")
                else:
                    print("Ciudad no encontrada.")

            elif mod_choice == 'b':
                # Opción para añadir una nueva conexión entre ciudades
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
                # Opción para actualizar el clima entre ciudades
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
                                graph.add_edge(cities[city1], cities[city2], edge
