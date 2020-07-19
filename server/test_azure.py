import logging

import pandas as pd
from snowflake.sqlalchemy import URL as snow_URL
from sqlalchemy.engine import create_engine

from auth.azure import AzureAuthorizer
from utils.config import parse_configuration

logging.basicConfig(level=logging.INFO)

# read configuration file
config = parse_configuration("./config.yml")

config_azure = config["azure"]

# instantiate authorizer
authorizer = AzureAuthorizer(
    authority_uri=config_azure["authority_uri"],
    client_id=config_azure["app_id"],
    app_password=config_azure["app_password"],
)

# resource name (uri in Azure AD) as defined in Azure oauth resource:
# really important: the resource name shall match EXACTLY the resource name registered in Snowflake security integration
# in other words it should match the claims encoded in the JSON Web Token (JWT)
resource_name = config_azure["resource_name"]

# get token
token = authorizer.get_token_with_client_credentials(resource_name)

# Connect to snowflake with registered Azure's client token:
# mandatory: user, account, role, authenticator, token
# optional: warehouse, database
config_snowflake = config["snowflake"]

url = snow_URL(
    user=config_snowflake["user"],
    role=config_snowflake["role"],
    account=config_snowflake["account"],
    # warehouse=config_snowflake["warehouse"],
    authenticator="oauth",
    # database = config_snowflake["database"],
    token=token,
)

engine = create_engine(url, pool_recycle=3600)

# fetch data
sql_statement = config["sql"]["select_statement"]
df = pd.read_sql_query(sql_statement, engine)
data = df.to_json(orient="index")
print(data)
engine.dispose()
print("Done!")
