import logging
from flask import Flask
app = Flask(__name__)

app.secret_key = "secret recipes"


logging.basicConfig(filename='record.log', level=logging.ERROR)
