#!/usr/bin/env python3
"""
Force locale with URL parameter
"""
from flask import Flask, render_template, request
from flask_babel import Babel, _

app = Flask(__name__)


class Config:
    """
    Configuration class for Flask app
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    Determine the locale to use for this request.
    
    Checks the URL parameter 'locale' for a supported locale.
    If not present or not supported, fallback to the best match
    from the request's Accept-Language header.

    Returns:
        str: The locale to use.
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """
    Render the index page.
    
    Renders the '4-index.html' template.

    Returns:
        str: The rendered template.
    """
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(debug=True)
