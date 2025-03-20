from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/teste")
def teste():
    return "página dois"

if __name__ == '__main__':
    app.run(host='192.168.100.56', port=500)
