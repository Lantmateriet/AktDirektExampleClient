#!/usr/bin/env python3
"""Configuration and initialization of the application."""

import os
import pathlib
import flask
import dotenv

from werkzeug.middleware.proxy_fix import ProxyFix

import akt_direkt_proxy.client
import akt_direkt_proxy.views.proxy
import akt_direkt_proxy.views.startpage

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


def _read_config(app, test_config):
    """Read configuration from ENV variables and config file.

    If test_config is given it is used instead of the configuration given in
    environment variables.
    """
    mandatory_vars = ("SERVICE_URL", "TOKEN_URL", "CONSUMER_KEY", "CONSUMER_SECRET")
    defaults = {"REVERSE_PROXIED": "False"}
    if test_config:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    else:
        # If an ENV file is specified then load it, it will not override existing ENV variables.
        # Load config from file if one is specified
        env_path = os.environ.get("AKTDIREKT_ENV_FILE", None)
        if env_path:
            dotenv.load_dotenv(dotenv_path=pathlib.Path(env_path))
            print("loaded environment from " + env_path)

        # Read config from ENV variables
        for var_name in set(mandatory_vars) | set(defaults.keys()):
            var = os.environ.get(var_name, default=defaults.get(var_name, None))
            print(var_name, var)
            if var:
                app.config[var_name] = var

    # Check that we have the necessary configuration variables
    missing = set(mandatory_vars) - app.config.keys()
    if missing:
        raise ValueError(
            "ERROR, missing the following configuration variables: " + " ".join(missing)
        )
    # print(app.config) # This prints you CONSUMER_KEY and SECRET so use with care.


def create_app(test_config=None):
    """Application creation, is called from the webserver."""
    # instantiate the app
    app = flask.Flask(__name__)

    _read_config(app, test_config)

    # Create the Akt Direct client and add it to the application context
    app.client = akt_direkt_proxy.client.AktDirectClient(
        service_url=app.config["SERVICE_URL"],
        token_url=app.config["TOKEN_URL"],
        consumer_key=app.config["CONSUMER_KEY"],
        consumer_secret=app.config["CONSUMER_SECRET"],
    )

    # The API of this web application is modular, lets register the modules (blueprints)
    app.register_blueprint(akt_direkt_proxy.views.proxy.bp)
    app.register_blueprint(akt_direkt_proxy.views.startpage.bp)

    if app.config["REVERSE_PROXIED"] == "True":
        # App is behind a proxy that sets the -For and -Host headers.
        # This is needed if the application is behind a reverse proxy that
        # changes how the URL:s look.
        print("ACTIVATING SUPPORT FOR REVERSE PROXY")

        # x_for – Number of values to trust for X-Forwarded-For.
        # x_host – Number of values to trust for X-Forwarded-Host.
        # x_prefix – Number of values to trust for X-Forwarded-Prefix.
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_prefix=1)

    return app
