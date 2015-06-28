#!/bin/bash

if [ "$DEV" == "true" ]
then
  DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
  export PYTHONPATH="$PYTHONPATH:$DIR"
  python rainbow/web/app.py
else
  gunicorn -b "0.0.0.0:$PORT" --workers $WEB_CONCURRENCY rainbow.web.app:app
fi
