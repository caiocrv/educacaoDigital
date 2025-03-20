from flask import Flask, render_template, request, jsonify

import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['POST'])
def login():
    # Armazenando o usuário e senha na variavel
    username = request.form.get('username')
    password = request.form.get('password')

    # Armazenando em um dicionário
    user_data = {
        "username":username,
        "password":password
    }

    print(user_data)

    return jsonify(user_data)







if __name__ == '__main__':
    app.run(host='172.19.214.107', port=500)
