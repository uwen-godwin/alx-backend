# i18n Project

This project demonstrates the use of internationalization (i18n) in a Flask web application using Flask-Babel.

## Setup

1. Clone the repository.
2. Install the required dependencies:
    ```bash
    $ pip install Flask Flask-Babel
    ```
3. Run the desired app:
    ```bash
    $ export FLASK_APP=0-app.py
    $ flask run
    ```
   Replace `0-app.py` with `1-app.py`, `2-app.py`, etc., for each task.

## Tasks

### Task 0: Basic Flask App
- `0-app.py`
- `templates/0-index.html`

### Task 1: Basic Babel Setup
- `1-app.py`
- `templates/1-index.html`

### Task 2: Get Locale from Request
- `2-app.py`
- `templates/2-index.html`

### Task 3: Parametrize Templates
- `3-app.py`
- `templates/3-index.html`
- `babel.cfg`
- `translations/en/LC_MESSAGES/messages.po`
- `translations/fr/LC_MESSAGES/messages.po`

### Task 4: Force Locale with URL Parameter
- `4-app.py`
- `templates/4-index.html`

### Task 5: Mock Logging In
- `5-app.py`
- `templates/5-index.html`

### Task 6: Use User's Time Zone
- `6-app.py`
- `templates/6-index.html`

### Task 7: Infer Appropriate Time Zone
- `7-app.py`
- `templates/7-index.html`

## Translations

To manage translations:
1. Extract messages:
    ```bash
    $ pybabel extract -F babel.cfg -o messages.pot .
    ```
2. Initialize new languages:
    ```bash
    $ pybabel init -i messages.pot -d translations -l en
    $ pybabel init -i messages.pot -d translations -l fr
    ```
3. Compile translations:
    ```bash
    $ pybabel compile -d translations
    ```

## License

This project is licensed under the MIT License.
