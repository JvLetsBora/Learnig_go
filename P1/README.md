# Documentação Super ponderada

## Visão Geral
Este projeto é uma demonstração de uma lista de tarefas altamente escalável feita em Flutter com um serviço de adição de filtro a imagens. Abaixo está a descrição das funcionalidades por meio das rotas disponíveis na API.

## Coleção e Metadados
- **Cliente**: Thunder Client
- **Nome da Coleção**: Tasks
- **ID da Coleção**: 0e03eb7e-d1ae-4ab7-9553-261bf2e6a2d1
- **Data de Exportação**: 2024-05-13T19:32:59.790Z
- **Versão**: 1.2
- **Arquivo**: Learnig_go\P1\thunder-collection_Tasks.json

## Rotas

### Deletar Tarefa (Task)
- **Nome**: Task
- **URL**: `http://127.0.0.1:8000/tasks/{task_id}`
- **Método**: DELETE
- **Parâmetros de Caminho**:
  - `task_id`: Identificador da tarefa a ser excluída.
- **Resposta de Sucesso**:
  - Código 200: Tarefa excluída com sucesso.

### Deletar Usuário (User)
- **Nome**: User
- **URL**: `http://127.0.0.1:8000/users/{user_id}/`
- **Método**: DELETE
- **Parâmetros de Caminho**:
  - `user_id`: Identificador do usuário a ser excluído.
- **Resposta de Sucesso**:
  - Código 200: Usuário excluído com sucesso.

### Obter Usuários (Users)
- **Nome**: Users
- **URL**: `http://127.0.0.1:8000/users/`
- **Método**: GET
- **Resposta de Sucesso**:
  - Código 200: Retorna a lista de usuários.

### Atualizar Usuário (User)
- **Nome**: User
- **URL**: `http://127.0.0.1:8000/users/{user_id}/`
- **Método**: PUT
- **Parâmetros de Caminho**:
  - `user_id`: Identificador do usuário a ser atualizado.
- **Corpo**: Os dados do usuário a serem atualizados no formato JSON.
- **Resposta de Sucesso**:
  - Código 200: Usuário atualizado com sucesso.

### Criar Tarefa (Task)
- **Nome**: Tasks
- **URL**: `http://127.0.0.1:8000/users/{user_id}/tasks/`
- **Método**: POST
- **Parâmetros de Caminho**:
  - `user_id`: Identificador do usuário ao qual a tarefa será associada.
- **Corpo**: Os dados da nova tarefa a serem criados no formato JSON.
- **Resposta de Sucesso**:
  - Código 200: Tarefa criada com sucesso.

### Obter Usuário (User)
- **Nome**: User
- **URL**: `http://127.0.0.1:8000/users/{user_id}/`
- **Método**: GET
- **Parâmetros de Caminho**:
  - `user_id`: Identificador do usuário a ser obtido.
- **Resposta de Sucesso**:
  - Código 200: Retorna os detalhes do usuário solicitado.

### Criar Usuário (User)
- **Nome**: User
- **URL**: `http://127.0.0.1:8000/users/`
- **Método**: POST
- **Corpo**: Os dados do novo usuário a serem criados no formato JSON.
- **Resposta de Sucesso**:
  - Código 200: Usuário criado com sucesso.

### Adiciona efeito a uma imagem Usuário (Image)
- **Nome**: User
- **URL**: `http://127.0.0.1:8000/images/uploand`
- **Método**: POST
- **Corpo**: É necessário um input do tipo file.
- **Resposta de Sucesso**:
  - Código 200: Efeito adicionado com sucesso à imagem do usuário.

## Como usar:
Para esta atividade, há dois fluxos disponíveis: um assíncrono e outro síncrono. Abaixo, como utilizar ambos:



## Video demostração:
[Link para o vídeo de funcionamento.](https://drive.google.com/file/d/1x031iFTv7VS8aNb_sddSCPfb8wvZUOMm/view?usp=sharing)