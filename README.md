# MVP 2025 POS - API Users

Esta API é um dos componentes do sistema MVP 2025 POS, responsável pelo gerenciamento de usuários e integração de autenticação via Keycloak.

API REST desenvolvida em FastAPI para cadastro e controle de usuários.


##  Funcionalidades

### Autenticação OAuth2 via Keycloak.

#### CRUD de Usuários:

POST /user: Criar um novo usuário

GET /user/{user_id}: Buscar um usuário pelo ID

PUT /user/{user_id}: Atualizar dados de um usuário

DELETE /user/{user_id}: Deletar um usuário


# Instalação e Configuração

####  1 ) Clone o projeto

```
git clone https://github.com/morettonijose/keycloak_users.git
cd mvp_2025_pos-users
```


####  2 ) Configure as variáveis de ambiente

Crie um arquivo .env ou .local.env e defina:

```
KEYCLOAK_URL=http://localhost:8080/
KEYCLOAK_REALM=mvp-2025
KEYCLOAK_CLIENT_ID=client_id
KEYCLOAK_CLIENT_SECRET=client_secret
KEYCLOAK_TOKEN_URL_PUBLIC=http://localhost:8080/realms/mvp-2025/protocol/openid-connect/token
DATABASE_URL=postgresql://user:password@db-notifications:5432/notifications
```


 ####  3 ) Suba o ambiente com Docker Compose
 
```
 docker-compose up --build
 ```

 Isso irá iniciar:

API de Notificações

API de Usuários

Banco de Dados PostgreSQL (para usuários e notificações)

Keycloak Server


 ####  4 ) Acesse

Keycloak Admin Console: http://localhost:8080/

API Users Swagger: http://localhost:8000/docs

API Notifications Swagger: http://localhost:8001/docs


 ####  Obs ) Docker

O projeto já contém:

Dockerfile para cada API

docker-compose.yml para orquestração dos serviços

Suba o ambiente rodando : docker-compose up --build
