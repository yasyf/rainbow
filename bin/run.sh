#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export PYTHONPATH="$PYTHONPATH:$DIR"

if [ "$DEV" == "true" ]
then
  python rainbow/web/app.py
else
  python rainbow/helpers/threads.py &
  gunicorn -b "0.0.0.0:$PORT" --workers $WEB_CONCURRENCY rainbow.web.app:app
fi
