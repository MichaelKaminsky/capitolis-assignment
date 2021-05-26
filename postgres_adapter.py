import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()


class Database:
    """PostgreSQL Database class."""

    def __init__(self):
        self.host = os.getenv('DATABASE_HOST')
        self.username = os.getenv('DATABASE_USERNAME')
        self.password = os.getenv('DATABASE_PASSWORD')
        self.port = os.getenv('DATABASE_PORT')
        self.dbname = os.getenv('DATABASE_NAME')
        self.conn = None

    def connect(self):
        """Connect to a Postgres database."""
        if self.conn is None:
            self.conn = psycopg2.connect(host=self.host,
                                         user=self.username,
                                         password=self.password,
                                         port=self.port,
                                         dbname=self.dbname,
                                         sslmode='require')

    def insert_rows(self, data=list, table_name=str):
        new_data = []
        for raw in data:
            new_data.append(tuple(raw.values()))

        records_list_template = ','.join(['%s'] * len(new_data))
        keys = tuple(data[0].keys())
        keys_stryng = ', '.join(keys)

        query = f'INSERT INTO {table_name} ({keys_stryng})' \
                f' VALUES ' \
                f'{records_list_template}'

        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query, new_data)
            self.conn.commit()
            cur.close()
            return f"{cur.rowcount} rows inserted."


db = Database()
