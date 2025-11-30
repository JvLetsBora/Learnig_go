# Integração do HiveMQ com Kafka

## Setup do ambiente 

1. Certifique-se de ter instalado as seguintes tecnologias: 
   - [go](https://rmnicola.github.io/m9-ec-encontros/go)
   - [Mosquitto](https://mosquitto.org)
   - [Docker](https://www.docker.com/get-started/)

## Testes 

Siga a sequência de comandos abaixo para realizar os testes:

1. Observação: É necessário um arquivo '.env' nos diretórios './publisher' e './subscribe' com as seguintes variáveis de ambiente:
- BROKER_ADDR=<ENDEREÇO DO SEU BROKER>
- HIVE_USER=<USUÁRIO DO SEU BROKER>
- HIVE_PSWD=<SENHA DO SEU BROKER>

2. Observação: É necessário um arquivo '.env' no diretórios './' com a seguinte variável de ambiente:
- MSG_TESTE=<Menssagem de teste>

3. Abra dois terminais, para rodar os testes do publisher e subscribe respectivamente.

**Publisher**


1. Entre no diretório usando o comando:
```
   cmd cd \publisher
```

2. Rode o comando de teste:
```
cmd go test
```

**subscriber**
Para realizar este test, é necessário que haja um publicador enviando uma mensagem de teste para o tópico no qual a inscrição está registrada.

1. Entre no diretório usando o comando:
```
cmd cd \subscribe
```

2. Rode o comando de teste:
```
cmd go test
```
Video de funcionamento:
<br>

[link](https://drive.google.com/file/d/17OGo1XEb0LU8GIBGC1YTNF6M6nkG6HpR/view?usp=sharing)
