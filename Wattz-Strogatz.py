import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def create_ring_lattice(N, k):
    G = nx.Graph()
    G.add_nodes_from(range(N))
    for node in range(N):
        for i in range(1, k//2 + 1):
            neighbor = (node + i) % N
            G.add_edge(node, neighbor)
    return G


def rewire_edges_real_time(G, k, p, draw_interval=0.5):
    N = len(G.nodes())
    
    pos = nx.circular_layout(G)
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))
    
    def handle_close(evt):
        print("Window closed.")
        plt.ioff()
    
    fig.canvas.mpl_connect('close_event', handle_close)
    
    node_colors = ['skyblue'] * N
    
    try:
        for node in range(N):
            neighbors = list(G.neighbors(node))

            node_colors[node] = 'red'
            ax.clear()
            nx.draw(G, pos, ax=ax, with_labels=False, node_color=node_colors, node_size=50, edge_color="gray")
            plt.title(f"Processing node {node}")
            plt.pause(draw_interval)
            
            for i in range(1, k//2 + 1):
                neighbor = (node + i) % N
                if np.random.rand() < p:
                    G.remove_edge(node, neighbor)
                    
                    new_neighbor = np.random.choice(list(set(range(N)) - set(G.neighbors(node)) - {node}))
                    G.add_edge(node, new_neighbor)
                    
                    node_colors[new_neighbor] = 'green'
                    ax.clear()
                    nx.draw(G, pos, ax=ax, with_labels=False, node_color=node_colors, node_size=50, edge_color="gray")
                    plt.title(f"Rewiring edge ({node}, {neighbor}) -> ({node}, {new_neighbor})")
                    plt.pause(draw_interval)
                    
                    node_colors[new_neighbor] = 'skyblue'
                    
            node_colors[node] = 'skyblue'
            
            if not plt.fignum_exists(fig.number):
                raise RuntimeError("Window closed by user.")
                    
    except RuntimeError as e:
        print(e)
    finally:
        plt.title("Done!")
        plt.ioff()
        plt.show()
    
    return G


def watts_strogatz_model_real_time(N, k, p, draw_interval=0.5):
    G = create_ring_lattice(N, k)
    G = rewire_edges_real_time(G, k, p, draw_interval)
    return G

N = 20
k = 4
p = 0.5
draw_interval = 0.5


G = watts_strogatz_model_real_time(N, k, p, draw_interval)

