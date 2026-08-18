# from dbm import sqlite3

from flask import Flask

from database import db
from models.user import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"


# Session <- conexao ativa - abrir e fechar a sessao
# Banco relacional - Banco que armazena informacoes em tabelas e elas se relacionam entre si

db.init_app(app)


@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello world"


if __name__ == "__main__":
    app.run(debug=True)
