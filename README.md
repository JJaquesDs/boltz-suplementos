# Boltz Suplementos
Sistema WEB para a marca Boltz Suplementos.
---------------------------------------------------------------------------------------------------

## Descrição

A API visa atuar como controle de estoque e conter a lógica e acesso a áreas de experiências para usuários

O sistema na fase atual permite:

* Cadastrar usuários, administradores para estoque e vizualização de dados sensíveis

* Cadastrar usuários comuns apenas para testes no momento (Área de usuários ainda não iplementada)

## Tecnologias utilizadas

* Python 3.12.5
* FastAPI
* Uvicorn
* Alembic
* Pydantic
* SQLModel + SqlAlchemy
* bcrypt

## Iniciar Projeto ##

### Criando ambiente virtual isolado ###
  Primeiro precisamos criar umm ambiente virtual(venv) para manter um ambiente isolado com todas nossas dependências do projeto
  Para criar a venv, ultilize o seguinte comando na raiz do projeto:
```cmd
python -m venv .venv
```

  Após isso, inicialize a venv agora e toda vez que for entrar no projeto, pois aqui ficará tudo que o projeto precisa para funcionar:
1. cmd (Prompt de Comandos):
```cmd
.venv\Scripts\activate.bat
```

2. powershell:
```poweshell
.\venv\Scripts\Activate
```

> [!NOTE]
> **Você deve ter o Python instalado para ultilizar todos esses comandos e esse projeto**.
----------------------------------------------------------------------------------------------
### Instalando dependências ###
  Começando instalando **requirements-dev.txt** que contém o **pip-tools**,
  ferramenta util para ultilizar comandos de terminal no projeto

```cmd
pip install -r requirements-dev.txt
```

  O arquivo **requirements.txt** agora pode ser instalado com todas as dependências do projeto
```cmd
pip install -r requirements.txt
```

  Agora todas as dependências para o projeto em Python rodar estão instaladas no seu ambiente virtual!
-----------------------------------------------------------------------------------------------------


## Configuração do banco de dados para acesso ao sistema

Encontre o arquivo [.env-example](.env-example)
e no mesmo diretório crie um arquivo file com o nome **".env"** e preencha conforme as especificações do example

Vale ressaltar que deve ser criado um **banco de dados Postgres** para ser preenchido em **.env**

### Migrations (Alembic)

Para rodar a aplicação pela primeira vez, o banco de dados deve ter as tabelas criadas
isso é feito via migrations pelo **Alembic**. Para efetuar esse passo no **terminal** esteja na raiz do projeto e com a **venv** ativa por exemplo:

````text
C: ..\boltz_suplementos
````

Aqui rode o seguinte comando no terminal:

````bash
alembic upgrade head
````

> [!Note]
> Caso você crie novas entidades ou mude atributos das entidades nas tabelas siga os comandos abaixo:

### Caso fora criada uma entidade:

Vá para o código de início do pacote "\users" em [_ init _](app/domains/__init__.py)
e importe as classes das entidades, como, por exemplo:

````text
from .users.users import *
from .produtos.produtos import *
from .MODULO_DA_ENTIDADE.CLASSE_DA_ENTIDADE import *
````

Depois rode a migration:

````bash
alembic revision --autogenerate -m "mensagem_da_migracao"
````

Depois rode a migration:

````bash
alembic upgrade head
````

### Caso fora feita alteração num atributo de uma entidade

````bash
alembic revision --autogenerate -m "alteracao_feita"
````
Depois rode a migration:

````bash
alembic upgrade head
````


------------------------------------------------------------------------------------------------------------------------------
## Acesso ao sistema

-------------------------------------------------------------------------------------------------------------------------------
Primeiro voce deve ativar a **venv** como demonstrado à cima e entrar na raiz do projeto, caso não esteja
como por exemplo

````text
C:..\boltz_suplementos
````


Via terminal execute para rodar o servidor uvicorn:

```bash
uvicorn main:app --reload
```

A aplicação ficará disponível em:

```
http://localhost:8000
```

---

# Swagger

A documentação da API pode ser acessada em:

```
http://localhost:8000/docs
```


> [!Note]
> Com o .env configurado, ao iniciar a aplicação pela primeira vez o seu **superusuario**
> será criado e voce poderá acessar as funcionalidades com ele


