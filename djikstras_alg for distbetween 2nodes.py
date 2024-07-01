import sys
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
def dijkstra(graph, source):
    unvisited = set(graph.nodes())
    distance = {node: sys.maxsize for node in unvisited}
    distance[source] = 0
    parent = {}
    while unvisited:
        current_node = min(unvisited, key=lambda node: distance[node])
        unvisited.remove(current_node)
        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor].get('weight', 0)  
            if distance[current_node] + weight < distance[neighbor]:
                distance[neighbor] = distance[current_node] + weight
                parent[neighbor] = current_node
    return distance, parent
def visualize_path():
    source_node = source_node_combobox.get()
    destination_node = destination_node_combobox.get()
    shortest_distances, parents = dijkstra(G, source_node)
    shortest_path = [destination_node]
    current_node = destination_node
    while current_node != source_node:
        current_node = parents[current_node]
        shortest_path.insert(0, current_node)
    shortest_path_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
    color = next(color_generator)
    all_paths.append((shortest_path_edges, color))  # Assign a unique color for this path
    update_graph_visualization()
def add_node_to_graph():
    new_node = new_node_entry.get()
    if new_node not in G.nodes():
        G.add_node(new_node)
        update_node_comboboxes()
        update_graph_visualization()
    else:
        print("Node already exists in the graph.")
def add_connection_to_graph():
    node_a = connection_node_a_combobox.get()
    node_b = connection_node_b_combobox.get()
    weight = connection_weight_entry.get()
    if node_a in G.nodes() and node_b in G.nodes() and weight:
        G.add_edge(node_a, node_b, weight=int(weight))
        update_graph_visualization()  # Update graph visualization after adding a connection
    else:
        print("Invalid input. Please check the node names and ensure a weight is provided.")
def update_graph_visualization():
    pos = nx.spring_layout(G)
    plt.clf()  
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=10)
    edge_labels = {(node, neighbor): G[node][neighbor].get('weight', '') for node, neighbor in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    for path_edges, color in all_paths:
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color=color, width=2)
    plt.title("Graph Visualization")
    plt.pause(0.1)
    plt.show()
def update_node_comboboxes():
    node_values = list(G.nodes())
    source_node_combobox['values'] = node_values
    destination_node_combobox['values'] = node_values
    connection_node_a_combobox['values'] = node_values
    connection_node_b_combobox['values'] = node_values
app = tk.Tk()
app.title("Shortest Path Visualization")
G = nx.Graph()
all_paths = []
new_node_label = tk.Label(app, text="Add New Node:")
new_node_label.pack()
new_node_entry = tk.Entry(app)
new_node_entry.pack()
add_node_button = tk.Button(app, text="Add Node to Graph", command=add_node_to_graph)
add_node_button.pack()
connection_label = tk.Label(app, text="Add Connection (e.g., 'A B'):")
connection_label.pack()
connection_frame = tk.Frame(app)
connection_frame.pack()
connection_node_a_combobox = ttk.Combobox(connection_frame, values=[], state="readonly")
connection_node_a_combobox.grid(row=0, column=0)
connection_node_b_combobox = ttk.Combobox(connection_frame, values=[], state="readonly")
connection_node_b_combobox.grid(row=0, column=1)
connection_weight_label = tk.Label(connection_frame, text="Weight:")
connection_weight_label.grid(row=0, column=2)
connection_weight_entry = tk.Entry(connection_frame, state=tk.NORMAL)
connection_weight_entry.grid(row=0, column=3)
add_connection_button = tk.Button(connection_frame, text="Add Connection", command=add_connection_to_graph)
add_connection_button.grid(row=0, column=4)
source_node_label = tk.Label(app, text="Source Node:")
source_node_label.pack()
source_node_combobox = ttk.Combobox(app, values=[], state="readonly")
source_node_combobox.pack()
destination_node_label = tk.Label(app, text="Destination Node:")
destination_node_label.pack()
destination_node_combobox = ttk.Combobox(app, values=[], state="readonly")
destination_node_combobox.pack()
add_shortest_path_button = tk.Button(app, text="Add Shortest Path", command=visualize_path)
add_shortest_path_button.pack()
color_generator = iter(['red', 'blue', 'green', 'purple', 'orange', 'pink'])
app.mainloop()