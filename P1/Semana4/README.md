# Atividade Ponderada - Construção de Aplicativo Híbrido com Flutter

## Descrição
Esta aplicação móvel permite ao usuário criar e gerenciar tarefas, além de processar imagens.

## Requisitos do Projeto
- **Frontend**: Desenvolvido em Flutter.
- **Backend:**: Microsserviços.
    - **Gerenciamento de tarefas**: Desenvolvido em microsserviços.
    - **Serviço de logs**: Desenvolvido em microsserviços.
- **Contenerização**: Dockerfile e docker-compose.yml incluídos.
- **Entrega**: README.md com instruções de execução.

## Checkpoints e Prazos
### Checkpoint: Domingo (19/05/2024 - 23h59)
- **Aplicativo Flutter**:
  - Tela de login (sem autenticação de rotas necessária).
  - Cadastro de usuário.
  - Tela para captura de imagens.
- **Backend em Microsserviços**:
  - Cadastro de usuários.
  - Log das ações do usuário (login e criação de conta).

### Entrega Final: Domingo (26/05/2024 - 23h59)
- **Aplicativo Flutter**:
  - Envio de imagens para processamento.
- **Backend em Microsserviços**:
  - Recebimento e processamento de imagens, retorno do resultado ao aplicativo.
  - Log das ações do usuário (login, criação de conta, envio de imagens).
  - Serviço de notificação para o usuário quando o processamento da imagem termina.


## Instalação e Execução
### Pré-requisitos
- [Docker](https://www.docker.com/get-started)
- [Flutter](https://flutter.dev/docs/get-started/install)

### Passos para executar a aplicação

Abra o terminal, navegue até a pasta onde deseja clonar o projeto e siga os passos abaixo:

1. Clone o repositório:
   ```bash
   git clone https://github.com/JvLetsBora/Learnig_go.git

**Iniciando Backend**
   
2. Entre no repositório:
   ```bash
   cd Learnig_go\P1\Semana4

3. Configurar as variáveis de ambiente:
   ```bash
   cmd.exe /c out.bat

4. Suba o backend:
   ```bash
   docker compose up

**Iniciando Frontend**

Em outro terminal, execute as instruções:

5. Entre no frontend:
   ```bash
   cd Learnig_go\P1\flutter_point\flutter_application_1

6. Execute o comando:
   ```bash
   flutter run

Tendo executado todos os passos corretamente, o resultado esperado será aquele visto neste [vídeo](https://driv.dev/docs/get-started/install).