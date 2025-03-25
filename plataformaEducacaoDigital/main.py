from flask import Flask, render_template, request, jsonify

import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def login():
    # Armazenando o usuário e senha na variavel
    username = request.form.get('username')
    password = request.form.get('password')
    print("Buscando credencial")

    try:
        with open("plataformaEducacaoDigital/data/users.json", "r", encoding="utf-8") as arquivo:
            userRegistration = json.load(arquivo)
    except FileNotFoundError:
        return render_template('login.html', error="Usuário não encontrado.")

    print("Validando credencial")
    if username != userRegistration.get("username") and password != userRegistration.get("password"):
        print("Senha ou usuário incorreto")
        return render_template('login.html', error="Senha ou usuário incorreto")
    
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')
        username = request.form.get('username')

        if confirmPassword == password:
            # Armazenando em um dicionário
            user_data = {
                "username":username,
                "password":password
            }

            with open("plataformaEducacaoDigital/data/users.json", "w", encoding="utf-8") as arquivo:
                json.dump(user_data, arquivo, indent=4, ensure_ascii=False)
            
            print(user_data)

            return render_template('login.html')
        
        elif confirmPassword != password:
            return render_template('register.html', error="As senhas não coincidem.")
                   

    return render_template('register.html')

@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=500)