---

Na documentação, a interface swagger open-api mostra todas as rotas e os verbos de requisições,
bem como exemplos de saídas e visualização das saídas dos json da API.

Ela permite mostrar uma interface amigável para manipulação do backend e testes das rotas

<img src="boltz_suplementos\img_for_docs\swagger_interface.png" width="400">

# Endpoints

Nessa sessão será demonstrado os endpoints da API e suas aplicações

## Users:
Base URL: /users

-------------------------------------------------------
1. **Criar usuário**

Cria um novo usuário no sistema.

Endpoint: POST /users/

- Parâmetros: Nenhum

- Response: 201 CREATE

Request Body:

````json
{
  "nome": "Joao",
  "email": "teste@example.com",
  "senha": "1234"
}
````


  Campos:

  | Campo     | Tipo      | Obrigatório | Descrição          |
  |-----------|-----------|-------------|--------------------|
  | nome      | String    | Sim         | Nome do usuário    |
  | email     | EmailStr  | Sim         | Email do usuário   |
  | senha     | String    | Sim         | Senha do usuário   |


> [!Note]
> Como estamos utilizando **Pydantic EmailStr**, você deve passar um email válido como:
> **joao@email.com**, emails sem **"@"** ou sem **".com"**
> retornarão erro e não salvarão o usuário nos registros

> [!Note]
> Essa rota só cria **por padrão** usuários com permissão **user** básica


2. **Listar Todos os Usuários**
   Retorna uma lista com todos os usuários cadastrados no sistema.

Endpoint: GET /users/listar_todos

- **Depende de estar logado com usuário administrador**

- Parâmetros: Nenhum

- Response: 200 OK


Request Body:

````json
[
  {
    "nome": "joao",
    "email": "joao@example.com",
    "role": "superuser",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  },
    {
    "nome": "rikelme",
    "email": "rikelme@example.com",
    "role": "admin",
    "user_id": "4gb96g75-6828-5673-c4gd-3d074g77bgb7"
  },
  {
    "nome": "averaldo",
    "email": "averaldo@example.com",
    "role": "user",
    "user_id": "7hg69a37-6828-5673-c4gd-3d074g77rgb1"
  }
]

````

3. **Listar usuário pelo uuid**
   Retorna usuários no sistema pelo uuid.

Endpoint: GET /users/{user_uuid}

- **Depende de estar logado com usuário administrador**

- Parâmetros: uuid (obrigatório) - UUID do histórico de manutenção a ser listado
  Exemplo: `GET /users/3fa85f64-5717-4562-b3fc-2c963f66afa6`

- Response: 200 OK

Response Body:

````json
{
    "nome": "joao",
    "email": "joao@example.com",
    "role": "superuser",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
````
Possíveis Erros:

- `404 Not Found` - Usuáirio não encontrado com o UUID fornecido
-----------------------------------------------------------------
4. **Atualizar Usuário**
   Atualiza parcialmente as informações de um usuário existente através do UUID.

Endpoint: PATCH /users/{user_uuid}

- Parâmetro:

- **Depende de estar logado com usuário administrador**

- uuid (obrigatório) - UUID do usuário a ser atualizado

- Exemplo: `PATCH /users/3fa85f64-5717-4562-b3fc-2c963f66afa6`


- Response: 200 OK


Request Body:

````json
{
    "email": "joao@email.com"
}
````

> [!Note]
> Você pode enviar apenas os campos que deseja atualizar, não precisa alterar todos

Possíveis erros:

- `404 Not Found` - Usuário não encontrado com UUID fornecido
- `400 Bad Request` - Dados inválidos na requisição

---------------------------------------------------------------------------------------

# Desenvolvimento

Para dúvidas sobre implementação ou integração:
- Email: [joaovitor.jaques.7748@gmail.com](mailto:joaovitor.jaques.7748@gmail.com)


- Github J.Vitor: https://github.com/JJaquesDs


### Reportar Problemas
Encontrou um bug ou tem uma sugestão? Sinta-se livre para mandar um email para gente!

-----------------------------------------------------------------------------------------------------------------------

Versão da API: `0.1.0`

Data da última grande atualização: `30/07/2026`

 © Direitos Reservados