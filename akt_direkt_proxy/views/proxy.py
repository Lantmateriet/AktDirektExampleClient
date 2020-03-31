"""Web API accepting calls with paths like those used by Akt Direkt."""

import flask

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

bp = flask.Blueprint("proxy", __name__, url_prefix="/")


@bp.route("/document/bundle.djvu")
def get_djvu():
    """Request for a dossiers bundled DjVU.

    to test this service use:
        djview "http://localhost:5000/document/bundle.djvu?archive=k21g&id=2180k-10/11"
    """
    archive = flask.request.args.get("archive")
    id_ = flask.request.args.get("id")
    r = flask.current_app.client.get_djvu(archive, id_)
    print_app_headers(r)
    if r.ok:
        return flask.Response(
            r.content, mimetype=r.headers["Content-Type"], status=r.status_code
        )
    else:
        print(r.headers)
        print(r.text)
        return flask.Response(
            r.content, mimetype=r.headers.get("Content-Type", ""), status=r.status_code
        )


@bp.route("/document/index.djvu")
def get_index_djvu():
    """Request for a dossiers index.djvu.

    This exists for backward compatibility with an older version (V3 API)

    redirects to bundle.djvu

    to test this service use:
        djview "http://localhost:5000/document/index.djvu?archive=k21g&id=2180k-10/11"
    """
    archive = flask.request.args.get("archive")
    id_ = flask.request.args.get("id")
    return flask.redirect(
        flask.url_for("proxy.get_djvu", archive=archive, id=id_), code=302
    )


def print_app_headers(r):
    """Print the application specific headers."""
    wanted_headers = ("Archive", "Document-ID", "Error-Code", "Error-Message")
    headers = {k: v for (k, v) in r.headers.items() if k in wanted_headers}
    print("Headers received from Akt Direkt:", headers)


@bp.route("/ping")
def get_ping():
    """Test the connection to the archive system.

    to test this service use:
        curl "http://localhost:5000/ping"
    """
    r = flask.current_app.client.get_ping()
    print_app_headers(r)
    if r.ok:
        return flask.Response(
            r.content, mimetype=r.headers["Content-Type"], status=r.status_code
        )
    else:
        print(r.headers)
        print(r.text)
        return flask.Response(
            r.content, mimetype=r.headers.get("Content-Type", ""), status=r.status_code
        )
