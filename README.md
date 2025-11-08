# 📦 Sistema de Gestão de Estoque - FastAPI

Sistema completo de gerenciamento de estoque desenvolvido em **FastAPI** com autenticação JWT, controle de usuários, produtos, fornecedores e movimentações de estoque.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🚀 Funcionalidades

### 🔐 Autenticação e Autorização
- ✅ Sistema de login com JWT (JSON Web Tokens)
- ✅ Registro de novos usuários
- ✅ Autenticação baseada em roles (Packer, Logistics Coordinator, System Admin)
- ✅ Troca de senha segura
- ✅ Proteção de rotas por permissões

### 👥 Gerenciamento de Usuários
- ✅ CRUD completo de usuários (apenas admins)
- ✅ Listagem com filtros (nome, email, occupation)
- ✅ Ativação/desativação de contas
- ✅ Controle de permissões por tipo de usuário

### 📦 Controle de Produtos
- ✅ Cadastro de produtos com categorias e fornecedores
- ✅ Busca e filtros avançados (nome, preço, categoria)
- ✅ Atualização parcial (PATCH) e completa (PUT)
- ✅ Validação de duplicação

### 🏷️ Categorias e Fornecedores
- ✅ Gerenciamento de categorias de produtos
- ✅ Cadastro e controle de fornecedores
- ✅ Relacionamento com produtos

### 📊 Controle de Estoque
- ✅ Registro de níveis de estoque por produto
- ✅ Configuração de estoque mínimo/máximo
- ✅ Alertas de estoque baixo
- ✅ Localização de produtos no estoque

### 🔄 Movimentações de Estoque
- ✅ Registro de entradas e saídas
- ✅ Histórico completo de movimentações
- ✅ Ajuste manual de estoque (apenas admins)
- ✅ Atualização automática de níveis
- ✅ Validação de estoque disponível

### 🛒 Gerenciamento de Pedidos
- ✅ Criação de pedidos vinculados ao usuário logado
- ✅ Controle de status (Pendente, Enviado, Entregue, Cancelado)
- ✅ Cálculo automático de preços
- ✅ Histórico de pedidos por usuário
- ✅ Cancelamento de pedidos com regras de negócio

---

