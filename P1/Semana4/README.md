# Atividade Ponderada - Construção de Aplicativo Híbrido com Flutter

## Descrição
Esta atividade consiste em construir uma aplicação Flutter e um backend com microsserviço. A Ultima versão do backend se encontra em: 'Learnig_go\P1\checkpoint\async'.

## Requisitos do Projeto
- **Frontend**: Desenvolvido em Flutter.
- **Backend:**: Desenvolvido em microsserviços.
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
1. Clone o repositório:
   ```bash
   git clone https://github.com/JvLetsBora/Learnig_go.git
   cd C:\Users\jvoli\Documents\Learnig_go\P1\checkpoint\async
