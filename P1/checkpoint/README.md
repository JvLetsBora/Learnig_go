# Documentação das Rotas da API

## Visão Geral
Este documento descreve as rotas disponíveis na API para interagir com usuários e tarefas.

## Coleção e Metadados
- **Cliente**: Thunder Client
- **Nome da Coleção**: Tasks
- **ID da Coleção**: 0e03eb7e-d1ae-4ab7-9553-261bf2e6a2d1
- **Data de Exportação**: 2024-05-13T19:32:59.790Z
- **Versão**: 1.2

## Rotas

### Deletar Tarefa (Task)
- **Nome**: Task
- **URL**: `http://127.0.0.1:8000/tasks/{task_id}`
- **Método**: DELETE
- **Parâmetros de Caminho**:
  - `task_id`: Identificador da tarefa a ser excluída.

### Deletar Usuário (User)
- **Nome**: User
- **URL**: `http://127.0.0.1:8000/users/{user_id}/`
- **Método**: DELETE
- **Parâmetros de Caminho**:
  - `user_id`: Identificador do usuário a ser excluído.

### Obter Usuários (Users)
- **Nome**: Users
- **URL**: `http://127.0.0.1:8000/users/`
- **Método**: GET

### Atualizar Usuário (User)
- **Nome**: User
- **URL**: `http://127.0.0.1:8000/users/{user_id}/`
- **Método**: PUT
- **Parâmetros de Caminho**:
  - `user_id`: Identificador do usuário a ser atualizado.
- **Corpo**: Os dados do usuário a serem atualizados no formato JSON.

### Criar Tarefa (Task)
- **Nome**: Tasks
- **URL**: `http://127.0.0.1:8000/users/{user_id}/tasks/`
- **Método**: POST
- **Parâmetros de Caminho**:
  - `user_id`: Identificador do usuário ao qual a tarefa será associada.
- **Corpo**: Os dados da nova tarefa a serem criados no formato JSON.

### Obter Usuário (User)
- **Nome**: User
- **URL**: `http://127.0.0.1:8000/users/{user_id}/`
- **Método**: GET
- **Parâmetros de Caminho**:
  - `user_id`: Identificador do usuário a ser obtido.

### Criar Usuário (User)
- **Nome**: User
- **URL**: `http://127.0.0.1:8000/users/`
- **Método**: POST
- **Corpo**: Os dados do novo usuário a serem criados no formato JSON.
