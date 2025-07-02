import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create a graph to represent the farm irrigation network
def create_irrigation_network():
    irrigation_network = nx.Graph()
    irrigation_network.add_edges_from([
        (1, 2, {'weight': 2}),
        (1, 3, {'weight': 1}),
        (2, 3, {'weight': 2}),
        (2, 4, {'weight': 3}),
        (3, 4, {'weight': 1}),
        (4, 5, {'weight': 2}),
        (3, 5, {'weight': 4})
    ])
    return irrigation_network

# Find the minimum spanning tree
def find_minimum_spanning_tree(graph):
    return nx.minimum_spanning_tree(graph)

# Display the network on the canvas
def display_network(graph, mst=None, path_edges=None):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 6))

    # Draw the graph
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, ax=ax)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)

    # Draw the minimum spanning tree edges
    if mst:
        nx.draw_networkx_edges(mst, pos, edge_color='green', width=2, ax=ax, label="Minimum Spanning Tree")
    
    # Draw the optimal path edges
    if path_edges:
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=3, ax=ax, label="Optimal Path")

    ax.set_title("Farm Irrigation Network")
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    plt.close(fig)

# Find the optimal path using Dijkstra's algorithm
def optimal_water_distribution(graph, source, target):
    try:
        path = nx.shortest_path(graph, source=source, target=target, weight='weight')
        path_edges = list(zip(path, path[1:]))
        return path, path_edges
    except nx.NetworkXNoPath:
        messagebox.showerror("Error", f"No path exists between node {source} and node {target}")
        return None, None

# Callback for the "Show Path" button
def show_path():
    try:
        source_node = int(start_entry.get())
        target_node = int(end_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid integers for nodes.")
        return

    # Find and display the optimal path
    path, path_edges = optimal_water_distribution(irrigation_network, source_node, target_node)
    if path:
        messagebox.showinfo("Optimal Path", f"Optimal Path from {source_node} to {target_node}: {path}")
        display_network(irrigation_network, mst, path_edges)

# Set up the main window
window = tk.Tk()
window.title("Farm Irrigation Network")

# Instructions label
instructions = tk.Label(window, text="Enter start and end nodes for irrigation path:", font=("Arial", 12))
instructions.pack(pady=10)

# Start node input
start_label = tk.Label(window, text="Start Node:", font=("Arial", 10))
start_label.pack()
start_entry = tk.Entry(window)
start_entry.pack(pady=5)

# End node input
end_label = tk.Label(window, text="End Node:", font=("Arial", 10))
end_label.pack()
end_entry = tk.Entry(window)
end_entry.pack(pady=5)

# Show Path button
show_path_button = tk.Button(window, text="Show Path", command=show_path, font=("Arial", 10))
show_path_button.pack(pady=10)

# Initialize the irrigation network and minimum spanning tree
irrigation_network = create_irrigation_network()
mst = find_minimum_spanning_tree(irrigation_network)

# Initial display of the network with MST
display_network(irrigation_network, mst)

# Run the Tkinter main loop
window.mainloop()




