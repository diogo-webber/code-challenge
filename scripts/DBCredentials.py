import os

import yaml
from scripts.Printer import Printer

# Data from docker-compose.yml to connected to the databases.

class DBCredentials():
    """Class that collect yml information about the database."""
    
    def __init__(self, yml_service: str) -> None:
        with open("docker-compose.yml", "r") as file:
            _yml = yaml.safe_load(file)
            
        try:
            _db =  _yml["services"][yml_service]
            _environment = _db["environment"]

            self.db_name = _environment["POSTGRES_DB"]

            self.dsn =  f"""
                host={os.getenv("DATABASES_HOST")}
                dbname={self.db_name}
                user={_environment["POSTGRES_USER"]}
                password={_environment["POSTGRES_PASSWORD"]}
                port={_db["ports"][0].split(":")[0]}
            """
        except:
            Printer.fatal_error("INVALID_YML_SERVICES")

