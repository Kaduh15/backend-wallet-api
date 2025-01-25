# 💰 API de Carteira Digital

Esta API permite gerenciar carteiras digitais e realizar transferências entre usuários autenticados, utilizando Django Rest Framework e autenticação JWT.

---

## 🚀 Como Rodar o Projeto

### 1️⃣ **Clone o Repositório**

```bash
git clone https://github.com/seu_usuario/backend-wallet-api.git
cd backend-wallet-api
```

### 2️⃣ **Configure o Docker e Suba os Containers**

```bash
docker-compose up --build
```

Isso iniciará os serviços da API e do banco de dados PostgreSQL.

---

## 🛠️ Funcionalidades da API

### ✅ **Autenticação com JWT**

- **Registro de Usuário** (`POST /auth/register/`)
  - Requisição:
    ```json
    {
        "username": "usuario1",
        "email": "usuario1@example.com",
        "password": "senha123"
    }
    ```
  - Resposta:
    ```json
    {
        "id": 1,
        "username": "usuario1",
        "email": "usuario1@example.com"
    }
    ```

- **Login de Usuário** (`POST /auth/login/`)
  - Requisição:
    ```json
    {
        "username": "usuario1",
        "password": "senha123"
    }
    ```
  - Resposta:
    ```json
    {
        "refresh": "REFRESH_TOKEN",
        "access": "ACCESS_TOKEN"
    }
    ```

- **Refresh Token** (`POST /auth/refresh/`)
  - Requisição:
    ```json
    {
        "refresh": "REFRESH_TOKEN"
    }
    ```
  - Resposta:
    ```json
    {
        "access": "NOVO_ACCESS_TOKEN"
    }
    ```

### ✅ **Gerenciamento de Carteira**

- **Consultar Saldo** (`GET /wallet/balance/`)
  - Requisição: (Autenticado com token JWT)
  - Resposta:
    ```json
    {
        "id": 1,
        "user": 1,
        "balance": "150.50"
    }
    ```

- **Adicionar Saldo** (`PATCH /wallet/add/`)
  - Requisição:
    ```json
    {
        "amount": 100.00
    }
    ```
  - Resposta:
    ```json
    {
        "message": "Saldo adicionado com sucesso",
        "balance": "250.50"
    }
    ```

- **Transferências entre usuários** (`POST /wallet/transfer/`)
  - Requisição:
    ```json
    {
        "receiver": "usuario2",
        "amount": 50.00
    }
    ```
  - Resposta:
    ```json
    {
        "id": 1,
        "sender": "usuario1",
        "receiver": "usuario2",
        "amount": 50.00,
        "timestamp": "2024-01-01T12:00:00Z"
    }
    ```

- **Listar Transações** (`GET /wallet/transactions/`)
  - Parâmetros Opcionais:
    - `?start_date=2024-01-01&end_date=2024-01-31`
  - Resposta:
    ```json
    [
        {
            "id": 1,
            "sender": "usuario1",
            "receiver": "usuario2",
            "amount": 50.00,
            "timestamp": "2024-01-01T12:00:00Z"
        }
    ]
    ```

---

## 🔑 **Autenticação**

Todas as rotas protegidas exigem um **token JWT** no cabeçalho:

```
Authorization: Bearer SEU_ACCESS_TOKEN
```

Após o login, o token é retornado:

```json
{
    "refresh": "REFRESH_TOKEN",
    "access": "ACCESS_TOKEN"
}
```

Para acessar as rotas protegidas, use o **ACCESS\_TOKEN** no cabeçalho da requisição.

---

## 📦 Como Popular o Banco com Dados Fictícios

Para criar usuários e transações de exemplo, execute:

```bash
docker-compose exec app python manage.py populate_db
```

Isso criará usuários com carteiras e algumas transferências entre eles.

---

## 📌 **Executando os Testes**

Os testes automatizados garantem que a API funciona corretamente.

Para rodar os testes:

```bash
docker-compose exec app python manage.py test
```

Isso executará os testes para **autenticação, carteira e transferências**.

---

## 📜 **Tecnologias Utilizadas**

- **Python 3.11**
- **Django Rest Framework**
- **PostgreSQL**
- **Docker & Docker Compose**
- **JWT (JSON Web Token)**
- **pytest / Django TestCase**


