#!/bin/sh

#
# start the server (run this file) like this
#
#   pipenv run ./start.sh
#

export FLASK_APP=akt_direkt_proxy
export AKTDIREKT_ENV_FILE=config.cfg  # Fallback if no env variables are set
flask run --host=0.0.0.0
