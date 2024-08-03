import networkx as nx
import matplotlib.pyplot as plt
import re

def generate_tracert_graph(tracert_result, target):
    G = nx.DiGraph()
    ip_pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
    ips = ip_pattern.findall(tracert_result)
    
    for i in range(len(ips) - 1):
        G.add_edge(ips[i], ips[i+1])
    
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')
    graph_image_path = f"static/tracert_{target}.png"
    plt.savefig(graph_image_path)
    plt.close()
    
    return graph_image_path
