import sqlite3


class SQLiteDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        columns_str = ', '.join(columns)
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")
        self.conn.commit()

    def drop_table(self, table_name):
        self.cursor.execute(f"DROP TABLE {table_name}")
        self.conn.commit()

    def insert_data(self, table_name, data):
        placeholders = ', '.join(['?' for _ in range(len(data))])
        self.cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", data)
        self.conn.commit()

    def update_data(self, table_name, data, condition):
        placeholders = ', '.join([f"{k} = ?" for k in data])
        condition_str = ' AND '.join([f"{k} = ?" for k in condition])
        values = list(data.values()) + list(condition.values())
        self.cursor.execute(f"UPDATE {table_name} SET {placeholders} WHERE {condition_str}", values)
        self.conn.commit()

    def delete_data(self, table_name, condition):
        condition_str = ' AND '.join([f"{k} = ?" for k in condition])
        values = list(condition.values())
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {condition_str}", values)
        self.conn.commit()

    def select_data(self, table_name, columns=None, condition=None):
        if columns is None:
            columns_str = '*'
        else:
            columns_str = ', '.join(columns)
        if condition is None:
            condition_str = ''
            values = []
        else:
            condition_str = ' WHERE ' + ' AND '.join([f"{k} = ?" for k in condition])
            values = list(condition.values())
        self.cursor.execute(f"SELECT {columns_str} FROM {table_name}{condition_str}", values)
        return self.cursor.fetchall()

    def count_table(self, table_name, columns):
        self.cursor.execute(f"SELECT count({columns}) FROM {table_name}")
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

