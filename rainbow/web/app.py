from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask.ext import assets
import os, glob

app = Flask(__name__)
app.secret_key = os.environ.get('SK')
app.wsgi_app = ProxyFix(app.wsgi_app)
dev = os.environ.get('DEV') == 'true'

env = assets.Environment(app)
env.load_path = [os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)]

js = []
coffee = []
order = ['services', 'filters', 'directives', 'controllers']
for x in order:
  js.extend(glob.glob('rainbow/web/static/js/{}/*.js'.format(x)))
  coffee.extend(glob.glob('rainbow/web/static/js/{}/*.js.coffee'.format(x)))

coffee_bundle = assets.Bundle(*coffee, filters=['coffeescript'])
js.append(coffee_bundle)

css = glob.glob('rainbow/web/static/css/*.css')
less = glob.glob('rainbow/web/static/css/*.less')
less_bundle = assets.Bundle(*less, filters=['less'])
css.append(less_bundle)

js_filters = []
css_filters = []

if not dev:
  js_filters.append('rjsmin')
  css_filters.append('cssmin')

env.register('js_app', assets.Bundle('rainbow/web/static/js/app.js.coffee',
                                     filters=['coffeescript'] + js_filters,
                                     output='js/min/app.min.js'))
env.register('js_all', assets.Bundle(*js, filters=js_filters, output='js/min/scripts.min.js'))
env.register('css_all', assets.Bundle(*css, filters=css_filters, output='css/min/styles.min.css'))

from rainbow.web.routes import *

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=int(os.environ.get('PORT') or 5000), debug=dev)
