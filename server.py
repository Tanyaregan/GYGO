

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, Character, Title, Episode
# from model import EpChar, TitleChar

app = Flask(__name__)

app.secret_key = "SEEKRIT"

app.jinja_env.undefined = StrictUndefined




# if __name__ == "__main__":
#     # We have to set debug=True here, since it has to be True at the
#     # point that we invoke the DebugToolbarExtension
#     app.debug = True
#     app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

#     connect_to_db(app)

#     # Use the DebugToolbar
#     DebugToolbarExtension(app)

#     app.run(port=5000, host='0.0.0.0')
