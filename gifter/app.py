from functools import wraps
from flask import Flask, session, g, request, redirect, url_for, flash, jsonify, render_template
import gifter.db # initialize db
from gifter.db.models import *
import gifter.config as config

gifter.db.map()

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


def require_auth(f):
	''' decorator for all pages that require auth '''
	@wraps(f)
	@db_session
	def decorated_function(*args, **kwargs):
		if "admin_id" not in session:
			return redirect(url_for('login', next=request.url))
		else:
			app.logger.info("admin id {}".format(session["admin_id"]))
			g.admin = AdminUser.get(id=session["admin_id"])
		return f(*args, **kwargs)
	return decorated_function


@app.route('/')
def index():
	return redirect(url_for('admin'))

@app.route('/admin')
@require_auth
def admin():
    logs = ActionLog.last_100_actions()
    return render_template("admin.html", logs = logs)


@app.route('/user_search?term=<term>')
@require_auth
def user_search(term):
	results = PublicUser.search(term, limit=10)

	# convert to an array of {'label':str(user), 'value':user.id}, needed for jquery autocomplete

	json_results = map(lambda u: {'label':str(u), 'value':u.id}, results)

	return jsonify(json_results)




@app.route('/login', methods=['GET', 'POST'])
@db_session
def login():

	
	if config.is_production():
		#TODO do SAML login
		raise NotImplementedError

	if request.method == "GET":
		return render_template('login.html')


	if not request.form.get("username"):
		flash("username expected")
		return render_template('login.html')

	admin = AdminUser.find_or_create_by_username(request.form["username"])
	admin.log_login() # create action log of login
	session["admin_id"] = admin.id
	return redirect(url_for('admin'))

@app.route('/logout')
@require_auth
def logout():

	if config.is_production():
		#TODO do SAML login
		raise NotImplementedError

	g.admin = None

	session["admin_id"] = None

	render_template("logout.html")


app.run()
	




