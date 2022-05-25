import os
from urllib.parse import urlparse


class DBClient:

    def __init__(self, dsn):
        self.driver = self.default_mysql_driver()
        self.dsn = dsn
        self._parsed = urlparse(self.dsn)
        self.conn = self.connect()

    @staticmethod
    def default_mysql_driver():
        import pymysql
        return pymysql


    @property
    def database(self):
        if self._parsed.path.strip('/'):
            return os.path.basename(self._parsed.path)
        return None

    def get_url(self):
        return self._parsed.geturl()

    def connect(self, database=None, ensure_db=True, **kwargs):
        """
        :param use_proxy: respect environment variable ALL_PROXY
        """
        database = database or self.database
        params = {
            'host': self._parsed.hostname,
            'port': self._parsed.port,
            'user': self._parsed.username,
            'password': self._parsed.password,
            'autocommit': True,
        }
        params.update(kwargs)

        if database and ensure_db:
            conn, cursor = None, None
            try:
                conn = self._create_conn(**params)
                cursor = conn.cursor()
                cursor.execute(f'create database if not exists `{database}`')
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
        if database:
            params['database'] = database

        return self._create_conn(**params)

    def _create_conn(self, **params):
        return self.driver.connect(**params)

    def execute_sql(self, sql, params=None, conn=None, log_sql=True):
        print("execut sql {}".format(sql))
        conn = conn or self.conn
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
