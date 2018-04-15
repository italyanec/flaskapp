import networkx
import numpy
import json
import copy

from itertools import combinations


class Graph:
    def __init__(self, edges, nodes):
        self._edges = edges
        self._nodes = nodes

        self._find_longest_path()

    def _path_to_list_of_edges(self, path):
        list_of_edges = []
        for i in range(len(path) - 1):
            for edge in self._edges:
                if path[i] in edge and path[i + 1] in edge:
                    list_of_edges.append(edge)
        return list_of_edges

    def _find_longest_path(self):
        g = networkx.Graph()
        g.add_edges_from(self._edges)

        all_paths = []
        for pair in combinations(g.nodes, 2):
            for path in networkx.all_simple_paths(g, pair[0], pair[1]):
                all_paths.append(path)

        self._lp_nodes = all_paths[numpy.argmax(list(map(len, all_paths)))]
        self._lp_edges = self._path_to_list_of_edges(self._lp_nodes)

    def to_visjs(self, color_lp='green', color_cm='blue'):
        # nodes in lp
        vis_nodes = [{'id': i,
                      'label': str(i),
                      'shape': 'circle',
                      'color': color_lp}
                     for i in set(self._lp_nodes)]
        # nodes not in lp
        vis_nodes.extend(
            [{'id': i,
              'label': str(i),
              'shape': 'circle',
              'color': color_cm}
             for i in set(self._nodes) ^ set(self._lp_nodes)])
        # edges in lp
        edges_copy = copy.deepcopy(self._edges)
        vis_edges = []
        for edge in self._lp_edges:
            edges_copy.remove(edge)  # create list of edges not including in the longest path
            vis_edges.append(
                {'from': edge[0],
                 'to': edge[1],
                 'color': {'color': color_lp}})
        # edges not in lp
        vis_edges.extend(
            [{'from': edge[0],
              'to': edge[1],
              'color': {'color': color_cm}}
             for edge in edges_copy])

        return json.dumps({'nodes': vis_nodes, 'edges': vis_edges})