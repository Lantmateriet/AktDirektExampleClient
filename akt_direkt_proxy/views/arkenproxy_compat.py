"""web API emulating the old ArkenProxy API

Documentation for ArkenProxy API:
    ArkenProxy används genom att man gör ett anrop där man anger länets/arkivets id samt dokumentets id.

    Parametrar:
        document - dokumentets id (oftast aktbeteckningen)
        county - län (t.ex. 21)
        archive - arkiv (t.ex. lm21)
        debug - valfri text som kan vara behjälplig vid felsökning hos Lantmäteriet, t ex användarnamn

    Parametern document måste alltid anges och antingen county eller archive, debug är valfri.
    Alla parametrar måste vara URL-kodade, och vara kodat i ISO-8859-1.

    Exempel:

        Sök på län 21 och dokument 21-P90:90:
        http://<dator som kör arkenproxy>:8080/arkenproxyclient/simpleFetchDocument?county=21&document=21-P90%3A90

        Sök på arkiv lm21 och dokument 21-P90:90:
        http://<dator som kör arkenproxy>:8080/arkenproxyclient/simpleFetchDocument?archive=lm21&document=21-P90%3A90

        Sök på län 21 och dokument 21-P90:90 och skicka in extra debuginformation "Kalle Karlsson":
        http://<dator som kör arkenproxy>:8080/arkenproxyclient/simpleFetchDocument?county=21&document=21-P90%3A90&debug=Kalle%20Karlsson


"""

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

bp = flask.Blueprint('arkenproxy_compat', __name__, url_prefix='/')


@bp.route('/arkenproxyclient/simpleFetchDocument')
def get_index_djvu():
    """Request for a dossiers index.djvu

    to test this service use:
        djview "http://localhost:5000/arkenproxyclient/simpleFetchDocument?county=21&document=21-P90%3A90"
        djview "http://localhost:5000/arkenproxyclient/simpleFetchDocument?archive=lm21&document=21-P90%3A90"
    """
    # djview 'http://localhost:8091/arken/djvu/v3.0/document/index.djvu?archive=k21g&id=2180k-10/11'
    archive = flask.request.args.get('archive') or flask.request.args.get('county')
    id_ = flask.request.args.get('document')
    r = flask.current_app.client.get_index_djvu(archive, id_)
    print_app_headers(r)
    if r.ok:
        return flask.Response(r.content, mimetype=r.headers['Content-Type'], status=r.status_code)
    else:
        print(r.headers)
        print(r.text)
        return flask.Response(r.content, mimetype=r.headers.get('Content-Type', ''), status=r.status_code)


@bp.route('/arkenproxyclient/page_<vers>_<subdoc>_<page>_<archive>_<enc_id>.djvu')
def get_page_djvu(vers, subdoc, page, archive, enc_id):
    """Request for a single page

    This is not the same as it was in ArkenProxy, these calls are based on the page filenames embedden in index.djvu
    and they are different in index.djvu received from Akt Direkt.

    to test this service use:
        djview 'http://localhost:5000/arkenproxyclient/page_1_1_1_k21g_MjE4MGstMTAvMTE=.djvu'
    """
    r = flask.current_app.client.get_page_djvu(vers, subdoc, page, archive, enc_id)
    print_app_headers(r)
    return flask.Response(r.content, mimetype=r.headers['Content-Type'], status=r.status_code)

def print_app_headers(r):
    """Print the application specific headers"""
    wanted_headers = ('Archive', 'Document-ID', 'Error-Code', 'Error-Message')
    headers = {k: v for (k, v) in r.headers.items() if k in wanted_headers}
    print('Headers received from Akt Direkt:', headers)

