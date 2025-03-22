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

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        if confirmPassword != password:
            return render_template('cadastro.html', error="As senhas não coincidem.")

        return jsonify({"massege": "Cadastro realizado com sucesso!"})
    
    return render_template('cadastro.html')






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=500)