## 🛠️ Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno e rápido
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - ORM para Python
- **[Pydantic](https://docs.pydantic.dev/)** - Validação de dados
- **[Alembic](https://alembic.sqlalchemy.org/)** - Migrações de banco de dados
- **[Python-Jose](https://python-jose.readthedocs.io/)** - JWT (JSON Web Tokens)
- **[Passlib](https://passlib.readthedocs.io/)** - Hashing de senhas com Bcrypt
- **[SQLite](https://www.sqlite.org/)** - Banco de dados (desenvolvimento)

---

## 📋 Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- virtualenv (recomendado)

---

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/Sistema_Estoque_FastAPI.git
cd Sistema_Estoque_FastAPI
```

### 2. Crie e ative um ambiente virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Segurança
SECRET_KEY=sua_chave_secreta_super_segura_aqui_mude_isso
JWT_SECRET_KEY=sua_chave_jwt_64_chars_hexadecimal

# Banco de dados
DATABASE_URL=sqlite:///./banco.db

# Configurações da aplicação
DEBUG=False
```

### 5. Execute as migrações do banco de dados

```bash
alembic upgrade head
```

### 6. Inicie o servidor

```bash
uvicorn main:app --reload
```

O servidor estará disponível em: **http://localhost:8000**

---

## 📚 Documentação da API

Após iniciar o servidor, acesse a documentação interativa:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔑 Estrutura de Usuários

O sistema possui 3 tipos de usuários com diferentes permissões:

### 🔹 Packer (Empacotador)
- Visualizar produtos e estoque
- Registrar entrada de produtos
- Criar pedidos

### 🔸 Logistics Coordinator (Coordenador de Logística)
- Todas as permissões do Packer
- Gerenciar produtos, categorias e fornecedores
- Atualizar status de pedidos
- Ajustar níveis de estoque

### 🔺 System Admin (Administrador)
- Todas as permissões do sistema
- Gerenciar usuários (criar, editar, deletar)
- Configurações avançadas
- Acesso total aos dados

---

## 📖 Exemplos de Uso

### 1. Registrar um novo usuário

```bash
POST /auth/register
Content-Type: application/json

{
  "name": "João Silva",
  "email": "joao@empresa.com",
  "password": "senhaSegura123",
  "occupation": "packer"
}
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "João Silva",
    "email": "joao@empresa.com",
    "occupation": "packer",
    "active": true
  }
}
```

### 2. Fazer login

```bash
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=joao@empresa.com&password=senhaSegura123
```

### 3. Criar um produto (requer autenticação)

```bash
POST /products
Authorization: Bearer seu_token_jwt_aqui
Content-Type: application/json

{
  "name": "Notebook Dell Inspiron 15",
  "description": "Notebook para trabalho",
  "price": 2500.00,
  "category_id": 1,
  "supplier_id": 1
}
```

### 4. Registrar entrada no estoque

```bash
POST /stock/movements
Authorization: Bearer seu_token_jwt_aqui
Content-Type: application/json

{
  "product_id": 1,
  "movement_type": "in",
  "quantity": 50,
  "reference_type": "purchase"
}
```

### 5. Criar um pedido

```bash
POST /orders
Authorization: Bearer seu_token_jwt_aqui
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2
}
```

---

## 🗂️ Estrutura do Projeto

```
Sistema_Estoque_FastAPI/
├── models/
│   └── models.py              # Modelos SQLAlchemy (User, Product, Order, etc)
├── schemas/
│   ├── auth_schema.py         # Schemas de autenticação
│   ├── user_schema.py         # Schemas de usuário
│   ├── product_schema.py      # Schemas de produto
│   ├── category_schema.py     # Schemas de categoria
│   ├── supplier_schema.py     # Schemas de fornecedor
│   ├── stock_schema.py        # Schemas de estoque
│   └── order_schema.py        # Schemas de pedido
├── routes/
│   ├── auth_routes.py         # Rotas de autenticação
│   ├── user_routes.py         # Rotas de usuários
│   ├── product_routes.py      # Rotas de produtos
│   ├── category_routes.py     # Rotas de categorias
│   ├── supplier_routes.py     # Rotas de fornecedores
│   ├── stock_routes.py        # Rotas de estoque
│   └── order_routes.py        # Rotas de pedidos
├── security/
│   ├── auth.py                # Funções de autenticação JWT
│   └── security.py            # Configurações de segurança
├── alembic/
│   └── versions/              # Migrações do banco
├── .env                       # Variáveis de ambiente (não commitar!)
├── .gitignore
├── alembic.ini                # Configuração do Alembic
├── database.py                # Configuração do banco de dados
├── main.py                    # Arquivo principal da aplicação
├── requirements.txt           # Dependências do projeto
└── README.md
```

---

## 🔒 Segurança

### Boas Práticas Implementadas:

- ✅ Senhas hasheadas com **Bcrypt**
- ✅ Autenticação via **JWT** com expiração
- ✅ Validação de dados com **Pydantic**
- ✅ Proteção contra SQL Injection (SQLAlchemy ORM)
- ✅ Variáveis sensíveis em arquivo **.env**
- ✅ CORS configurável
- ✅ Validação de permissões por role

### ⚠️ Importante:

- Nunca commite o arquivo `.env` no Git
- Use senhas fortes em produção
- Troque as chaves secretas padrão
- Configure HTTPS em produção
- Implemente rate limiting para APIs públicas

---

## 🧪 Testes

Para executar os testes (quando implementados):

```bash
pytest
```

Para testes com cobertura:

```bash
pytest --cov=.
```

---

## 📊 Modelo do Banco de Dados

### Principais Tabelas:

- **users** - Usuários do sistema
- **products** - Produtos cadastrados
- **categories** - Categorias de produtos
- **suppliers** - Fornecedores
- **stock_levels** - Níveis atuais de estoque
- **stock_movements** - Histórico de movimentações
- **orders** - Pedidos realizados

### Diagrama ER (simplificado):

```
users (1) ──────< (N) orders
users (1) ──────< (N) stock_movements

products (N) ────> (1) categories
products (N) ────> (1) suppliers
products (1) ────< (1) stock_levels
products (1) ────< (N) stock_movements
products (1) ────< (N) orders
```

---

## 🚀 Deploy

### Opções de Deploy:

1. **Heroku**
   ```bash
   git push heroku main
   ```

2. **Railway**
   - Conecte seu repositório GitHub
   - Configure as variáveis de ambiente
   - Deploy automático

3. **Docker** (exemplo)
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

---

## 📝 Roadmap

- [ ] Implementar testes unitários e de integração
- [ ] Adicionar paginação em todas as listagens
- [ ] Implementar filtros avançados
- [ ] Sistema de notificações (email/webhook)
- [ ] Relatórios em PDF
- [ ] Dashboard com gráficos
- [ ] Integração com APIs de pagamento
- [ ] Sistema de backup automático
- [ ] Logs estruturados
- [ ] Rate limiting por usuário
- [ ] Webhooks para eventos importantes

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

**Seu Nome**
- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [Seu Nome](https://linkedin.com/in/seu-perfil)
- Email: seu.email@exemplo.com

---

## 📞 Suporte

Se você encontrar algum problema ou tiver sugestões:

- Abra uma [Issue](https://github.com/seu-usuario/Sistema_Estoque_FastAPI/issues)
- Entre em contato via email
- Consulte a [documentação](http://localhost:8000/docs)

---

## 🙏 Agradecimentos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework incrível
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM poderoso
- Comunidade Python Brasil

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!

**Desenvolvido com ❤️ usando FastAPI**
