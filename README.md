

# Rodar o requirements

```
pip3 install -r requirements.txt
```

# Auth API para Postman

API simples em Python puro para testar autenticação e CRUD de usuário no Postman.

## Como rodar

```bash
python app.py
```

Se o comando `python` não estiver configurado no seu terminal, use:

```bash
"C:\Users\Luan Dev\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" app.py
```

A API sobe em:

```text
http://localhost:8000
```

Os dados ficam em memória. Quando você parar o servidor, os usuários e tokens são apagados.

## Rotas

### Health check

```http
GET /health
```

### Criar usuário

```http
POST /users
Content-Type: application/json
```

Body:

```json
{
  "name": "Luan",
  "email": "luan@email.com",
  "password": "123456"
}
```

### Login

```http
POST /auth/login
Content-Type: application/json
```

Body:

```json
{
  "email": "luan@email.com",
  "password": "123456"
}
```

Copie o `token` retornado e use nas próximas rotas:

```http
Authorization: Bearer SEU_TOKEN
```

### Logout

```http
POST /auth/logout
Authorization: Bearer SEU_TOKEN
```

### Buscar usuário logado

```http
GET /users/me
Authorization: Bearer SEU_TOKEN
```

### Buscar usuário por ID

```http
GET /users/{user_id}
Authorization: Bearer SEU_TOKEN
```

### Atualizar usuário

```http
PUT /users/{user_id}
Authorization: Bearer SEU_TOKEN
Content-Type: application/json
```

Body:

```json
{
  "name": "Luan Atualizado",
  "email": "luan.atualizado@email.com",
  "password": "novaSenha123"
}
```

### Deletar usuário

```http
DELETE /users/{user_id}
Authorization: Bearer SEU_TOKEN
```

## Ordem recomendada no Postman

1. `POST /users`
2. `POST /auth/login`
3. Copiar `token` e `user.id`
4. `GET /users/me`
5. `GET /users/{user_id}`
6. `PUT /users/{user_id}`
7. `POST /auth/logout`
8. Fazer login novamente se quiser testar delete
9. `DELETE /users/{user_id}`
