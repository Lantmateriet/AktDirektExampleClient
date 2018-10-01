"""web API accepting calls with paths like those used by Akt Direkt"""

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

bp = flask.Blueprint('proxy', __name__, url_prefix='/')

@bp.route('/document/index.djvu')
def get_index_djvu():
    """Request for a dossiers index.djvu

    to test this service use:
        djview "http://localhost:5000/document/index.djvu?archive=k21g&id=2180k-10/11"
    """
    # djview 'http://localhost:8091/arken/djvu/v3.0/document/index.djvu?archive=k21g&id=2180k-10/11'
    archive = flask.request.args.get('archive')
    id_ = flask.request.args.get('id')
    r = flask.current_app.client.get_index_djvu(archive, id_)
    print_app_headers(r)
    if r.ok:
        return flask.Response(r.content, mimetype=r.headers['Content-Type'], status=r.status_code)
    else:
        print(r.headers)
        print(r.text)
        return flask.Response(r.content, mimetype=r.headers.get('Content-Type', ''), status=r.status_code)

@bp.route('/document/page_<vers>_<subdoc>_<page>_<archive>_<enc_id>.djvu')
def get_page_djvu(vers, subdoc, page, archive, enc_id):
    """Request for a single page

    to test this service use:
        djview 'http://localhost:5000/document/page_1_1_1_k21g_MjE4MGstMTAvMTE=.djvu'
    """
    r = flask.current_app.client.get_page_djvu(vers, subdoc, page, archive, enc_id)
    print_app_headers(r)
    return flask.Response(r.content, mimetype=r.headers['Content-Type'], status=r.status_code)

def print_app_headers(r):
    """Print the application specific headers"""
    wanted_headers = ('Archive', 'Document-ID', 'Error-Code', 'Error-Message')
    headers = {k: v for (k, v) in r.headers.items() if k in wanted_headers}
    print('Headers received from Akt Direkt:', headers)

