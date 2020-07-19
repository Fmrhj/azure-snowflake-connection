import logging

from fastapi import FastAPI, Response
import pandas as pd
import uvicorn

from auth.azure import AzureAuthorizer
from db.snowflakeconnector import SnowflakeConnector
from utils.config import parse_configuration


def main(configfile="./config.yml"):

    logging.basicConfig(level=logging.INFO)

    app = FastAPI()
    
    # read configuration file 
    config = parse_configuration("./config.yml")
    
    config_azure = config["azure"]
    config_snowflake = config['snowflake']

    authorizer = AzureAuthorizer(
        authority_uri=config_azure["authority_uri"],
        client_id=config_azure["app_id"],
        app_password=config_azure["app_password"]
        )
    
    snowflake_db_connector = SnowflakeConnector(
        user = config_snowflake["user"],
        account=config_snowflake["account"],
        role=config_snowflake["role"],
        warehouse=config_snowflake["warehouse"],
        resource_name=config_azure["resource_name"],
        authorizer=authorizer)
        
    @app.get("/")
    async def root():
        engine = snowflake_db_connector.get_engine()
        df = pd.read_sql_query(config["sql"]["select_statement"], engine)
        data = df.to_json(orient="index")
        engine.dispose()
        return Response(content=data, media_type="application/json")

    # implement an asgi async server (socket io). For the time keep it simple
    uvicorn.run(app, host="0.0.0.0", port=5000, workers=1)

if __name__=="__main__":
    main()
