# welhome - Minhas Propriedades

Sistema de gerenciamento de imóveis.

## Como Rodar

1. Instale as dependências:

```bash
npm install
```

2. Inicie o backend (FastAPI na porta 8000)

3. Inicie o frontend:

```bash
npm run dev
```

4. Acesse: `http://localhost:8080`

## Backend

O backend deve estar em `http://localhost:8000` com endpoints:

- `GET /properties`
- `POST /properties`
- `PUT /properties/:id`
- `DELETE /properties/:id`

## Funcionalidades

- Listagem com busca e ordenação
- Adicionar/editar/remover imóveis
- Indicador de status (ativo/inativo)
