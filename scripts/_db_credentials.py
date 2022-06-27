import os

import yaml
from scripts.message_utils import fatal_error

# Data from docker-compose.yml to connected to the databases.

with open("docker-compose.yml", "r") as file:
    _yml = yaml.safe_load(file)

class _DBCredentials():
    def __init__(self, service) -> None:
        try:
            _db =  _yml["services"][service]
            _environment = _db["environment"]

            self.db_name = _environment["POSTGRES_DB"]

            self.dns =  f"""
                host={os.getenv("DATABASES_HOST")}
                dbname={self.db_name}
                user={_environment["POSTGRES_USER"]}
                password={_environment["POSTGRES_PASSWORD"]}
                port={_yml["services"][service]["ports"][0].split(":")[0]}
            """
        except:
            fatal_error("INVALID_YML_SERVICES")

source_db_credentials = _DBCredentials("source_db")
output_db_credentials = _DBCredentials("output_db")

