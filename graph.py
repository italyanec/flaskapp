import networkx as nx
import pyexcel as pe
import numpy as np
import json

class Graph:
    def __init__(self, filepath):
        data = pe.get_sheet(file_name=filepath, name_columns_by_row=0)
        self.edges = list(zip(data.column_at(0), data.column_at(1)))
        self.nodes = data.column_at(2)
        #self.G = nx.Graph()
        #self.G.add_edges_from(edges)

    def to_visjs(self):
        nodes = [{'id': i, 'label': i} for i in self.nodes]
        edges = [{'from': i[0], 'to': i[1]} for i in self.edges]
        data = {'nodes': nodes, 'edges': edges}
        return json.dumps(data)

if __name__ == "__main__":

    x = Graph('sample.xlsx')
    print(x.to_visjs())