"""Tweet Generator"""
from jinja2 import StrictUndefined
from flask import (Flask, render_template, request,)
from flask_debugtoolbar import DebugToolbarExtension
from tweet import generate_user_tweets

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

#Raise error for variables in Jinja2
app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=["GET"])
def display_homepage():
    """display homepage and tweet form"""
    display_tweet = None
    username = request.args.get("username")
    if username:
        display_tweet = generate_user_tweets(username)
    return render_template('index.html', username=username, display_tweet=display_tweet)


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    app.run(port=5000, host='0.0.0.0')
