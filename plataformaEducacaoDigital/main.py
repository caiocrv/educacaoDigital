from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from argon2 import PasswordHasher
import jwt
import datetime
import pytz
import uuid
import json
import secrets


ph = PasswordHasher()
app = Flask(__name__)
SECRET_KEY = secrets.token_urlsafe(50)

@app.route("/", methods=['GET'])
def index():
    return render_template('landingPage.html')

@app.route("/landingPage", methods=['GET'])
def landingPage():
    if request.method == 'GET':
        return render_template('landingPage.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')
        username = request.form.get('username')

        characterSpecial = 0
        characterUpper = 0

        for character in username:
            if character.isspace():
                return render_template('register.html', error="Usuário não pode conter espaço.")
            
            ascii_code = ord(character)
            if not (97 <= ascii_code <= 122 or ascii_code in (95, 46)):
                return render_template('register.html', error="Usuário só pode conter letras minúsculas, _ ou .")

        if confirmPassword != password:
            return render_template('register.html', error="As senhas não coincidem.")
        
        for character in password:
            if character.isspace():
                return render_template('register.html', error="Senha não pode conter espaço.")
            
            if character in "@#?!&$":
                characterSpecial += 1
            
            if character.isupper():
                characterUpper += 1

        if len(password) >= 6 and characterSpecial >= 1 and characterUpper >= 1:
            try:
                with open("plataformaEducacaoDigital/data/users.json", "r", encoding="utf-8") as arquivo:
                    users_data = json.load(arquivo)
            except FileNotFoundError:
                users_data = []

            if any(user['username'] == username for user in users_data):
                return render_template('register.html', error="Usuário já está sendo utilizado")
            

            user_id = str(uuid.uuid4())
            hashadPassword = ph.hash(password)

            user_data = {
                "id":user_id,
                "username":username,
                "password":hashadPassword
            }

            users_data.append(user_data)

            with open("plataformaEducacaoDigital/data/users.json", "w", encoding="utf-8") as arquivo:
                json.dump(users_data, arquivo, indent=4, ensure_ascii=False)
                
            print(user_data)

            return render_template('login.html', error="Usuário cadastrado com sucesso!")
        else:
            return render_template('register.html', error="Senha não possiu dificuldade mínima permitida. Utilize letras maiúsculas, número e caractere especial (@, $, #, ?, !, &)")
                   
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
        
    username = request.form.get('username')
    password = request.form.get('password')

    try:
        with open("plataformaEducacaoDigital/data/users.json", "r", encoding="utf-8") as arquivo:
            userRegistration = json.load(arquivo)
    except FileNotFoundError:
        return render_template('login.html', error="Usuário não encontrado.")

    try:
        user = next((u for u in userRegistration if u['username'] == username), None)
        
        if not user:
            return render_template('login.html', error="Usuário ou senha incorreto")
        
        if not ph.verify(user['password'], password):
            return render_template('login.html', error="Usuário ou senha incorreto")
    except:
        return render_template('login.html', error="Usuário ou senha incorreto")

    payload = {
        "user_id":user['id'],
        "user_name":user['username'],
        "exp": datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=12) # Token expira em 12 hora
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    response = make_response(redirect(url_for('home')))
    response.set_cookie("auth_token", token)

    return response

@app.route("/home", methods=['GET', 'POST'])
def home():    
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

@app.route("/quizLogic", methods=['GET'])
def quizLogic():
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
        return render_template('quizLogic.html')
    
    dados = request.get_json()
    acertosQuizLogic = dados.get("acertos", 0)

    with open("plataformaEducacaoDigital/data/users.json", "r", encoding="utf-8") as arquivo:
        usuarios = json.load(arquivo)

    for usuario in usuarios:
        if usuario["id"] == user_id:
            usuario["hitQuizLogic"]  = acertosQuizLogic
            break

    with open("plataformaEducacaoDigital/data/users.json", "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

    return {"mensagem": "Acertos salvos com sucesso"}

@app.route("/quizHtml", methods=['GET'])
def quizHtml():
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
        return render_template('quizHtml.html')
    
    dados = request.get_json()
    acertosQuizHtml = dados.get("acertos", 0)

    with open("plataformaEducacaoDigital/data/users.json", "r", encoding="utf-8") as arquivo:
        usuarios = json.load(arquivo)

    for usuario in usuarios:
        if usuario["id"] == user_id:
            usuario["hitQuizHtml"]  = acertosQuizHtml
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

            por_quiz = {}
            for a in reversed(avals):
                quiz = a["quiz"]
                if quiz not in por_quiz:
                    por_quiz[quiz] = {
                        "acertos": a["acertos"],
                        "total": a["total"]
                    }

            porcentagens = []
            for q in por_quiz.values():
                if q["total"] > 0:
                    porcentagens.append((q["acertos"] / q["total"]) * 100)

            media = round(sum(porcentagens) / len(porcentagens), 2) if porcentagens else 0
            return jsonify({"media": media, "porQuiz": por_quiz})

    return {"media": 0, "porQuiz": {}}

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    response = make_response(redirect(url_for("landingPage")))
    response.set_cookie("auth_token", "", expires=0)

    return response



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=500, debug=True)