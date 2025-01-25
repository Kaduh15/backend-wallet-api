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
- **Login de Usuário** (`POST /auth/login/`)
- **Refresh Token** (`POST /auth/refresh/`)

### ✅ **Gerenciamento de Carteira**

- **Consultar Saldo** (`GET /wallet/balance/`)
- **Adicionar Saldo** (`PATCH /wallet/add/`)
- **Transferências entre usuários** (`POST /wallet/transfer/`)
- **Listar Transações** (`GET /wallet/transactions/`)

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


