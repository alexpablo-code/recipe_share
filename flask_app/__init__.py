import logging
from flask import Flask
app = Flask(__name__)

app.secret_key = "secret recipes"


logging.basicConfig(filename='errors.log', level=logging.ERROR)

logging.basicConfig(filename='info.log', level=logging.INFO)
