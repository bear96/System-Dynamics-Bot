import networkx as nx
import pygraphviz as pgv
from PIL import Image
import matplotlib.pyplot as plt

# Create a MultiDiGraph
G = nx.MultiDiGraph()

# Add two directed edges between nodes 'a' and 'b'
G.add_edge('a', 'b', label='(-)')
G.add_edge('b', 'a', label='(+)')
G.add_edge('c','a',label = '(+)')
G.add_edge('d','c',label = '(-)')

# Convert to PyGraphviz graph
A = nx.nx_agraph.to_agraph(G)

# Customize the edges to have curved arrows on both ends
for edge in A.edges():
    edge.attr.update(directed=True, arrowhead='vee', arrowsize='0.5', constraint=False)

# Set additional graph attributes
A.graph_attr['layout'] = 'neato'
A.graph_attr['splines'] = 'curved'  # Enable splines for curved edges
A.graph_attr['overlap'] = 'scale'
A.graph_attr['sep'] = '0.5'

# Set font size for node labels
A.node_attr['fontname'] = 'Helvetica'  # Choose your font
A.node_attr['fontsize'] = '14'  # Set font size

# Set font size for edge labels
A.edge_attr['fontname'] = 'Helvetica'
A.edge_attr['fontsize'] = '12'
A.edge_attr['labelfloat'] = 'true'
A.graph_attr['size'] = '1024,1024'

# Save and display the graph image
A.draw("./test_graph.png", format="png", prog='neato')
img = Image.open("./test_graph.png")
# h = img.size[1] * 4
# w = img.size[0] * 4
# img = img.resize((w, h), resample=Image.LANCZOS)
img.show()
