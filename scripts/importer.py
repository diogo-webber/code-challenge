import os
from glob import glob

from scripts.BaseWorker import BaseWorker
from scripts.constants import SQL
from scripts.Printer import Printer

RESULT_QUERY_PATH = os.getenv("RESULT_QUERY_PATH")

def _collect_csv_for_date(date: str):
    return glob(f"./data/**/{date}/*.csv", recursive=True)

class Importer(BaseWorker):
    """Class that performs operations with the output database."""
    def import_to_postgres(self):
        """
        Import the data from CSV files to output database.

        Return:
            `success`: bool - whether the import was successful.
        """

        Printer.output_message("IMPORT")
        
        self.connect_to_db()

        files = _collect_csv_for_date(self.target_date)
        if len(files) < 5:
            return Printer.skip_operation("IMPORT_NO_DATA", date=self.target_date)

        self.db.clear_tables()

        for csv in files:
            file_name = os.path.basename(csv).removesuffix(".csv")
            table = file_name.split("_")[1:-1]
            table = "_".join(table)
            sql = SQL.IMPORT_TO_DB.format(table_name=table)
            
            with open(csv, "r") as file:
                self.db.execute_copy(sql, file)

        return Printer.success()
    
    def generate_final_query(self):
        """
        Export a query that shows the orders and its details to a CSV file.

        Return:
            `success`: bool - whether the export was successful.
        """

        Printer.output_message("QUERY", name=RESULT_QUERY_PATH)

        self.connect_to_db()
            
        self.db.run_sql(SQL.SELECT_FINAL_QUERY)

        if len(self.db.cur.fetchall()) == 0:
            return Printer.skip_operation("QUERY_NO_DATA")

        with open(RESULT_QUERY_PATH, "w") as file:
            self.db.execute_copy(SQL.FINAL_QUERY, file)

        return Printer.success()