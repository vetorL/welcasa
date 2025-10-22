# 🏠 welhome – Sistema de Gestão de Imóveis

Aplicação **fullstack** simples para gerenciar propriedades (imóveis) da welhome.
Desenvolvida com **FastAPI** (backend) e **React** (frontend).

## 🚀 Como Rodar o Projeto

### 🧩 1. Clonar o repositório

```bash
git clone <URL_DO_REPO>
cd <PASTA_DO_REPO>
```

### ⚙️ 2. Rodar o Backend (FastAPI + SQLite)

#### Criar e ativar ambiente virtual

**Linux/macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Instalar dependências

```bash
pip install fastapi uvicorn pydantic
```

#### Executar o servidor

```bash
python backend/app.py
```

> O backend iniciará em:
> 📍 `http://127.0.0.1:8000`

#### Banco de dados

Um banco **SQLite local (`properties.db`)** é criado automaticamente ao rodar o servidor.

Tabela utilizada:

```sql
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    address TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active','inactive'))
);
```

### 💻 3. Rodar o Frontend (React)

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

> O frontend estará disponível em:
> 🌐 `http://localhost:8080`

Certifique-se de que o **backend** está rodando na porta `8000`.

## 🧭 Endpoints do Backend

| Método   | Rota               | Descrição                    |
| -------- | ------------------ | ---------------------------- |
| `GET`    | `/properties`      | Lista todos os imóveis       |
| `POST`   | `/properties`      | Cria um novo imóvel          |
| `PUT`    | `/properties/{id}` | Atualiza um imóvel existente |
| `DELETE` | `/properties/{id}` | Remove um imóvel             |

**Exemplo de criação:**

```bash
curl -X POST http://127.0.0.1:8000/properties \
  -H "Content-Type: application/json" \
  -d '{"title":"Apartamento 101","address":"Rua das Flores, 123","status":"active"}'
```

---

## 🐳 4. Rodar com Docker (modo completo – frontend + backend juntos)

A aplicação pode ser executada em um **único container**, com o frontend já compilado e servido pelo FastAPI.

### 🧱 Build da imagem

Na raiz do projeto (onde está o `Dockerfile`):

```bash
podman build -t welhome .
# ou
docker build -t welhome .
```

### ▶️ Rodar o container

```bash
podman run --rm -p 8000:8000 welhome
# ou
docker run --rm -p 8000:8000 welhome
```

### 🌐 Acessar

Abra no navegador:
**[http://localhost:8000](http://localhost:8000)**

- Frontend e API estão no mesmo endereço.
- `/properties` → endpoints da API
- `/` → interface web React (SPA)

---

## 🧱 Estrutura do Projeto

```
.
├── backend/
│   ├── app.py
│   └── properties.db
├── frontend/
│   ├── package.json
│   └── src/
└── Dockerfile
```

---

## 🧰 Tecnologias Utilizadas

**Backend**

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLite](https://www.sqlite.org/)
- [Pydantic](https://docs.pydantic.dev/)

**Frontend**

- [React](https://react.dev/)
- [Vite](https://vitejs.dev/)
- [npm](https://www.npmjs.com/)

**Infraestrutura**

- [Docker / Podman](https://www.docker.com/)

---

## 🧩 Autor

Desenvolvido para o **Case Técnico Simplificado – Lista de Imóveis (welhome)**.
CRUD completo, simples e funcional, conforme especificado no desafio técnico.
