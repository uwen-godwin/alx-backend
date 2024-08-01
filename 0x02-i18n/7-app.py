#!/usr/bin/env python3
"""
Infer appropriate time zone
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _, format_datetime
import pytz
from datetime import datetime

app = Flask(__name__)

class Config:
    """Config class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(Config)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user():
    """Get user from users dictionary"""
    try:
        user_id = int(request.args.get('login_as'))
    except (TypeError, ValueError):
        return None
    return users.get(user_id)

@app.before_request
def before_request():
    """Set g.user"""
    g.user = get_user()

@babel.localeselector
def get_locale():
    """Get locale from request"""
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    user = g.get('user')
    if user and user['locale'] in app.config['LANGUAGES']:
        return user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@babel.timezoneselector
def get_timezone():
    """Get timezone from request"""
    timezone = request.args.get('timezone')
    if timezone:
        try:
            return pytz.timezone(timezone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    user = g.get('user')
    if user and user['timezone']:
        try:
            return pytz.timezone(user['timezone']).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    return app.config['BABEL_DEFAULT_TIMEZONE']

@app.route('/')
def index():
    """Infer appropriate time zone"""
    current_time = format_datetime(datetime.now())
    return render_template('7-index.html', current_time=current_time)

if __name__ == '__main__':
    app.run()
