from app import app
from flask import render_template, flash, redirect, session, url_for, request, g

@app.route('/')
@app.route('/index')
def index():
	url_for('static', filename='bootstrap/css/bootstrap.min.css')
	return render_template('index.html')

