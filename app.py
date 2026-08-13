from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import hashlib
import json
import re
import uuid


HOST = "localhost"
PORT = 8000

users = {}
sessions = {}


def json_response(handler, status, data):
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def public_user(user):
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
    }


def parse_json(handler):
    content_length = int(handler.headers.get("Content-Length", 0))
    if content_length == 0:
        return {}

    raw_body = handler.rfile.read(content_length)
    try:
        return json.loads(raw_body.decode("utf-8"))
    except json.JSONDecodeError:
        raise ValueError("JSON inválido")


def get_logged_user(handler):
    auth_header = handler.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "", 1).strip()
    user_id = sessions.get(token)
    if not user_id:
        return None

    return users.get(user_id)


def find_user_by_email(email):
    for user in users.values():
        if user["email"].lower() == email.lower():
            return user
    return None


class AuthAPIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/health":
            return json_response(self, 200, {"status": "ok"})

        if path == "/users/me":
            logged_user = get_logged_user(self)
            if not logged_user:
                return json_response(self, 401, {"message": "Token ausente ou inválido"})

            return json_response(self, 200, public_user(logged_user))

        match = re.fullmatch(r"/users/([a-zA-Z0-9-]+)", path)
        if match:
            logged_user = get_logged_user(self)
            if not logged_user:
                return json_response(self, 401, {"message": "Token ausente ou inválido"})

            user_id = match.group(1)
            user = users.get(user_id)
            if not user:
                return json_response(self, 404, {"message": "Usuário não encontrado"})

            if logged_user["id"] != user_id:
                return json_response(self, 403, {"message": "Você só pode acessar seu próprio usuário"})

            return json_response(self, 200, public_user(user))

        return json_response(self, 404, {"message": "Rota não encontrada"})

    def do_POST(self):
        path = urlparse(self.path).path

        try:
            data = parse_json(self)
        except ValueError as error:
            return json_response(self, 400, {"message": str(error)})

        if path == "/users":
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")

            if not name or not email or not password:
                return json_response(self, 400, {"message": "Informe name, email e password"})

            if find_user_by_email(email):
                return json_response(self, 409, {"message": "E-mail já cadastrado"})

            user_id = str(uuid.uuid4())
            user = {
                "id": user_id,
                "name": name,
                "email": email,
                "password": hash_password(password),
            }
            users[user_id] = user

            return json_response(self, 201, {"message": "Usuário criado com sucesso", "user": public_user(user)})

        if path == "/auth/login":
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return json_response(self, 400, {"message": "Informe email e password"})

            user = find_user_by_email(email)
            if not user or user["password"] != hash_password(password):
                return json_response(self, 401, {"message": "E-mail ou senha inválidos"})

            token = str(uuid.uuid4())
            sessions[token] = user["id"]

            return json_response(self, 200, {"message": "Login realizado com sucesso", "token": token, "user": public_user(user)})

        if path == "/auth/logout":
            auth_header = self.headers.get("Authorization", "")
            token = auth_header.replace("Bearer ", "", 1).strip() if auth_header.startswith("Bearer ") else ""

            if not token or token not in sessions:
                return json_response(self, 401, {"message": "Token ausente ou inválido"})

            del sessions[token]
            return json_response(self, 200, {"message": "Logout realizado com sucesso"})

        return json_response(self, 404, {"message": "Rota não encontrada"})

    def do_PUT(self):
        path = urlparse(self.path).path
        match = re.fullmatch(r"/users/([a-zA-Z0-9-]+)", path)
        if not match:
            return json_response(self, 404, {"message": "Rota não encontrada"})

        logged_user = get_logged_user(self)
        if not logged_user:
            return json_response(self, 401, {"message": "Token ausente ou inválido"})

        user_id = match.group(1)
        if logged_user["id"] != user_id:
            return json_response(self, 403, {"message": "Você só pode atualizar seu próprio usuário"})

        try:
            data = parse_json(self)
        except ValueError as error:
            return json_response(self, 400, {"message": str(error)})

        user = users.get(user_id)
        if not user:
            return json_response(self, 404, {"message": "Usuário não encontrado"})

        if "email" in data and find_user_by_email(data["email"]) and data["email"].lower() != user["email"].lower():
            return json_response(self, 409, {"message": "E-mail já cadastrado"})

        if "name" in data:
            user["name"] = data["name"]
        if "email" in data:
            user["email"] = data["email"]
        if "password" in data:
            user["password"] = hash_password(data["password"])

        return json_response(self, 200, {"message": "Usuário atualizado com sucesso", "user": public_user(user)})

    def do_DELETE(self):
        path = urlparse(self.path).path
        match = re.fullmatch(r"/users/([a-zA-Z0-9-]+)", path)
        if not match:
            return json_response(self, 404, {"message": "Rota não encontrada"})

        logged_user = get_logged_user(self)
        if not logged_user:
            return json_response(self, 401, {"message": "Token ausente ou inválido"})

        user_id = match.group(1)
        if logged_user["id"] != user_id:
            return json_response(self, 403, {"message": "Você só pode deletar seu próprio usuário"})

        if user_id not in users:
            return json_response(self, 404, {"message": "Usuário não encontrado"})

        del users[user_id]

        tokens_to_remove = [token for token, session_user_id in sessions.items() if session_user_id == user_id]
        for token in tokens_to_remove:
            del sessions[token]

        return json_response(self, 200, {"message": "Usuário deletado com sucesso"})


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), AuthAPIHandler)
    print(f"API rodando em http://{HOST}:{PORT}")
    print("Pressione Ctrl+C para parar.")
    server.serve_forever()
