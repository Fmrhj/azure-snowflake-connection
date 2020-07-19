from typing import Any, Dict, Optional

import adal


class AzureAuthorizer:
    """
    Azure authorizer. Gets token from a registered client application for a particular ouath resource
    """

    def __init__(self, authority_uri: str, app_password: str, client_id: str):

        self._authority_uri = authority_uri
        self._app_pasword = app_password
        self._context = adal.AuthenticationContext(authority_uri, api_version=None)
        self._client_id = client_id

    def get_token_with_client_credentials(self, resource_name: str) -> str:
        token = self._context.acquire_token_with_client_credentials(
            resource=resource_name, client_id=self._client_id, client_secret=self._app_pasword
        )
        return token["accessToken"]
