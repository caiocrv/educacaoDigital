from flask import Flask, render_template, request, redirect, url_for

import uuid
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
    if any(user['username'] == username for user in userRegistration) and any(keys['password'] == password for keys in userRegistration):
        print("Bem vindo")
        return render_template('home.html')
    else:
        print("Usuário ou senha incorreto")
        return render_template('login.html', error="Usuário ou senha incorreto")

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
                if character in "@#?!&":
                    characterSpecial += 1
                
                # Verificando a quantidade de caracteres maíusculo
                if character.isupper():
                    characterUpper += 1

            # Verificando dificuldade da senha
            if len(password) >= 6 and characterSpecial >= 1 and characterUpper >= 1:
                try:
                    with open("plataformaEducacaoDigital/data/users.json", "r", encoding="utf-8") as arquivo:
                        users_data = json.load(arquivo)
                except FileNotFoundError:
                    users_data = []

                if any(user['username'] == username for user in users_data):
                    print("Usuário já existe")
                    return render_template('register.html', error="Usuário já existe.")
                

                user_id = str(uuid.uuid4())  # Gerando um UUID único

                # Armazenando em um dicionário
                user_data = {
                    "id":user_id,
                    "username":username,
                    "password":password
                }

                users_data.append(user_data) # Adiciona o novo usuário

                # Inserindo usuário e senha no arquivo JSON
                with open("plataformaEducacaoDigital/data/users.json", "w", encoding="utf-8") as arquivo:
                    json.dump(users_data, arquivo, indent=4, ensure_ascii=False)
                
                print(user_data)

                return render_template('login.html')
            else:
                print("Senha não contém nível de dificuldade suficiente")
                return render_template('register.html', error="Senha não possiu dificuldade mínima permitida")

        else:
            return render_template('register.html', error="As senhas não coincidem.")
                   

    return render_template('register.html')

@app.route("/home", methods=['GET', 'POST'])
def home():
    print("BEM VINDO, VOCÊ ESTÁ NA PÁGINA HOME")
    return render_template('home.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=500, debug=True)
