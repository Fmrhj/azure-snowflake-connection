import pandas as pd

from db.snowflakeconnector import SnowflakeConnector
from utils.config import parse_configuration

# read configuration file
config = parse_configuration("./config.yml")

snowflake_config = config["snowflake"]

snowflake_db_connector = SnowflakeConnector(
    user=snowflake_config["user"],
    account=snowflake_config["account"],
    role=snowflake_config["role"],
    password=snowflake_config["password"],
    warehouse=snowflake_config["warehouse"],
)

engine = snowflake_db_connector.get_engine()

df = pd.read_sql_query(config["sql"]["select_statement"], engine)
print(df.to_json(orient="index"))

# connection.close()
engine.dispose()
print("Done!")
