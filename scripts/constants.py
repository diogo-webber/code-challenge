
POSTGRES_FOLDER_PATTERN = "./data/postgres/{table}/{date}"
CSV_FOLDER_PATTERN = "./data/csv/{date}"

OUTPUT_FILE_NAME_PATTERN = "table_{table}_{date}.csv"

class SQL():
    """All SQLs used in this pipeline."""
    LIST_TABLES = """
        SELECT tablename
        FROM pg_catalog.pg_tables
        WHERE schemaname NOT IN 
        ('information_schema', 'pg_catalog')
    """

    TRUNCATE_ALL = "TRUNCATE {select} CASCADE;"

    GENERIC_COPY_TO = """
        COPY ({select})
        TO STDOUT
        WITH HEADER CSV
        DELIMITER '|'
    """

    EXPORT_TO_CSV = GENERIC_COPY_TO.format(select="SELECT * FROM {table_name}")

    IMPORT_TO_DB = """
        COPY {table_name}
        FROM STDIN
        WITH HEADER CSV
        DELIMITER '|'
        NULL ''
    """

    SELECT_FINAL_QUERY = """
        SELECT * 
            FROM
                orders AS ord 
                INNER JOIN order_details AS dtl
                ON (ord.order_id = dtl.order_id)
    """

    FINAL_QUERY = GENERIC_COPY_TO.format(select=SELECT_FINAL_QUERY)