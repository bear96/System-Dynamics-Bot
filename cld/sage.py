import os
from cld import CLD
from utils import *
import re
import networkx as nx
from matplotlib import pyplot as plt
from matplotlib import image
import docx
import numpy as np
from PIL import Image
from typing import Optional


class GreatSage():
    def __init__(self,
                 verbose:bool = False,
                 diagram: bool = False,
                 threshold: float = 0.85,
                 question: Optional[str] = None,
                 api_key: Optional[str] = None):
        self.verbose = verbose
        self.diagram = diagram
        self.question = question
        self.CLD = CLD(question = self.question, verbose = self.verbose, threshold=threshold)

    def think(self):
        response = self.CLD.generate_causal_relationships()
        result_list = self.check_relationship_repetitions(response)
        if self.diagram:
            self.generate_causal_loop_diagram(result_list)
        if not self.verbose:
            return response
        else:
            return None

    def check_relationship_repetitions(self, response):
        lines = response.strip().split('\n')
        result_list = [line[line.index('.') + 2:].strip() for line in lines]
        result_list = [re.sub(r'[!.,;:]', '', line) for line in result_list]
        result_list = list(set(result_list))
        return result_list

    def generate_causal_loop_diagram(self,result_list):
        symbol = ""
        G = nx.MultiDiGraph()

        for i, line in enumerate(result_list):
            variable1, variable2, symbol = self.CLD.extract_variables(line)
            G.add_nodes_from([variable1,variable2])
            G.add_edge(variable1, variable2, label = symbol)
        A = nx.nx_agraph.to_agraph(G)
        for edge in A.edges():
            edge.attr.update(directed=True, arrowhead='vee', arrowsize='0.5', constraint = False)
        A.graph_attr['splines'] = 'curved'  # Enable splines for curved edges
        A.graph_attr['layout'] = 'neato'
        A.graph_attr['overlap'] = 'scale'
        A.graph_attr['sep'] = '0.5'
        # Set font size for node labels
        A.node_attr['fontname'] = 'Helvetica'  # Choose your font
        A.node_attr['fontsize'] = '14'  # Set font size

        # Set font size for edge labels
        A.edge_attr['fontname'] = 'Helvetica'
        A.edge_attr['fontsize'] = '12'
        A.edge_attr['labelfloat'] = 'true'

        A.graph_attr['size'] = '512,512'
        save_name = input("Enter the name of this diagram before saving: ")
        A.draw(f"./{save_name}.png", format="png", prog='neato')
        img = Image.open(f"./{save_name}.png")
        h = img.size[1] *4
        w = img.size[0] *4
        img = img.resize((w,h),resample=Image.BILINEAR)
        img.save(f"./{save_name}.png", dpi = (300,300))
        img.show()

        return A