# from dbm import sqlite3

from flask import Flask, jsonify, request
from flask_login import LoginManager

from database import db
from models.user import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"


login_manager = LoginManager()

# Session <- conexao ativa - abrir e fechar a sessao
# Banco relacional - Banco que armazena informacoes em tabelas e elas se relacionam entre si


# Iniciao junto com o App
db.init_app(app)
login_manager.init_app(app)


# view login


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        pass

    return jsonify({"message": "credenciais invalidas"}), 400


@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello world"


if __name__ == "__main__":
    app.run(debug=True)
