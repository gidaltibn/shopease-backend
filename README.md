````markdown
# Shopease Backend

**Shopease** é uma API REST para gerenciamento de uma loja virtual, desenvolvida com **Flask** e integrada à **FakeStore API**. O backend permite operações de autenticação de usuários, manipulação de carrinho de compras, checkout e histórico de pedidos. O projeto utiliza **SQLite** como banco de dados e está configurado para ser executado via **Docker**.

## Funcionalidades

- **Autenticação JWT**: Registro e login de usuários com geração de token JWT.
- **Carrinho de compras**: Adicionar, remover e listar produtos no carrinho e alterar quantidade.
- **Pedidos**: Finalizar pedido (checkout) e consultar histórico de pedidos.
- **Integração com FakeStore API**: Busca de produtos via API externa.
- **Persistência de dados**: Utiliza **SQLite** para armazenar dados de usuários, produtos no carrinho e pedidos.

## Tecnologias Utilizadas

- [Flask](https://flask.palletsprojects.com/) - Framework de desenvolvimento web.
- [SQLite](https://www.sqlite.org/index.html) - Banco de dados embutido.
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) - Extensão para integração do Flask com bancos de dados.
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/) - Autenticação baseada em JWT.
- [FakeStore API](https://fakestoreapi.com/) - API externa para busca de produtos.
- [Docker](https://www.docker.com/) - Para conteinerização do aplicativo.

## Pré-requisitos

Antes de começar, você precisará ter o [Docker](https://www.docker.com/get-started) instalado na sua máquina.

## Como Rodar o Projeto

### Rodando com Docker

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/shopease-backend.git
   cd shopease-backend
   ```
````

2. **Construa a imagem Docker:**

   ```bash
   docker-compose up --build
   ```

3. **Acesse a aplicação:**

   A API estará disponível em `http://localhost:5000`.

## Rotas da API

### Autenticação

- **POST /auth/register** - Registro de novo usuário.

  - Body:
    ```json
    {
      "username": "user",
      "email": "user@example.com",
      "password": "password"
    }
    ```

- **POST /auth/login** - Login de usuário e geração de token JWT.

  - Body:
    ```json
    {
      "email": "user@example.com",
      "password": "password"
    }
    ```
  - **Resposta:** Após o login bem-sucedido, o token JWT é retornado. Este token deve ser incluído no cabeçalho `Authorization` em todas as transações que exigem autenticação.
  - Exemplo:
    ```bash
    Authorization: Bearer <access_token>
    ```

- **POST /auth/logout** - Logout do usuário (JWT Token é invalidado).

### Carrinho de Compras

- **GET /cart/** - Listar itens do carrinho. **Autenticação necessária.**

  - **Cabeçalho:**
    ```bash
    Authorization: Bearer <access_token>
    ```

- **POST /cart/add** - Adicionar produto ao carrinho. **Autenticação necessária.**

  - Body:
    ```json
    {
      "product_id": 1,
      "quantity": 2
    }
    ```

- **POST /cart/remove** - Remover produto do carrinho. **Autenticação necessária.**
  - Body:
    ```json
    {
      "product_id": 1
    }
    ```

### Pedidos

- **GET /orders** - Listar histórico de pedidos do usuário. **Autenticação necessária.**

  - **Cabeçalho:**
    ```bash
    Authorization: Bearer <access_token>
    ```

- **POST /checkout** - Finalizar pedido (checkout). **Autenticação necessária.**
  - **Cabeçalho:**
    ```bash
    Authorization: Bearer <access_token>
    ```

## Integração com FakeStore API

A integração com a **FakeStore API** permite buscar produtos e seus detalhes:

- **GET /products** - Listar produtos da FakeStore API.
- **GET /products/<product_id>** - Buscar detalhes de um produto específico.

## Dockerfile e Docker-Compose

### Dockerfile

O projeto inclui um **Dockerfile** para conteinerizar a aplicação:

```Dockerfile
# Usar uma imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instalar as dependências listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação para o container
COPY . .

# Definir a variável de ambiente para desativar o modo de depuração (produção)
ENV FLASK_ENV=production

# Expor a porta 5000 para o Flask
EXPOSE 5000

# Comando para iniciar a aplicação Flask
CMD ["flask", "run", "--host=0.0.0.0"]
```

### Docker Compose

O projeto também utiliza **docker-compose** para facilitar o gerenciamento dos serviços:

```yaml
version: "3"
services:
  web:
    build: .
    command: flask run --host=0.0.0.0
    volumes:
      - ./:/app
    ports:
      - "5000:5000"
```

## Requisitos Adicionais

- Todas as rotas protegidas (como `/cart`, `/orders`, e `/checkout`) exigem o token JWT no cabeçalho de autorização.
- O projeto utiliza **SQLite** por padrão, mas pode ser facilmente modificado para utilizar **PostgreSQL** ou **MySQL** alterando a string de conexão no arquivo `config.py`.
