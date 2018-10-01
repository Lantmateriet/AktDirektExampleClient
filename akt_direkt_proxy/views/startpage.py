"""User interface of the example application"""

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

bp = flask.Blueprint('user_interface', __name__, url_prefix='/')

@bp.route('/')
@bp.route('/index.html')
def index():
    """Generate the startpage with form for generation dossier URLs"""
    test_result = flask.current_app.client.test_connection()
    return flask.render_template('startpage.html', test_result=test_result)

@bp.route('/index_url')
def index_url():
    """Generate a dossier URL"""
    archive = flask.request.args.get('archive')
    document_id = flask.request.args.get('document_id')
    index_url = flask.url_for('proxy.get_index_djvu', archive=archive, id=document_id, _external=True)
    return flask.render_template('index_url.html', index_url=index_url)
