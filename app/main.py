from flask import Flask, request, jsonify #type: ignore
from flask_cors import CORS #type: ignore
from controllers.controller import prod

app = Flask(__name__)

app.register_blueprint(prod, url_prefix="/product")

CORS(app, origins=['*'])

if __name__ == "__main__":
    app.run(debug=True)