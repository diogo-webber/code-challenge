from scripts.Database import Database

class BaseWorker():
    """Base Class for Extractor and Importer"""
    def __init__(self, target_date: str) -> None:
        """
        Parameters:
            `target_date`: str - the date to be used in operations.
        """
        self.target_date = target_date
        self.db = None
            
    def set_db(self, db: Database):
        """
        Parameters:
            `db`: Database - the database object.
        """
        self.db = db
    
    def connect_to_db(self):
        """Create a Database connection if not have one."""
        if self.db and not self.db.conn:
            self.db.connect()