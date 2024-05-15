#Hoja de Trabajo 10
#Algoritmos y Estructuras de Datos
#Integrantes:  Nina Nájera - 231088, Mishell Ciprian - 231169


class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.adj_matrix = [[float('inf')] * num_vertices for _ in range(num_vertices)]
        self.next_matrix = [[None] * num_vertices for _ in range(num_vertices)]
        for i in range(num_vertices):
            self.adj_matrix[i][i] = 0

    def add_edge(self, u, v, weight):
        self.adj_matrix[u][v] = weight
        self.next_matrix[u][v] = v

    def floyd_warshall(self):
        dist = list(map(lambda i: list(map(lambda j: j, i)), self.adj_matrix))
        for k in range(self.num_vertices):
            for i in range(self.num_vertices):
                for j in range(self.num_vertices):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        self.next_matrix[i][j] = self.next_matrix[i][k]
        self.adj_matrix = dist

    def get_path(self, u, v):
        if self.next_matrix[u][v] is None:
            return []
        path = [u]
        while u != v:
            u = self.next_matrix[u][v]
            path.append(u)
        return path

    def get_center(self):
        max_distances = [max(row) for row in self.adj_matrix]
        return max_distances.index(min(max_distances))

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

def main():
    graph, cities, edges = read_graph('logistica.txt')
    graph.floyd_warshall()

    city_names = {index: name for name, index in cities.items()}

    while True:
        print("Opciones:")
        print("1. Consultar ruta más corta entre dos ciudades")
        print("2. Consultar la ciudad en el centro del grafo")
        print("3. Modificar el grafo")
        print("4. Salir")

        choice = int(input("Seleccione una opción: "))

        if choice == 1:
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
            center = graph.get_center()
            print("La ciudad en el centro del grafo es:", city_names[center])

        elif choice == 3:
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
            break

        else:
            print("Error, intente nuevamente.")

if __name__ == "__main__":
    main()