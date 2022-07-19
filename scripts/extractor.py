import os
from pathlib import Path
import csv as csv_module
from glob import glob

from scripts.BaseWorker import BaseWorker
from scripts.Printer import Printer
from scripts.constants import SQL, OUTPUT_FILE_NAME_PATTERN, CSV_FOLDER_PATTERN, POSTGRES_FOLDER_PATTERN

STATIC_CSV_PATH = os.getenv("STATIC_CSV_PATH")

def _convert_csv_delimiter_and_copy(from_, to):
     with open(from_) as source_csv:
        with open(to, 'w', newline='') as file:
            reader = csv_module.DictReader(source_csv, delimiter=',')
            writer = csv_module.DictWriter(file, reader.fieldnames, delimiter='|')
            writer.writeheader()
            writer.writerows(reader)

class Extractor(BaseWorker):
    """Class that performs operations with the source database."""
    def extract_csv(self) -> bool:
        """
        Copy the CSV file and change the delimiter.

        Return:
            `sucess`: bool - whether the extraction was successful.
        """
        
        Printer.output_message("CSV")
        
        if not os.path.exists(STATIC_CSV_PATH):
            return Printer.skip_operation("NO_SOURCE_CSV", path=STATIC_CSV_PATH)

        target_path = Path(CSV_FOLDER_PATTERN.format(date=self.target_date))

        if os.path.exists(target_path):
            return Printer.skip_operation("CSV_EXIST", date=self.target_date)

        os.makedirs(target_path)

        csv_name = os.path.basename(STATIC_CSV_PATH).removesuffix(".csv")
        new_file = target_path / OUTPUT_FILE_NAME_PATTERN.format(table=csv_name, date=self.target_date)
        
        _convert_csv_delimiter_and_copy(from_=STATIC_CSV_PATH, to=new_file)
        
        return Printer.success()

    def extract_db(self) -> bool:
        """
        Extract all tables from source database

        Return:
            `success`: bool - whether the extraction was successful.
        """

        Printer.output_message("DB")
        
        self.connect_to_db()

        path_pattern = f"./data/postgres/*/{self.target_date}"
        if len(glob(path_pattern)) > 0:
            return Printer.skip_operation("CSV_TABLES_EXIST", date=self.target_date)

        table_list = self.db.list_tables()

        for table_name in table_list:
            target_path = Path(POSTGRES_FOLDER_PATTERN.format(table=table_name, date=self.target_date))
            os.makedirs(target_path)

            new_file = target_path / OUTPUT_FILE_NAME_PATTERN.format(table=table_name, date=self.target_date)

            sql = SQL.EXPORT_TO_CSV.format(table_name=table_name)
            with open(new_file, "w") as file:
               self.db.execute_copy(sql, file)

        return Printer.success()