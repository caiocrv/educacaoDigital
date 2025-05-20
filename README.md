# 📚 DevStart - Plataforma de Inclusão Digital

A **DevStart** é uma plataforma web educacional gratuita, desenvolvida com o objetivo de promover a **inclusão digital** por meio de conteúdos introdutórios e práticos em **programação**, **HTML**, **cibersegurança** e **lógica de programação**.

## 🎯 Objetivo

Oferecer um ambiente acessível e seguro onde usuários iniciantes possam:
- Criar uma conta de forma simples e segura
- Realizar quizzes temáticos
- Acompanhar sua evolução com gráficos de desempenho
- Ter seus dados protegidos conforme os princípios da **LGPD** e **boas práticas de cibersegurança**

---

## ⚙️ Tecnologias Utilizadas

- **Back-end:** Flask (Python)
- **Front-end:** HTML5, CSS3, JavaScript
- **Banco de Dados:** Arquivos JSON
- **Segurança:**
  - Senhas criptografadas com Argon2
  - Autenticação via JWT armazenado em cookies
  - Validações de senha e usuário
- **Gráficos:** Chart.js

---

## 🧩 Funcionalidades

- ✅ Registro e login com autenticação segura
- ✅ Página inicial de boas-vindas (Landing Page)
- ✅ Interface de usuário responsiva
- ✅ Validação de senhas seguras (mínimo 6 caracteres, maiúsculas, especiais)
- ✅ Quizzes interativos:
  - Python
  - Lógica de Programação
  - HTML
  - Cibersegurança
- ✅ Armazenamento das respostas dos quizzes
- ✅ Dashboard com gráficos:
  - Média geral de acertos
  - Acertos por quiz
- ✅ Logout e expiração de sessão

---

## 🧪 Estrutura do Projeto

```

plataformaEducacaoDigital/
│
├── static/                      # Arquivos de imagem, CSS e JS
│
├── templates/                   # Arquivos HTML (views)
│   ├── landingPage.html
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   ├── quizPython.html
│   ├── quizCybersecurity.html
│   └── ...
│
├── data/                        # "Banco de dados" em JSON
│   ├── users.json
│   └── avaliacoes.json
│
├── main.py                      # Arquivo principal da aplicação Flask
└── README.md                    # (Este arquivo)

````

---

## 🚀 Como Executar Localmente

### Pré-requisitos

- Python 3.10+
- Pip

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/plataformaEducacaoDigital.git
cd plataformaEducacaoDigital
````

2. Instale as dependências:

```bash
pip install flask argon2-cffi pyjwt pytz
```

3. Execute o servidor Flask:

```bash
python main.py
```

4. Acesse via navegador:

```
http://localhost:5000
```

---

## 🛡️ Segurança e LGPD

* Todas as senhas são **criptografadas** com **Argon2**.
* Autenticação baseada em **JWT** com expiração de 12h.
* Nenhum dado sensível é armazenado em texto puro.
* Armazenamento em arquivos locais JSON — ideal para prototipagem segura sem banco de dados.

---

## 📈 Exemplo de Gráficos

Os dados de desempenho são visualizados via **Chart.js**:

* **Gráfico 1**: Acertos por quiz
* **Gráfico 2**: Média de acertos (última tentativa de cada quiz)

---

## 👨‍💻 Autor

Desenvolvido por Caio (https://github.com/caiocrv) e Khimberlly (https://github.com/khiml) como projeto integrador do curso de **Análise e Desenvolvimento de Sistemas**.

---

## 📄 Licença

Este projeto é livre para fins educacionais. Sinta-se à vontade para usar, modificar e contribuir.

---

## 💡 Contato

Caio Gomes Carvalho
* 💼 LinkedIn: [https://linkedin.com/in/caiocrv](https://linkedin.com/in/caiocrv)