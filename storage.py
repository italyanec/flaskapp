import pyexcel
import networkx
import numpy
import json
import copy
import sqlite3

from itertools import combinations
from datetime import datetime


def parse(file):
    excel = {'content': file.read(),
             'name': file.filename,
             'type': file.filename.split('.')[-1]}

    data = pyexcel.get_sheet(file_content=excel['content'], file_type=excel['type'], name_columns_by_row=0)
    nodes = list(filter(lambda x: isinstance(x, int),
                        set(data.column_at(2))))
    edges = list(filter(lambda x: x[0] in nodes and x[1] in nodes,
                        list(zip(data.column_at(0), data.column_at(1)))))

    return {'nodes': nodes, 'edges': edges}


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

    def to_visjs(self):
        nodes = [{'id': i, 'label': str(i), 'shape': 'circle', 'color': 'green'} for i in
                 set(self._nodes) & set(self._lp_nodes)]
        nodes.extend([{'id': i, 'label': str(i), 'shape': 'circle', 'color': 'blue'} for i in
                      set(self._nodes) ^ set(self._lp_nodes)])
        # nodes = [{'id': i, 'label': i, 'shape': 'circle'} for i in set(self.nodes)]
        edges_copy = copy.deepcopy(self._edges)
        [edges_copy.remove(edge) for edge in self._lp_edges]
        edges = []
        for edge in edges_copy:
            edges.append({'from': edge[0], 'to': edge[1], 'color': {'color': 'blue'}})
        for edge in self._lp_edges:
            edges.append({'from': edge[0], 'to': edge[1], 'color': {'color': 'green'}})
        data = {'nodes': nodes, 'edges': edges}

        return json.dumps(data)


# https://habrahabr.ru/post/321510/
class History:
    def __init__(self, dbname):
        self._dbname = dbname
        conn = sqlite3.connect(self._dbname)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Graphs (
            ID integer primary key autoincrement,
            NET text not null,
            FILENAME text not null,
            DATETIME text not null
        )""")

    def save(self, file):
        data = parse(file)
        net = Graph(data['edges'], data['nodes']).to_visjs()
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(self._dbname)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Graphs (NET, FILENAME, DATETIME) VALUES ( ?, ?, ? )",
                                           (net, file.filename, time))
        conn.commit()
        conn.close()

    def tolist(self):
        conn = sqlite3.connect(self._dbname)
        cursor = conn.cursor()
        req = "SELECT ID, DATETIME, FILENAME FROM Graphs ORDER BY ID DESC"
        data = [row for row in cursor.execute(req)]
        conn.close()

        return data

    def _get_values_by_id(self, values, id):
        conn = sqlite3.connect(self._dbname)
        cursor = conn.cursor()
        req = 'SELECT {} FROM Graphs WHERE id == {}'.format(
            ','.join(values), '(SELECT MAX(ID) FROM Graphs)' if id < 0 else str(id))
        data = next(cursor.execute(req))
        conn.close()

        return data

    def get_metadata_by_id(self, id):
        return self._get_values_by_id(['ID', 'DATETIME', 'FILENAME'], id)

    def get_graph_by_id(self, id):
        return self._get_values_by_id(['NET'], id)

    def get_all_by_id(self, id):
        return self._get_values_by_id(['ID', 'DATETIME', 'FILENAME', 'NET'], id)
