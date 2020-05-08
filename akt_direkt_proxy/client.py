"""Client library for Akt Direkt service."""

import threading
import urllib.parse
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError, OAuth2Error
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

__copyright__ = """

    Copyright 2018 Lantmäteriet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""


class AktDirectClient:
    """Client library for Akt Direkt service."""

    def __init__(self, service_url, consumer_key, consumer_secret, token_url):
        """Initialize client with configuration given by Lantmäteriet."""
        self.service_url = service_url
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.token_url = token_url
        self._update_token_recursion_limiter = threading.Semaphore(
            1
        )  # Used to stop recursion in error handling
        self._init_lock = threading.RLock()
        self._initialize()

    def _initialize(self):
        """Initialize/reinitialize client libraries."""
        with self._init_lock:
            self.auth = HTTPBasicAuth(self.consumer_key, self.consumer_secret)
            self.client = BackendApplicationClient(client_id=self.consumer_key)
            self.oauth = OAuth2Session(client=self.client)
            self.update_token()

    def update_token(self):
        """Fetch new token from server.

        Get a access token using your consumer key and secret,
        the token will be used to access the service.
        Note that a token has a limited life.
        """
        with self._init_lock:
            try:
                token = self.oauth.fetch_token(token_url=self.token_url, auth=self.auth)
                print(f"fetched new token: {token}")
                self.oauth.token = token
            except OAuth2Error as err:
                # We have seen a case where update_token on expiration fails but reinitializaton
                # works, so if update fails we try to reinitialize.
                # But initilize calls update_token so if it's a "real" error we needs to stop the error
                # handling from going into a recursion.
                with self._update_token_recursion_limiter as recursion_ok:
                    if not recursion_ok:
                        raise

                    print(
                        "Got OAuth2Error when trying to update token, will reinitialize. error was: ",
                        err,
                    )
                    self._initialize()

    def _call_service(self, rel_path, params=None, stream=False):
        """Call the service and handle token expiration.

        This method is used by the get_ and test_ methods in this class.

        returns a requests response object
        """
        # without the / the last element in service_url may be replaced
        url = urllib.parse.urljoin(self.service_url + "/", rel_path)
        try:
            res = self.oauth.get(url, stream=stream, params=params)
        except TokenExpiredError:
            # If the token has expired get a new one and retry
            self.update_token()
            res = self.oauth.get(url, stream=stream, params=params)
        except OAuth2Error as err:
            # This is not a case we have seen but to be on the safe side we try to reinitialize
            # if it happens.
            print(
                "Got OAuth2Error other than TokenExpiredError, will reinitialize. error was: ",
                err,
            )
            self._initialize()
            res = self.oauth.get(url, stream=stream, params=params)
        if not res.ok:
            # If update_token() fails the next call will result in a 401
            # We can choose to reinitialize on all errors instead of only 401 because
            # the Akt-Direkt API do not use HTTP error codes as part of the API.
            print(
                "Got an HTTP response >= 400, will reinitialize and try again, error was: ",
                res.status_code,
                res.text,
            )
            self._initialize()
            res = self.oauth.get(url, stream=stream, params=params)

        print(f"Called {res.request.url}", params)
        if not res.ok:
            print("Call failed, status-code:", res.status_code)
            print(res.text)
        return res

    def get_djvu(self, archive, id_):
        """Get the dossier as a DjVU.

        returns a requests response object
        """
        rel_path = "document/bundle.djvu"
        params = {"archive": archive, "id": id_}
        res = self._call_service(rel_path, stream=True, params=params)
        return res

    def get_djvu_djvu_on_error(self, archive, id_):
        """Get the dossier as a DjVU.

        returns a requests response object
        """
        rel_path = "document/djvu_on_error/bundle.djvu"
        params = {"archive": archive, "id": id_}
        res = self._call_service(rel_path, stream=True, params=params)
        return res

    def get_ping(self):
        """Make a communication test with Akt Direkt.

        This call test your configuration, communications, authentication and authorization.

        returns a requests response object
        """
        rel_path = "ping"
        res = self._call_service(rel_path)

        return res

    def test_connection(self):
        """Make a communication test with Akt Direkt.

        This call test your configuration, communications, authentication and authorization.

        returns a boolean, True if everything is OK or False if not.
        """
        res = self.get_ping()
        return res.ok
