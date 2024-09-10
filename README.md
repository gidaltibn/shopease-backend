# Shopease Backend

**Shopease** é uma API REST para gerenciamento de uma loja virtual, desenvolvida com **Flask** e integrada à **FakeStore API**. O backend permite operações de autenticação de usuários, manipulação de carrinho de compras, checkout e histórico de pedidos. O projeto utiliza **SQLite** como banco de dados e está configurado para ser executado via **Docker**.

## Funcionalidades

- **Autenticação JWT**: Registro e login de usuários com geração de token JWT.
- **Carrinho de compras**: Adicionar, remover e listar produtos no carrinho.
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

2. **Construa a imagem Docker:**

   ```bash
   docker-compose up --build
   ```

3. **Acesse a aplicação:**

   A API estará disponível em `http://localhost:5000`.

### Rodando Localmente (sem Docker)

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/shopease-backend.git
   cd shopease-backend
   ```

2. **Crie e ative um ambiente virtual:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados SQLite:**

   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. **Execute a aplicação:**

   ```bash
   flask run
   ```

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

### Carrinho de Compras

- **GET /cart/** - Listar itens do carrinho.
- **POST /cart/add** - Adicionar produto ao carrinho.
  - Body:
    ```json
    {
      "product_id": 1,
      "quantity": 2
    }
    ```

- **POST /cart/remove** - Remover produto do carrinho.
  - Body:
    ```json
    {
      "product_id": 1
    }
    ```

### Pedidos

- **GET /orders** - Listar histórico de pedidos do usuário.
- **POST /checkout** - Finalizar pedido (checkout).
  
## Integração com FakeStore API

A integração com a **FakeStore API** permite buscar produtos e seus detalhes:

- **GET /products** - Listar produtos da FakeStore API.

## Contribuição

Contribuições são bem-vindas! Para contribuir, siga os passos abaixo:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`).
4. Envie sua branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.