from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from argon2 import PasswordHasher
import jwt
import datetime
import pytz
import uuid
import json


ph = PasswordHasher()
app = Flask(__name__)
SECRET_KEY = "123"

@app.route("/", methods=['GET'])
def index():
    return render_template('landingPage.html')

@app.route("/landingPage", methods=['GET'])
def landingPage():
    if request.method == 'GET':
        # Quando o usuário apenas acessa a página /landingPage via navegador
        return render_template('landingPage.html')

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

        # Validando username
        for character in username:
            # Verificando se o username tem espaço
            if character.isspace():
                print("Usuário não pode conter espaço")
                return render_template('register.html', error="Usuário não pode conter espaço.")
            
            # Verificando caracteres no username 
            ascii_code = ord(character)
            if not (97 <= ascii_code <= 122 or ascii_code in (95, 46)):
                print("O usuário pode conter apenas letras minúsculas e '_' ou '.'")
                return render_template('register.html', error="Usuário só pode conter letras minúsculas, _ ou .")

        # Validando password
        if confirmPassword != password:
            return render_template('register.html', error="As senhas não coincidem.")
        
        for character in password:
            # Verificando se a senha tem backspace
            if character.isspace():
                print("Senha não pode conter espaço")
                return render_template('register.html', error="Senha não pode conter espaço.")
            
            # Verificando a quantidade de caracteres especiais na senha
            if character in "@#?!&$":
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
            return render_template('register.html', error="Senha não possiu dificuldade mínima permitida. Utilize letras maiúsculas, número e caractere especial (@, $, #, ?, !, &)")
                   
    return render_template('register.html')

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
            return render_template('login.html', error="Usuário ou senha incorreto")
        
        if not ph.verify(user['password'], password):
            return render_template('login.html', error="Usuário ou senha incorreto")
    except:
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

    return response

@app.route("/home", methods=['GET', 'POST'])
def home():
    print("BEM VINDO, VOCÊ ESTÁ NA PÁGINA HOME")
    
    # Verificar se o token existe nos cookies
    token = request.cookies.get('auth_token')
    
    if token:
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return render_template('home.html')
            
        except jwt.ExpiredSignatureError:
            return redirect(url_for('index', error="Sessão expirou. Faça login novamente."))
        except jwt.InvalidTokenError:
            return redirect(url_for('index', error="Token inválido."))
    else:
        return redirect(url_for('index', error="Você precisa estar logado para acessar esta página."))

@app.route("/quizPython", methods=['GET'])
def quizPython():
    token = request.cookies.get('auth_token')

    if not token:
        return redirect(url_for('index', error="Não autenticado"))

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
    except jwt.ExpiredSignatureError:
        return redirect(url_for('index', error="Token expirado"))
    except jwt.InvalidTokenError:
        return redirect(url_for('index', error="Token expirado"))
    
    if request.method == 'GET':
        # Quando o usuário apenas acessa a página /quizPython via navegador
        return render_template('quizPython.html')
    
    dados = request.get_json()
    acertosQuizPython = dados.get("acertos", 0)

    with open("plataformaEducacaoDigital/data/users.json", "r", encoding="utf-8") as arquivo:
        usuarios = json.load(arquivo)

    for usuario in usuarios:
        if usuario["id"] == user_id:
            usuario["hitQuizPython"]  = acertosQuizPython
            break

    with open("plataformaEducacaoDigital/data/users.json", "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

    return {"mensagem": "Acertos salvos com sucesso"}

@app.route("/quizCybersecurity", methods=['GET'])
def quizCybersecurity():
    token = request.cookies.get('auth_token')

    if not token:
        return redirect(url_for('index', error="Não autenticado"))

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
    except jwt.ExpiredSignatureError:
        return redirect(url_for('index', error="Token expirado"))
    except jwt.InvalidTokenError:
        return redirect(url_for('index', error="Token expirado"))

    if request.method == 'GET':
        # Quando o usuário apenas acessa a página /quizCybersecurity via navegador
        return render_template('quizCybersecurity.html')
    
    dados = request.get_json()
    acertosQuizCybersecurity = dados.get("acertos", 0)

    with open("plataformaEducacaoDigital/data/users.json", "r", encoding="utf-8") as arquivo:
        usuarios = json.load(arquivo)

    for usuario in usuarios:
        if usuario["id"] == user_id:
            usuario["hitQuizCybersecurity"]  = acertosQuizCybersecurity
            break

    with open("plataformaEducacaoDigital/data/users.json", "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

    return {"mensagem": "Acertos salvos com sucesso"}

@app.route("/saveReviews", methods=["POST"])
def saveReviews():
    token = request.cookies.get('auth_token')

    if not token:
        return redirect(url_for('index', error="Não autenticado"))

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
        username = payload["user_name"]
    except jwt.ExpiredSignatureError:
        return redirect(url_for('index', error="Token expirado"))
    except jwt.InvalidTokenError:
        return redirect(url_for('index', error="Token expirado"))

    dados = request.get_json()
    quiz = dados.get("quiz")
    acertos = dados.get("acertos")
    total = dados.get("total")
    data = dados.get("data")

    if not all([quiz, acertos, total, data]):
        return {"error": "Dados incompletos"}, 400

    caminho = "plataformaEducacaoDigital/data/avaliacoes.json"
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            usuarios = json.load(arquivo)
    except FileNotFoundError:
        usuarios = []

    for user in usuarios:
        if user["user_id"] == user_id:
            user["avaliacoes"].append({
                "quiz": quiz,
                "acertos": acertos,
                "total": total,
                "data": data
            })
            break
    else:
        usuarios.append({
            "user_id": user_id,
            "username": username,
            "avaliacoes": [{
                "quiz": quiz,
                "acertos": acertos,
                "total": total,
                "data": data
            }]
        })

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

    return {"mensagem": "Avaliação salva com sucesso"}

@app.route('/graphicData')
def graphicData():
    token = request.cookies.get('auth_token')

    if not token:
        return redirect(url_for('index', error="Não autenticado"))

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
    except jwt.ExpiredSignatureError:
        return redirect(url_for('index', error="Token expirado"))
    except jwt.InvalidTokenError:
        return redirect(url_for('index', error="Token expirado"))

    caminho = "plataformaEducacaoDigital/data/avaliacoes.json"
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            usuarios = json.load(arquivo)
    except FileNotFoundError:
        return {"media": 0, "porQuiz": {}}

    for user in usuarios:
        if user["user_id"] == user_id:
            avals = user.get("avaliacoes", [])
            if not avals:
                return {"media": 0, "porQuiz": {}}

            total_acertos = 0
            total_questoes = 0
            por_quiz = {}

            for a in avals:
                total_acertos += a["acertos"]
                total_questoes += a["total"]

                if a["quiz"] not in por_quiz:
                    por_quiz[a["quiz"]] = {"acertos": 0, "total": 0}
                por_quiz[a["quiz"]]["acertos"] += a["acertos"]
                por_quiz[a["quiz"]]["total"] += a["total"]

            media = round((total_acertos / total_questoes) * 100, 2)
            return jsonify({"media": media, "porQuiz": por_quiz})

    return {"media": 0, "porQuiz": {}}

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    response = make_response(redirect(url_for("landingPage")))
    response.set_cookie("auth_token", "", expires=0)

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=500, debug=True)
