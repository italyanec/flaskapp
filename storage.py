import pyexcel
import sqlite3

from datetime import datetime
from graph import Graph


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
