from flask import Flask
app = Flask(__name__)
import logging

app.secret_key = "secret recipes"


logging.basicConfig(filename='errors.log', level=logging.DEBUG)

