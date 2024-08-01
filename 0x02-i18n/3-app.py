#!/usr/bin/env python3
"""
Parametrize templates
"""
from flask import Flask, render_template
from flask_babel import Babel, _

app = Flask(__name__)

class Config:
    """Config class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(Config)
babel = Babel(app)

@babel.localeselector
def get_locale():
    """Get locale from request"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    """Parametrize templates"""
    return render_template('3-index.html')

if __name__ == '__main__':
    app.run()
