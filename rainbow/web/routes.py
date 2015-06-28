from flask import render_template, Response, jsonify, request
from .app import app
from rainbow.helpers.threads import Pooler, parse_calendar
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

@app.route('/api/calendar', methods=['POST'])
def api_create_view():
    calendar = Calendar.from_url(request.form['url'], request.form['type'])
    _id = calendar.save()
    user_geo = (request.form.get('lat'), request.form.get('lng'))
    Pooler.submit(parse_calendar, request.form['type'], request.form['url'], user_geo)
    return jsonify({'status': 'success', 'id': str(_id)})

@app.route('/api/calendar/<_id>.ics')
def ics_calendar_view(_id):
    calendar = Calendar.find(_id)
    return Response(calendar.to_ical(), mimetype='text/calendar')

@app.route('/api/calendar/<_id>.json')
def json_calendar_view(_id):
    calendar = Calendar.find(_id)
    return jsonify(calendar.to_dict())
