from app import app
from flask import render_template, flash, redirect, session, url_for, request, g
from werkzeug.wsgi import SharedDataMiddleware
import os

@app.route('/')
@app.route('/index')
def index():
	url_for('static', filename='bootstrap/css/bootstrap.min.css')
	return render_template('index.html')


# these are all tests of the graphs before they get merged into the homepage
#TODO: delete
@app.route('/race-stops')
def race_stops():
	return render_template('race_stops.html')

@app.route('/total-stops')
def total_stops():
	return render_template('total_stops_map.html')

@app.route('/line-graph')
def  line_graph():
	return render_template('line-graph.html')

# store assets files on server for now
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
	'/': os.path.join(os.path.dirname(__file__), '/static')
})

