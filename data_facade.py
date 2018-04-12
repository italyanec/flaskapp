import sqlite3

# https://habrahabr.ru/post/321510/
class History:
    def __init__(self, dbname):
        self._conn = sqlite3.connect(dbname)
        self._cursor = self._conn.cursor()

    def add(self, data):
        try:
            self._cursor.execute('insert into Graphs values ({}, {}, {})'.format(
                filename, datetime, struct
            ))
        except sqlite3.DatabaseError as err:
            print('Error: ', err)

    def get_graph_by_id(self, id):
        self._cursor.execute('SELECT struct FROM Graphs WHERE id == {}'.format(id))
        self._cursor.fetchone()

        return

    def get_info_by_id(self, ):
        self._cursor.execute('SELECT * FROM Graphs')
        pass

if __name__ == "__main__":


