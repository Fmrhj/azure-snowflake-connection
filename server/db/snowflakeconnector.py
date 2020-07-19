import logging
from typing import Optional

from snowflake.sqlalchemy import URL as snow_URL
from sqlalchemy.engine import Engine, create_engine

from auth.azure import AzureAuthorizer


class SnowflakeConnector:
    """
    Class to create Snowflake connections
    """

    logger = logging.getLogger("SnowflakeConnector")

    def __init__(
        self,
        user: str,
        account: str,
        role: str,
        warehouse: Optional[str],
        password: Optional[str] = None,
        authorizer: Optional[AzureAuthorizer] = None,
        resource_name: Optional[str] = None,
    ):
        self._user = user
        self._account = account
        self._password = password
        self._warehouse = warehouse

        if authorizer is None:
            self._engine = self._create_engine_sql_auth()
        elif resource_name is not None:
            self._engine = self._create_engine_azure_auth(resource_name, authorizer)
        else:
            raise Exception("Check your resource name and authorization method")

        with self._engine.connect():
            self.logger.info("Snowflake SQL connection successful")

    def _create_engine_sql_auth(self) -> Engine:

        url = snow_URL(
            user=self._user,
            account=self._account,
            password=self._password,
            warehouse=self._warehouse,
        )
        engine = create_engine(url, pool_recycle=3600)
        return engine

    def _create_engine_azure_auth(self, resource_name: str, authorizer: AzureAuthorizer) -> Engine:

        token = authorizer.get_token_with_client_credentials(resource_name)

        url = snow_URL(user=self._user, account=self._account, token=token, authenticator="oauth")

        engine = create_engine(url, pool_recycle=3600)
        return engine

    def get_engine(self) -> Engine:
        return self._engine
