from flask import Flask, render_template, request, redirect, url_for, make_response, session
from argon2 import PasswordHasher
import jwt
import datetime
import pytz
import uuid
import json


ph = PasswordHasher()
app = Flask(__name__)
SECRET_KEY = "123"

@app.route("/")
def index():
    return render_template('landingPage.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Quando o usuário apenas acessa a página /login via navegador
        return render_template('login.html')
        
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
    try:
        user = next((u for u in userRegistration if u['username'] == username), None)
        
        if not user:
            print("TESTE1")
            return render_template('login.html', error="Usuário ou senha incorreto")
        
        if not ph.verify(user['password'], password):
            print("TESTE2")
            return render_template('login.html', error="Usuário ou senha incorreto")
    except:
        print("TESTE3")
        return render_template('login.html', error="Usuário ou senha incorreto")

    # Gerando Token de acesso, usado para verificar a sessão do usuário
    payload = {
        "user_id":user['id'],
        "user_name":user['username'],
        "exp": datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=12) # Token expira em 12 hora
    }

    print("Gerando token")
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    print(token)

    # Armazenando o token em um cookie
    response = make_response(redirect(url_for('home')))
    response.set_cookie("auth_token", token)

    print("testando return")
    return response

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

        if confirmPassword != password:
            return render_template('register.html', error="As senhas não coincidem.")
        
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
                print("Usuário já está sendo utilizado")
                return render_template('register.html', error="Usuário já está sendo utilizado")
            

            user_id = str(uuid.uuid4())  # Gerando um UUID único
            hashadPassword = ph.hash(password)

            # Armazenando em um dicionário
            user_data = {
                "id":user_id,
                "username":username,
                "password":hashadPassword
            }

            users_data.append(user_data) # Adiciona o novo usuário

            # Inserindo usuário e senha no arquivo JSON
            with open("plataformaEducacaoDigital/data/users.json", "w", encoding="utf-8") as arquivo:
                json.dump(users_data, arquivo, indent=4, ensure_ascii=False)
                
            print(user_data)

            return render_template('login.html', error="Usuário cadastrado com sucesso!")
        else:
            print("Senha não contém nível de dificuldade suficiente")
            return render_template('register.html', error="Senha não possiu dificuldade mínima permitida")
                   
    return render_template('register.html')

@app.route("/home", methods=['GET', 'POST'])
def home():
    print("BEM VINDO, VOCÊ ESTÁ NA PÁGINA HOME")
    
    # Verificar se o token existe nos cookies
    token = request.cookies.get('auth_token')
    
    if token:
        try:
            jwt.decode(token, "123", algorithms=["HS256"])
            return render_template('home.html')
            
        except jwt.ExpiredSignatureError:
            return redirect(url_for('index', error="Sessão expirou. Faça login novamente."))
        except jwt.InvalidTokenError:
            return redirect(url_for('index', error="Token inválido."))
    else:
        return redirect(url_for('index', error="Você precisa estar logado para acessar esta página."))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=500, debug=True)
