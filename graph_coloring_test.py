import webcolors


def greedy_coloring(graph):
    colors = {}  # Dictionary to store the colors assigned to each vertex

    available_colors = list(webcolors.names_to_hex(spec="css3").keys())

    for vertex in graph:
        neighbors = [
            colors[neighbor] for neighbor in graph[vertex] if neighbor in colors
        ]  # Creazting neighbor using list through iteration

        # Finding the first available color
        color_available = None
        for color_name in available_colors:
            if color_name not in neighbors:
                color_available = color_name
                break

        colors[vertex] = color_available

    return colors


# Example usage with random color names in case of confilcts
graph = {"A": ["B", "C"], "B": ["A", "C", "D"], "C": ["A", "B", "D"], "D": ["B", "C"]}

result = greedy_coloring(graph)

for vertex, color in result.items():
    print(f"Vertex {vertex} is colored with the color {color}")
