"""Entrypoint for running the Flask app with the flask CLI."""
from . import create_app

app = create_app()
