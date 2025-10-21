# Welcasa - Sistema de Gestão de Imóveis

Sistema frontend para gerenciamento de imóveis.

## 🚀 Como Rodar o Projeto

### Pré-requisitos

- Node.js (versão 16 ou superior)
- npm ou yarn
- Backend Flask rodando na porta 8000

### Instalação

1. Clone o repositório:

```bash
git clone <YOUR_GIT_URL>
cd <YOUR_PROJECT_NAME>
```

2. Instale as dependências:

```bash
npm install
```

3. Inicie o servidor de desenvolvimento:

```bash
npm run dev
```

4. Acesse a aplicação em: `http://localhost:8080`

## 🔌 Integração com Backend

O frontend espera que o backend Flask esteja rodando em `http://localhost:8000` com os seguintes endpoints:

- `GET /properties` - Lista todos os imóveis
- `POST /properties` - Cria um novo imóvel
- `PUT /properties/:id` - Atualiza um imóvel
- `DELETE /properties/:id` - Remove um imóvel

### Estrutura de Dados

```json
{
  "id": 1,
  "title": "Apartamento em Copacabana",
  "address": "Av. Atlântica, 1500 - Rio de Janeiro",
  "status": "active"
}
```

## 🎨 Funcionalidades

- ✅ Listagem de imóveis em tabela
- ✅ Adicionar novos imóveis via modal
- ✅ Editar imóveis existentes
- ✅ Remover imóveis
- ✅ Indicador visual de status (ativo/inativo)
- ✅ Validação de formulários
- ✅ Feedback visual com toasts

## 🛠️ Tecnologias

- **React** - Biblioteca UI
- **TypeScript** - Tipagem estática
- **Vite** - Build tool
- **Tailwind CSS** - Estilização
- **shadcn/ui** - Componentes UI
- **React Query** - Gerenciamento de estado servidor
- **React Hook Form** - Gerenciamento de formulários
- **Zod** - Validação de schemas

## 📝 Estrutura do Projeto

```
src/
├── components/
│   ├── ui/                  # Componentes shadcn/ui
│   ├── PropertyTable.tsx    # Tabela de imóveis
│   └── PropertyModal.tsx    # Modal de cadastro/edição
├── services/
│   └── propertyService.ts   # Serviço de API
├── pages/
│   └── Index.tsx            # Página principal
└── hooks/
    └── use-toast.ts         # Hook de notificações
```
