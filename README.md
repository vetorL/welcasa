# 🏠 Welcasa Properties API

Backend minimalista em **FastAPI** com **SQLite local**, responsável por gerenciar propriedades (imóveis).

Implementa o CRUD básico de propriedades com os campos `id`, `title`, `address` e `status`.

## 🚀 Como rodar o projeto

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPO>
cd <PASTA_DO_REPO>
```

### 2. Criar e ativar ambiente virtual

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

### 3. Instalar dependências

```bash
pip install fastapi uvicorn pydantic
```

### 4. Executar o servidor

```bash
python app.py
```

> O servidor será iniciado em:
> 📍 `http://127.0.0.1:8000`

## 🧭 Endpoints disponíveis

### `GET /`

Verificação simples de saúde da API.

```json
{ "ok": true }
```

### `GET /properties`

Lista todas as propriedades cadastradas.

### `POST /properties`

Cria uma nova propriedade.
**Exemplo de corpo:**

```json
{
  "title": "Apartamento 101",
  "address": "Rua das Flores, 123",
  "status": "active"
}
```

### `PUT /properties/{id}`

Atualiza os dados de uma propriedade existente.
**Exemplo de corpo:**

```json
{
  "title": "Apartamento 101B",
  "address": "Rua das Flores, 123",
  "status": "inactive"
}
```

### `DELETE /properties/{id}`

Remove a propriedade com o `id` informado.

## 🗃️ Banco de dados

O banco é criado automaticamente ao iniciar o servidor:

```
properties.db
```

Tabela criada:

```sql
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    address TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active','inactive'))
);
```

## 🧪 Testes rápidos com `curl`

Criar:

```bash
curl -X POST http://127.0.0.1:8000/properties \
  -H "Content-Type: application/json" \
  -d '{"title":"Apto 101","address":"Rua XPTO, 123","status":"active"}'
```

Listar:

```bash
curl http://127.0.0.1:8000/properties
```

Atualizar:

```bash
curl -X PUT http://127.0.0.1:8000/properties/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Apto 101B","address":"Rua XPTO, 123","status":"inactive"}'
```

Remover:

```bash
curl -X DELETE http://127.0.0.1:8000/properties/1
```

## 🧰 Tecnologias utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLite](https://www.sqlite.org/)
- [Pydantic](https://docs.pydantic.dev/)
