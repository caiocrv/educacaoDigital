from flask import Flask, render_template, request, jsonify

import json
import unicodedata

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def login():
    # Armazenando o usuário e senha na variavel
    username = request.form.get('username')
    password = request.form.get('password')

    # Lendo arquivo JSON
    try:
        with open("plataformaEducacaoDigital/data/users.json", "r", encoding="utf-8") as arquivo:
            userRegistration = json.load(arquivo)
    except FileNotFoundError:
        return render_template('login.html', error="Usuário não encontrado.")

    # Validando credencial
    if username != userRegistration.get("username") or password != userRegistration.get("password"):
        return render_template('login.html', error="Senha ou usuário incorreto")
    
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():

    # Se tiver metodo "POST" no HTML, executa
    if request.method == 'POST':
        # Armazenando a usuário e senha do FORM
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')
        username = request.form.get('username')

        # Validando senha
        characterSpecial = 0
        characterUpper = 0

        if confirmPassword == password:
            for character in password:
                # Verificando se a senha tem backspace
                if character.isspace():
                    print("Senha não pode conter espaço")
                    return render_template('register.html', error="Senha não pode conter espaço.")
                
                # Verificando a quantidade de caracteres especiais na senha
                elif character == "@" or character == "#" or character == "?" or character == "!" or character == "&":
                    characterSpecial += 1
                
                # Verificando a quantidade de caracteres maíusculo
                elif character.isupper():
                    characterUpper += 1

            # Verificando quantidade de caracteres na senha
            qtdCharacter = sum(1 for _ in password)

            if characterSpecial >= 1 and qtdCharacter >= 6 and characterUpper >= 1:
                # Armazenando em um dicionário
                user_data = {
                    "username":username,
                    "password":password
                }

                # Inserindo usuário e senha no arquivo JSON
                with open("plataformaEducacaoDigital/data/users.json", "w", encoding="utf-8") as arquivo:
                    json.dump(user_data, arquivo, indent=4, ensure_ascii=False)
                
                print(user_data)

                return render_template('login.html')
            else:
                print("Senha não contém nível de dificuldade suficiente")
                return render_template('register.html', error="As senhas não coincidem.")

        else:
            return render_template('register.html', error="As senhas não coincidem.")
                   

    return render_template('register.html')

@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=500, debug=True)
