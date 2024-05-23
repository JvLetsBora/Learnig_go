# Atividade Ponderada - Construção de Aplicativo Híbrido com Flutter

## Descrição
Esta atividade consiste em construir uma aplicação Flutter, a ser realizada em sala de aula seguindo as orientações fornecidas. A entrega deve ocorrer via GitHub e a aplicação deve utilizar um backend fornecido, desenvolvido obrigatoriamente em microsserviços, preferencialmente em Python. A aplicação deve estar conteinerizada e incluir Dockerfile e docker-compose.yml. O repositório deve conter um README.md com instruções de execução.

## Requisitos do Projeto
- **Frontend**: Desenvolvido em Flutter.
- **Backend**: Desenvolvido em microsserviços.
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

## Barema de Correção
| Faixa de Nota | Conceito                | Descrição |
|---------------|-------------------------|-----------|
| 0 - 2         | Não Iniciou             | O desenvolvimento do projeto não foi totalmente iniciado. Utilizou apenas templates iniciais. Não há integração entre as partes do sistema. |
| 2.1 - 4       | Entrega Incompleta      | Aplicações iniciadas, mas não integradas. O aplicativo mobile não segue padrões abordados. O backend não é em microsserviços e/ou não está containerizado. |
| 4.1 - 6       | Atende Parcialmente     | Aplicativo desenvolvido e parcialmente integrado com o backend. Backend em arquitetura monolítica e com funcionalidades incompletas. |
| 6.1 - 9       | Atendeu os requisitos   | O aplicativo e o backend foram desenvolvidos e estão integrados. Backend em microsserviços e containerizado. Algumas funcionalidades podem estar incompletas. |
| 9.1 - 10      | Supera os requisitos    | O aplicativo e o backend foram desenvolvidos, estão integrados e todas as funcionalidades foram implementadas. Backend em microsserviços, containerizado e com implementações adicionais que melhoram a qualidade do projeto. |

## Instalação e Execução
### Pré-requisitos
- [Docker](https://www.docker.com/get-started)
- [Flutter](https://flutter.dev/docs/get-started/install)

### Passos para executar a aplicação
1. Clone o repositório:
   ```bash
   git clone <URL-do-repositório>
   cd <nome-do-repositório>
