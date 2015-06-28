from flask import render_template, Response, jsonify
from .app import app
from rainbow.models.calendar.calendar import Calendar


@app.before_request
def preprocess_request():
  pass

@app.after_request
def postprocess_request(response):
  return response

@app.route('/')
def index_view():
  return render_template('index.html')

@app.route('/calendar/<id>.vcs')
def ics_calendar_view(id):
    calendar = Calendar.find(id)
    return Response(calendar.to_ical(), mimetype='text/calendar')

@app.route('/calendar/<id>.json')
def json_calendar_view(id):
    calendar = Calendar.find(id)
    return jsonify(calendar.to_dict())
