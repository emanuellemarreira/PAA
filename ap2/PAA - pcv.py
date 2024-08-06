#Aplicação do algoritmo guloso do Problema do Caixeiro Viajante para resgates

#O código implementa uma estrutura de grafo com vértices e arestas, onde cada vértice
#representa um ponto de resgate e cada aresta representa uma via (estrada) entre dois
#pontos. Ele calcula a menor rota entre esses pontos usando um algoritmo
#similar ao problema do caixeiro viajante (TSP - Traveling Salesman Problem).

import math
from collections import defaultdict

class Edge:
    def __init__(self, source, destination, condicao_via, distancia_entre_vertices, n_resgate):
        self.source = source
        self.destination = destination
        self.weight = condicao_via * distancia_entre_vertices + (1 / n_resgate)

class Vertex:
    def __init__(self, name, num, coordx, coordy, n_resgate):
        self.name = name
        self.num = num
        self.coordx = coordx
        self.coordy = coordy
        self.rescue = n_resgate

class Graph:
    def __init__(self):
        self.vertexes = []
        self.edges = []
        self.condicoes_via = [1, 10]  # 1 bom e 10 ruim

    def edge_exist(self, src, dest):
        for edge in self.edges:
            if edge.source == src and edge.destination == dest:
                return True
        return False

    def vertex_exist(self, name, cx, cy):
        for v in self.vertexes:
            if v.name == name or (v.coordx == cx and v.coordy == cy):
                return True
        return False

    def add_vertexes(self, v):
        for n in range(v):
            name = input("nome do ponto: ")
            coordx = int(input("coordenada x: "))
            coordy = int(input("coordenada y: "))
            while self.vertex_exist(name, coordx, coordy):
                print("o vertice ja existe, redefina")
                name = input("nome do ponto: ")
                coordx = int(input("coordenada x: "))
                coordy = int(input("coordenada y: "))
            n_resgate = float(input("numero de animais e pessoas para resgate: "))
            vertex = Vertex(name, n, coordx, coordy, n_resgate)
            self.vertexes.append(vertex)

    def return_vertex(self, name):
        for vertex in self.vertexes:
            if vertex.name == name:
                return vertex

    def add_edges(self, e):
        for i in range(e):
            src = self.return_vertex(input("ponto de origem: "))
            dest = self.return_vertex(input("ponto de destino: "))
            while dest == src:
                dest = self.return_vertex(input("ponto de destino não pode ser igual ao ponto de origem, insira outro: "))
            while self.edge_exist(src, dest):
                dest = self.return_vertex(input("a aresta já existe, insira outro destino: "))
            condicao_via = int(input("condicao da via: "))
            while condicao_via not in self.condicoes_via:
                condicao_via = int(input("insira condicao válida: "))
            edge1 = Edge(src, dest, condicao_via, distancia_entre_dois_pontos((src.coordx, src.coordy), (dest.coordx, dest.coordy)), src.rescue + dest.rescue)
            edge2 = Edge(dest, src, condicao_via, distancia_entre_dois_pontos((src.coordx, src.coordy), (dest.coordx, dest.coordy)), src.rescue + dest.rescue)
            self.edges.append(edge1)
            self.edges.append(edge2)

    def print_edges(self):
        for e in self.edges:
            print(e.source.name, " -> ", e.destination.name, " (", e.weight, ") ")

    def get_adjacency_matrix(self):
        n = len(self.vertexes)
        matrix = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append(float('inf'))
            matrix.append(row)
        for edge in self.edges:
            matrix[edge.source.num][edge.destination.num] = edge.weight
        return matrix

def distancia_entre_dois_pontos(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def find_min_route(graph):
    tsp = graph.get_adjacency_matrix()
    n = len(tsp)
    sum = 0
    counter = 0
    j = 0
    i = 0
    min_weight = float('inf')
    visited_route_list = defaultdict(int)

    visited_route_list[0] = 1
    route = [0] * n
    route_list = [0]

    while i < n and j < n:
        if counter >= n - 1:
            break

        if j != i and (visited_route_list[j] == 0):
            if tsp[i][j] < min_weight:
                min_weight = tsp[i][j]
                route[counter] = j + 1

        j += 1

        if j == n:
            sum += min_weight
            min_weight = float('inf')
            visited_route_list[route[counter] - 1] = 1
            route_list.append(route[counter] - 1)
            j = 0
            i = route[counter] - 1
            counter += 1

    i = route[counter - 1] - 1

    for j in range(n):
        if (i != j) and tsp[i][j] < min_weight:
            min_weight = tsp[i][j]
            route[counter] = j + 1

    sum += min_weight
    route_list.append(route_list[0])

    print("Custo minimo eh :", sum)
    
    route_names = []
    for i in route_list:
        vertex_name = graph.vertexes[i].name
        route_names.append(vertex_name)
    print("Melhor rota é:", route_names)

def build_graph():
    v = int(input("numero de pontos de resgate: "))
    e = int(input("numero máximo de vias entre os pontos de resgate: "))
    print("===definições dos pontos de resgate===")
    g = Graph()
    g.add_vertexes(v)
    print("===definições das vias===")
    g.add_edges(e)
    return g

if __name__ == '__main__':
    g = build_graph()
    g.print_edges()
    find_min_route(g)
