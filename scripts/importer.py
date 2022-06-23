#!/usr/bin/env python
import os
from glob import glob

from scripts._database import Database
from scripts.constants import SQL
from scripts.configs import OUTPUT_DB_CREDENTIALS, RESULT_QUERY_FILE_NAME
from scripts.message_utils import skip_operation, output_message, sucess

def _collect_csv_for_date(date: str):
    return glob(f"./data/**/{date}/*.csv", recursive=True)

class Importer():
    """Class that performs operations with the output database."""
    def __init__(self, target_date: str) -> None:
        """
        Parameters:
            `target_date`: str - the date to be used in operations.
        """
        self.target_date = target_date
        self.target_db = None

    def import_to_postgres(self):
        """
        Import the data from CSV files to output database.

        Return:
            `sucess`: bool - whether the import was successful.
        """

        output_message("IMPORT")

        files = _collect_csv_for_date(self.target_date)
        if len(files) == 0:
            print(f"Não há dados disponiveis para a data \"{self.target_date}\".")
            return False

        self.target_db = Database(credentials_obj=OUTPUT_DB_CREDENTIALS)
        self.target_db.clear_tables()

        for csv in files:
            file_name = os.path.basename(csv).removesuffix(".csv")
            table = file_name.split("_")[1:-1]
            table = "_".join(table)
            sql = SQL.IMPORT_TO_DB.format(table_name=table)
            with open(csv, "r") as file:
                self.target_db.execute_copy(sql, file)

        self.target_db.close_connection()

        return sucess()
    
    def generate_final_query(self):
        """
        Export a query that shows the orders and its details to a CSV file.

        Return:
            `sucess`: bool - whether the export was successful.
        """

        output_message("QUERY", name=RESULT_QUERY_FILE_NAME)

        self.target_db = Database(credentials_obj=OUTPUT_DB_CREDENTIALS)

        self.target_db.run_sql(SQL.SELECT_FINAL_QUERY)

        if len(self.target_db.cur.fetchall()) == 0:
            skip_operation("QUERY_NO_DATA")
            self.target_db.close_connection()
            return False

        with open(f"./{RESULT_QUERY_FILE_NAME}.csv", "w") as file:
            self.target_db.execute_copy(SQL.FINAL_QUERY, file)

        self.target_db.close_connection()
        return sucess()