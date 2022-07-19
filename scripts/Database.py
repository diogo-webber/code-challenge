import psycopg2

from scripts.constants import SQL
from scripts.Printer import Printer

def _handle_connection_error(db_name, error):
    error_str = str(error)
    id_ = None
    
    if error_str.find("Is the server running") != -1:
        id_ = "DB_OFFLINE"

    elif error_str.find("server terminated abnormally") != -1:
        id_ = "DB_LOADING"

    if id_:
        return Printer.fatal_error(id_, db_name=db_name)

    return Printer.fatal_error("DB_FAIL", error=error_str)

def _get_table_names(cur):
    cur.execute(SQL.LIST_TABLES)
    return [row[0] for row in cur.fetchall()]

class Database():
    """
    Create a Postgres database connection.
    
    Parameters:
        `credentials_obj`: _DBCredentials - a database credential object.
    """
    
    def __init__(self, credentials_obj) -> None:
        self.name = credentials_obj.db_name
        self.credentials_dsn = credentials_obj.dsn
        
        self.conn = None
        self.cur = None

    def connect(self):
        """Create the connection with the database."""
        try:
            self.conn = psycopg2.connect(self.credentials_dsn)
            self.cur = self.conn.cursor()
        
        except Exception as e:
            _handle_connection_error(db_name=self.name, error=e)

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
        """Close the connection with the database if exist."""
        if self.conn:
            self.cur.close()
            self.conn.close()
