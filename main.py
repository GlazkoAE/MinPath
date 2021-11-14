from collections import defaultdict
from math import inf


def find_all_paths(matrix, n):
    # Замена всех нулевых элементов бесконечностью
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 0:
                matrix[i][j] = inf

    # Алгоритм Дейкстры
    valid = [True] * n
    length = [inf] * n
    length[0] = 0
    for _ in range(n):
        min_length = inf
        index = -1
        for i in range(n):
            if valid[i] and length[i] < min_length:
                min_length = length[i]
                index = i
        for i in range(n):
            if length[index] + matrix[index][i] < length[i]:
                length[i] = length[index] + matrix[index][i]
        valid[index] = False
    return length


def full_path_calculate(path):

    global min_path

    path_length = sum([matrix[i][j] for i, j in path[1:]])
    path_length += back_paths[path[-1][1]]

    if path_length < min_path:
        min_path = path_length


def min_path_calculate(current_vertex=0, prev_vertex=None, path=None):

    # Path - list, состоящий из ребер в виде кортежей
    # Хранит в себе путь от первой вершины до текущей
    if path is None:
        path = []
    path.append((prev_vertex, current_vertex))

    # Ограничение количества вершин в пути (n + макс. число повторов):
    # чем больше, тем точнее и сложнее метод (ближе к полному перебору)
    if len(path) <= n+3:
        # Проверка условия посещения всех вершин графа
        if len(set([to for prev_vertex, to in path])) == n:
            full_path_calculate(path)
        else:
            for next_vertex in graph[current_vertex]:
                if (current_vertex, next_vertex) not in path:
                    min_path_calculate(next_vertex, current_vertex, path)

    path.remove((prev_vertex, current_vertex))


n = int(input())

matrix = [[0] * n for _ in range(n)]
for i in range(n):
    matrix[i] = [int(j) for j in input().strip().split(" ")]

# Граф связей из матрицы расстояний
graph = defaultdict(list)
for i in range(n):
    row = matrix[i].copy()
    row = list(filter(lambda x: x != 0, row))
    for j in range(n):
        if matrix[i][j] != 0:
            graph[i].append(j)
    # Сортировка каждой строки graph для того, чтобы
    # при выборе пути приоритет был у ребер с меньшей длиной
    graph[i] = [item for _, item in sorted(zip(row, graph[i]))]

# Длины путей от всех вершин до первой
back_paths = find_all_paths(matrix, n)

# Рекурсивный обход графа методом ближайшего соседа и
# вычисление длины пути с учетом возврата в исходную точку
min_path = inf
min_path_calculate()

print(min_path)
