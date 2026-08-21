# from dbm import sqlite3


from flask import Flask, jsonify, request
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

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

login_manager.login_view = "login"  # type: ignore


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    assert data is not None
    username = data.get("username")
    password = data.get("password")

    if username and password:
        # Login

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "Autenticacao realizada com sucesso"})
        return jsonify({"message": "Autenticacao realizada com sucesso"})

    return jsonify({"message": "credenciais invalidas"}), 400


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"mesage": "Logout realizado com sucesso!"})


@app.route("/user", methods=["POST"])
def create_user():
    data = request.json

    assert data is not None
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "usuario cadastrado com sucesso"})
    return jsonify({"message": "Dados invalidos"}), 401


@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello world"


if __name__ == "__main__":
    app.run(debug=True)
