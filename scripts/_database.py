import psycopg2

from scripts.constants import SQL
from scripts.message_utils import fatal_error

def _get_table_names(cur):
    cur.execute(SQL.LIST_TABLES)
    return [row[0] for row in cur.fetchall()]

class Database():
    """Create a Postgres database connection."""
    def __init__(self, credentials_obj) -> None:
        """
        Parameters:
            `credentials_obj` - One of the classes of configs.py
        """
        self.name = credentials_obj.db_name
        self.credentials_dsn = credentials_obj.dns
        self.conn = self._connect()
        self.cur = self.conn.cursor()

    def _connect(self):
        try:
            return psycopg2.connect(self.credentials_dsn)
        except Exception as error:
            error_str = str(error)
            if error_str.find("Is the server running") != -1:
                fatal_error("DB_OFFLINE", db_name=self.name)
            elif error_str.find("server terminated abnormally") != -1:
                fatal_error("DB_LOADING",  db_name=self.name)
            else:
                fatal_error("DB_FAIL", error=error_str)
                
    def _sql_wrapper(self, fn):
        try:
            query = fn(self.cur)
        except Exception as error:
            self.conn.rollback()
            self.close_connection()
            raise error
        else:
            self.conn.commit()
            return query

    def clear_tables(self):
        """Erases all data from the database tables."""
        tables = ' ,'.join(self.list_tables())
        self.run_sql(SQL.TRUNCATE_ALL.format(select=tables))

    def execute_copy(self, sql, file):
        """Execute a SQL copy query.

        Parameters:
            `sql`: str - the SQL copy query.
            `file`: IO - the file-like object to copy to/from
        """
        self._sql_wrapper(fn=lambda cursor: cursor.copy_expert(sql, file))

    def run_sql(self, sql):
        """
        Execute a SQL query.

        Parameters:
            `sql`: str - the SQL query.
        """
        self._sql_wrapper(fn=lambda cursor: cursor.execute(sql))

    def list_tables(self):
        """
        List all public tables in the database.

        Return:
            `table_list`: List[str] - the list of tables.

        """
        return self._sql_wrapper(fn=_get_table_names)

    def close_connection(self):
        """Close the connection with the database."""
        self.cur.close()
        self.conn.close()
