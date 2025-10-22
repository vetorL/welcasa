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
python app.py
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

| Método   | Rota               | Descrição                           |
| -------- | ------------------ | ----------------------------------- |
| `GET`    | `/`                | Verificação simples de saúde da API |
| `GET`    | `/properties`      | Lista todos os imóveis              |
| `POST`   | `/properties`      | Cria um novo imóvel                 |
| `PUT`    | `/properties/{id}` | Atualiza um imóvel existente        |
| `DELETE` | `/properties/{id}` | Remove um imóvel                    |

**Exemplo de criação:**

```bash
curl -X POST http://127.0.0.1:8000/properties \
  -H "Content-Type: application/json" \
  -d '{"title":"Apartamento 101","address":"Rua das Flores, 123","status":"active"}'
```

## 🧱 Funcionalidades do Frontend

- 📋 Listagem de imóveis com busca e ordenação
- ➕ Adicionar, ✏️ editar e 🗑️ remover imóveis
- 🟢 Indicador de status (ativo/inativo)

## 🧰 Tecnologias Utilizadas

**Backend:**

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLite](https://www.sqlite.org/)
- [Pydantic](https://docs.pydantic.dev/)

**Frontend:**

- [React](https://react.dev/)
- [Vite](https://vitejs.dev/)
- [npm](https://www.npmjs.com/)

## ✅ Estrutura do Projeto

```
.
├── backend/
│   ├── app.py
│   └── properties.db
└── frontend/
    ├── package.json
    └── src/
```

## 🧩 Autor

Desenvolvido para o **Case Técnico Simplificado – Lista de Imóveis (welhome)**.
CRUD completo, simples e funcional, conforme especificado no desafio técnico.
