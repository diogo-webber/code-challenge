STATIC_CSV_PATH = "./data/order_details.csv"
RESULT_QUERY_FILE_NAME = "result_query"

class SOURCE_DB_CREDENTIALS():
    """Data from docker-compose.yml to connected to the source database."""
    HOST = "localhost"
    NAME = "northwind"
    USER = "northwind_user"
    PASSWORD = "thewindisblowing"
    PORT = "5432"

class OUTPUT_DB_CREDENTIALS():
    """Data from docker-compose.yml to connected to the output database."""
    HOST = "localhost"
    NAME = "outputdb"
    USER = "outputdb_user"
    PASSWORD = "thewindisblowing"
    PORT = "5433"
