import networkx as nx
import pyexcel as pe
import numpy as np
import json
import copy
from itertools import combinations


class Graph:
    def __init__(self, filepath):
        data = pe.get_sheet(file_name=filepath, name_columns_by_row=0)
        self.nodes = list(filter(lambda x: isinstance(x, int),
                                 set(data.column_at(2))))
        self.edges = list(filter(lambda x: x[0] in self.nodes and x[1] in self.nodes,
                                 list(zip(data.column_at(0), data.column_at(1)))))

        self.find_longest_path()

    def path_to_list_of_edges(self, path):
        list_of_edges = []
        for i in range(len(path) - 1):
            for edge in self.edges:
                if path[i] in edge and path[i + 1] in edge:
                    list_of_edges.append(edge)
        return list_of_edges

    def find_longest_path(self):
        g = nx.Graph()
        g.add_edges_from(self.edges)
        nodes = list(g.nodes)

        all_pairs_of_nodes = []
        for i in range(g.number_of_nodes() - 1):
            for j in range(i + 1, g.number_of_nodes()):
                all_pairs_of_nodes.append((nodes[i], nodes[j]))

        all_paths = []
        # all_pairs_of_nodes = combinations(g.number_of_nodes(), 2)
        for pair in all_pairs_of_nodes:
            for path in nx.all_simple_paths(g, pair[0], pair[1]):
                all_paths.append(path)

        self.lp_nodes = all_paths[np.argmax(list(map(len, all_paths)))]
        self.lp_edges = self.path_to_list_of_edges(self.lp_nodes)

    def to_sigmajs(self):
        pass

    def to_visjs(self):
        nodes = [{'id': i, 'label': str(i), 'shape': 'circle', 'color': 'green'} for i in
                 set(self.nodes) & set(self.lp_nodes)]
        nodes.extend([{'id': i, 'label': str(i), 'shape': 'circle', 'color': 'blue'} for i in
                      set(self.nodes) ^ set(self.lp_nodes)])
        # nodes = [{'id': i, 'label': i, 'shape': 'circle'} for i in set(self.nodes)]
        edges_copy = copy.deepcopy(self.edges)
        [edges_copy.remove(edge) for edge in self.lp_edges]
        edges = []
        for edge in edges_copy:
            edges.append({'from': edge[0], 'to': edge[1], 'color': {'color': 'blue'}})
        print(self.lp_edges)
        for edge in self.lp_edges:
            edges.append({'from': edge[0], 'to': edge[1], 'color': {'color': 'green'}})
        data = {'nodes': nodes, 'edges': edges}

        return json.dumps(data)


if __name__ == "__main__":
    x = Graph('sample.xlsx')
    print(x.to_visjs())
