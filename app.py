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
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://admin:admin123@127.0.0.1:3306/flask-crud"
)


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
        user = User(username=username, password=password, role="user")
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "usuario cadastrado com sucesso"})
    return jsonify({"message": "Dados invalidos"}), 401


@app.route("/user/<int:id_user>", methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return {"username": user.username}
    return jsonify({"message": "usuario nao encontrado"}), 404


@app.route("/user/<int:id_user>", methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role == "user":
        return jsonify({"message": "O Usuario nao tem permissao"}), 403

    if not data:
        return jsonify({"message": "JSON nao enviado"}), 400

    user = User.query.get(id_user)

    if not user:
        return jsonify({"message": "Usuario nao encontrado"}), 404

    password = data.get("password")

    if not password:
        return jsonify({"message": "Senha nao enviada"}), 400

    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()
        return {"username": f" Usuario {id_user} atualizado com sucesso"}
    return jsonify({"message": "usuario nao encontrado"}), 404


@app.route("/user/<int:id_user>", methods=["DELETE"])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if current_user.role != "admin":
        return jsonify({"message": "Operacao nao permitida"})
    if id_user == current_user.id:
        return jsonify({"message": "Delecao nao permitida"}), 403

    if user and id_user != current_user.id:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"O usuario {id_user} foi deletado com sucessos"})

    return jsonify({"message": "Erro ao deletar o usuario"}), 404


if __name__ == "__main__":
    app.run(debug=True)
