#!/usr/bin/env python3
"""
Basic Flask app with Babel, locale selection, forced locale via URL parameter, mock user login, and timezone support
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from datetime import datetime
import pytz

app = Flask(__name__)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

class Config:
    """Config class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(Config)
babel = Babel(app)

def get_user():
    """Mock user login"""
    user_id = request.args.get('login_as')
    if user_id:
        return users.get(int(user_id))
    return None

@app.before_request
def before_request():
    """Before request handler"""
    g.user = get_user()

@babel.localeselector
def get_locale():
    """Get the best match for supported languages"""
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@babel.timezoneselector
def get_timezone():
    """Get the best match for timezones"""
    timezone = request.args.get('timezone')
    if timezone:
        return timezone
    if g.user and g.user['timezone']:
        return g.user['timezone']
    return app.config['BABEL_DEFAULT_TIMEZONE']

@app.route('/')
def index():
    """ Basic route """
    user_timezone = get_timezone()
    current_time = datetime.now(pytz.timezone(user_timezone))
    formatted_time = current_time.strftime('%b %d, %Y, %I:%M:%S %p')
    return render_template('index.html', current_time=formatted_time)

if __name__ == '__main__':
    app.run()
