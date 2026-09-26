import math
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import heapq
import time


def count_edges_and_nodes():
    f = open("skopie_network.graphml")
    d = f.read()
    print(d.count("</node>"))
    print(d.count("</edge>"))

def haversine(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """Вычисляет расстояние между двумя точками на поверхности Земли (в километрах)."""
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    R = 6371  # Радиус Земли в км

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def dijkstra(
    graph: Dict[Tuple[float, float], List[Tuple[Tuple[float, float], float]]],
    start: Tuple[float, float],
    end: Tuple[float, float],
) -> Tuple[List[Tuple[float, float]], float, List[str]]:
    distances = {point: float("inf") for point in graph}
    distances[start] = 0

    path = {start: None}

    queue = [(0, start)]

    visited = set()

    while len(queue) > 0:
        curr_dist, curr_place = heapq.heappop(queue)

        if curr_place in visited:
            continue
        visited.add(curr_place)

        if curr_place == end:
            break

        for neighbor, dist in graph[curr_place]:
            if neighbor in visited:
                continue

            new_dist = curr_dist + dist

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                path[neighbor] = curr_place
                heapq.heappush(queue, (new_dist, neighbor))

    if not end in distances:
        return [], float("inf"), []

    res_path = []

    res_dist = distances[end]

    while end != start:
        res_path.append(end)
        end = path[end]

    res_path = res_path[::-1]

    return res_path, res_dist, []


def build_graph(
    edges: List[Tuple[Tuple[float, float], Tuple[float, float], str]]
) -> Dict[Tuple[float, float], List[Tuple[Tuple[float, float], float]]]:
    """Строит граф из рёбер."""
    graph = {}
    for start, end, _ in edges:
        dist = haversine(start, end)
        graph.setdefault(start, []).append((end, dist))
        graph.setdefault(end, []).append(
            (start, dist)
        )  # если граф неориентированный
    return graph


def read_graphml(
    file_path: str,
) -> Tuple[
    Dict[str, Tuple[float, float]],
    List[Tuple[Tuple[float, float], Tuple[float, float], str]],
]:
    """Читает GraphML файл и возвращает узлы и ребра с названиями улиц.

    Args:
        file_path: путь к файлу .graphml

    Returns:
        Кортеж (nodes, edges), где:
        - nodes: словарь {node_id: (x, y)}
        - edges: список [((x1, y1), (x2, y2), название_улицы), ...]
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {"g": "http://graphml.graphdrawing.org/xmlns"}

    nodes = {}
    for node in root.findall(".//g:node", ns):
        node_id = node.get("id")
        x, y = None, None
        for data in node.findall(".//g:data", ns):
            if data.get("key") == "d4":  # x координата (обычно longitude)
                x = float(data.text)
            elif data.get("key") == "d5":  # y координата (обычно latitude)
                y = float(data.text)
        if x is not None and y is not None:
            nodes[node_id] = (x, y)

    edges = []
    for edge in root.findall(".//g:edge", ns):
        source = edge.get("source")
        target = edge.get("target")
        street_name = None
        for data in edge.findall(".//g:data", ns):
            if data.get("key") == "d11":  # название улицы
                street_name = data.text if data.text else None
        if source in nodes and target in nodes:
            edges.append((nodes[source], nodes[target], street_name))

    return nodes, edges


def find_street_index(
    edges: List[Tuple[Tuple[float, float], Tuple[float, float], str]],
    street_name_query: str,
) -> Tuple[int, str]:
    """Возвращает индекс (номер) и название улицы по заданному имени.

    Args:
        edges: список рёбер с названиями улиц
        street_name_query: название улицы для поиска

    Returns:
        Кортеж (индекс, название_улицы), если найдено, иначе (-1, None)
    """
    for i, (_, _, name) in enumerate(edges):
        if name and name.lower() == street_name_query.lower():
            return i, name
    return -1, None


def visualize_path_with_network(
    nodes, edges, path, street_names=None, figsize=(20, 20)
):
    """Визуализация всей дорожной сети + маршрута красным.

    Если передан список street_names, то названия улиц выводятся вдоль
    маршрута.
    """
    plt.figure(figsize=figsize)
    ax = plt.gca()

    # Все рёбра — серые
    all_lines = [(start, end) for start, end, _ in edges]
    lc = LineCollection(all_lines, linewidths=0.3, colors="gray", alpha=0.4)
    ax.add_collection(lc)

    # Путь — красный
    if path and len(path) > 1:
        path_lines = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        lc_path = LineCollection(
            path_lines, linewidths=2.0, colors="red", alpha=0.9
        )
        ax.add_collection(lc_path)

    # Отображаем названия улиц, если они заданы
    if street_names:
        for i in range(len(path) - 1):
            mid_point = (
                (path[i][0] + path[i + 1][0]) / 2,
                (path[i][1] + path[i + 1][1]) / 2,
            )
            if i < len(street_names) and street_names[i]:
                plt.text(
                    mid_point[0],
                    mid_point[1],
                    street_names[i],
                    fontsize=8,
                    color="blue",
                    ha="center",
                )

    ax.autoscale()
    plt.axis("equal")
    plt.title("Кратчайший маршрут")
    plt.xlabel("Долгота")
    plt.ylabel("Широта")
    plt.grid(False)
    plt.tight_layout()
    plt.show()


def save_visualization(filename: str, dpi: int = 300) -> None:
    """Сохраняет текущую визуализацию в файл.

    Args:
        filename: имя файла для сохранения
        dpi: разрешение изображения
    """
    plt.savefig(filename, dpi=dpi, bbox_inches="tight")
    plt.close()


def visualize_only_path(path, figsize=(10, 10)):
    """Визуализирует только маршрут (без остального графа)."""
    if not path or len(path) < 2:
        print("Маршрут слишком короткий или отсутствует.")
        return

    plt.figure(figsize=figsize)
    ax = plt.gca()

    path_lines = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    lc_path = LineCollection(
        path_lines, linewidths=2.5, colors="red", alpha=0.9
    )
    ax.add_collection(lc_path)

    ax.autoscale()
    plt.axis("equal")
    plt.title("Кратчайший маршрут")
    plt.xlabel("Долгота")
    plt.ylabel("Широта")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Пример использования
if __name__ == "__main__":
    # 1. Загрузка данных
    nodes, edges = read_graphml("skopie_network.graphml")

    # 2. Задаём названия улиц для начала и конца маршрута
    start_street_query = "Александар Урдаревски"  # Название улицы для старта (пример)
    end_street_query = (
        "Божидар Видоески"  # Название улицы для финиша (пример)
    )

    # 3. Используем find_street_index для определения нужных рёбер
    start_index, start_street = find_street_index(edges, start_street_query)
    end_index, end_street = find_street_index(edges, end_street_query)

    if start_index == -1 or end_index == -1:
        print("Не удалось найти заданную улицу для начала или конца маршрута")
    else:
        # 4. Определяем стартовый и конечный узлы:
        # Используем первую точку ребра для старта и вторую точку ребра для финиша.
        start_node = edges[start_index][0]
        end_node = edges[end_index][1]

        # 5. Строим граф и ищем кратчайший путь
        
        graph = build_graph(edges)
        time_start = time.time()
        path, distance, street_names = dijkstra(graph, start_node, end_node)
        print(f"Время вычисления: {time.time() - time_start}")

        if not path:
            print("Путь не найден")
        else:
            print(f"Найден путь длиной {distance:.2f} км")
            print("Улицы на пути:", ", ".join(filter(None, street_names)))

        # 6. Визуализация маршрута
        visualize_path_with_network(nodes, edges, path, street_names)
