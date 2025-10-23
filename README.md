# 🏠 welhome – Sistema de Gestão de Imóveis

Aplicação **fullstack** simples para gerenciar imóveis, com **FastAPI** (backend) e **React + Vite** (frontend).

## 🚀 Como Rodar

### 1️⃣ Clonar o repositório

```bash
git clone <URL_DO_REPO>
cd <PASTA_DO_REPO>
```

### 2️⃣ Backend (FastAPI + PostgreSQL)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Suba o banco Postgres local com Podman (ou Docker):

```bash
podman run -d --name welhome-pg \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=welhome \
  -p 5432:5432 \
  -v welhome-pgdata:/var/lib/postgresql/data \
  docker.io/postgres:16
```

Configure a variável de ambiente:

```bash
export DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:5432/welhome?sslmode=disable"
```

Execute o servidor:

```bash
python app.py
```

➡️ **Backend:** [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 3️⃣ Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

➡️ **Frontend:** [http://localhost:8080](http://localhost:8080)
Certifique-se de que o backend está ativo na porta `8000`.

## 🧭 Endpoints Principais

| Método | Rota               | Descrição        |
| ------ | ------------------ | ---------------- |
| GET    | `/properties`      | Lista imóveis    |
| POST   | `/properties`      | Cria novo imóvel |
| PUT    | `/properties/{id}` | Atualiza imóvel  |
| DELETE | `/properties/{id}` | Remove imóvel    |

Exemplo:

```bash
curl -X POST http://127.0.0.1:8000/properties \
  -H "Content-Type: application/json" \
  -d '{"title":"Apartamento 101","address":"Rua das Flores, 123","status":"active"}'
```

## 🧱 Estrutura

```
.
├── backend/
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   ├── package.json
│   └── src/
```

## 🧰 Tecnologias

- **Backend:** FastAPI, PostgreSQL, Pydantic
- **Frontend:** React, Vite
- **Infra:** Podman / Docker
