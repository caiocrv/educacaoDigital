# 💻 Plataforma de Educação Digital

Sistema simples de autenticação com **Flask**, utilizando **JWT**, **Argon2** para criptografia de senhas e arquivos HTML com renderização dinâmica.

---

## 📦 Requisitos

- Python 3.7+
- pip

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

### 2. Crie e ative um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

Ou, se preferir:

```bash
pip install Flask argon2-cffi PyJWT pytz
```

---

## 🧪 Como usar

### 1. Execute o servidor

```bash
python main.py
```

Acesse em: [http://localhost:5000](http://localhost:5000)

---

## 👥 Funcionalidades

- Cadastro com validação de senha (mínimo de 6 caracteres, 1 maiúscula e 1 caractere especial).
- Login com verificação de credenciais criptografadas.
- Geração de JWT para sessões seguras.
- Armazenamento de usuários em JSON.
- Validações front-end com JavaScript.

---

## 📁 Estrutura do Projeto

```
├── main.py                     # Backend Flask
├── plataformaEducacaoDigital
│   └── data
│       └── users.json          # Dados dos usuários
├── static
│   └── scripts.js              # Validação de senha no frontend
├── templates
│   ├── login.html              # Página de login
│   ├── register.html           # Página de cadastro
│   └── home.html               # Página protegida
├── requirements.txt            # Dependências do projeto
```

---

## 📌 Observações

- A chave secreta usada no JWT (`SECRET_KEY`) está hardcoded para fins de teste. Em produção, utilize variáveis de ambiente!
- O arquivo `users.json` é utilizado como banco de dados local apenas para fins didáticos.


