# **Equilibre o Núcleo**

### **Entrega – Projeto com Integração Hardware** — *28/11/2025*

<img src="74480903-efcf-48e4-af89-e833f345bb5d.png" width="260">

---

## **Objetivo do Projeto**

Desenvolver um **jogo interativo** onde o jogador deve **equilibrar o núcleo** mantendo o valor lido pelo potenciômetro dentro da faixa **40% a 60%**.

A leitura é feita pelo **Raspberry Pi Pico W**, enviada via **TCP/WiFi** para o PC, onde um jogo em **Pygame** processa, exibe e controla a lógica.

---

## **Resumo do Funcionamento**

* O **Pico W** lê continuamente um potenciômetro (ADC).
* Mapeia o valor de **0–65535 → 0–100%**.
* Envia ao PC usando TCP (`VAL:xx.xx`).
* O PC exibe a leitura e roda o jogo:

  * O jogador deve manter o valor entre `40–60`.
  * Reinicia se sair da faixa por muito tempo.
  * Ganha após manter por **8 segundos**.
* O PC envia comandos para o Pico:

  * `LED:ON`, `LED:OFF`
  * `COMMAND:START_GAME`
  * `COMMAND:PING`
* O Pico pisca LED, processa comandos e controla dificuldade ao longo do tempo.

---

## **Estrutura do Projeto**

```
.
├── pc_code/
│   ├── main.py          # Jogo completo + TCP client
│   ├── test_led.py      # Envia comandos de LED
│   ├── test_pwm.py      # Lê valores e mostra barra em pygame
│   └── py.py            # Testes diversos
│
├── resp_code/
│   └── main.py          # Código principal do Pico W (servidor TCP)
│
└── README.md            # Este arquivo
```

---

# **To-Do List**

### Hardware

* [ ] Montagem: potenciômetro → ADC (GP26)
* [ ] LED → GP21
* [ ] Teste de alimentação e GND comum

### Raspberry Pi Pico W

* [ ] Conexão automática ao WiFi
* [ ] Servidor TCP escutando porta **8000**
* [ ] Envio periódico de `VAL:x.xx`
* [ ] Interpretação de comandos do PC
* [ ] Lógica do jogo (piscar LED, tensão crescente)
* [ ] Tratamento de desconexão

### Código no PC (Pygame)

* [ ] Conexão TCP com reconexão automática
* [ ] Leitura e filtro com noise
* [ ] Renderização do jogo (círculo + barra + HUD)
* [ ] Lógica de vitória
* [ ] Lógica de estabilidade

---

# **Como Executar**

---

## **No Raspberry Pi Pico W**

Copiar para o Pico:

```
resp_code/main.py
```

Editar no topo:

```python
WIFI_SSID = "NOME_DA_REDE"
WIFI_PASS = "SENHA"
PORT = 8000
```

Rodar:

* Conecta ao WiFi
* Mostra IP na serial
* Abre servidor TCP
* Começa a enviar `VAL:` automaticamente

---

## **No PC – Jogo Completo**

Arquivo:

```
pc_code/main.py
```

Antes de rodar, ajustar o IP do Pico:

```python
PICO_HOST = "xxx.xxx.xxx.xxx"   # IP do Pico
PICO_PORT = 8000
```

Rodar:

```
python main.py
```

O fluxo será:

1. Teste inicial → envia `PING`
2. Pico responde `PONG`
3. Abre o menu
4. Clique em **Iniciar Jogo**

---

## **Testes Avulsos**

### **Testar leitura e barra gráfica**

```
pc_code/test_pwm.py
python test_pwm.py
```

Mostra valor e barra animada.

---

### **Testar LED**

```
pc_code/test_led.py
```

---

# **Regras do Jogo**

| Evento                  | Detalhe                                        |
| ----------------------- | ---------------------------------------------- |
| **Objetivo**            | Manter valor entre **40 e 60%**                |
| **Tempo necessário**    | 8 segundos                                     |
| **Se sair da faixa**    | Relógio de estabilidade diminui                |
| **Vitória**             | LED pisca rápido                               |
| **Dificuldade no Pico** | “Tensão” aumenta gradualmente e acelera o loop |
| **Timeout final**       | Pico envia `LOSER_TIMEOUT`                     |

---

# **Protocolos de Comunicação**

### *Pico → PC*

```
VAL:xx.xx
LOSER_TIMEOUT
```

### *PC → Pico*

```
COMMAND:PING
COMMAND:START_GAME
LED:ON
LED:OFF
```

---

# **Arquivos Importantes**

---

## `pc_code/main.py`

* Cliente TCP com reconexão
* Thread de leitura
* Thread de escrita
* Jogo completo em Pygame
* Noise controlado para simulação
* HUD, barra, círculo, vitória, perda

---

## `pc_code/test_pwm.py`

* Leitura serial simples
* Exibição gráfica do valor
* Útil para calibrar potenciômetro

---

## `resp_code/main.py` (Pico W)

* Conexão WiFi
* Servidor TCP
* Mapeamento ADC → 0–100%
* Interpretação de comandos
* Envio periódico de valores
* Controle físico do LED
* Mecânica de “tensão crescente”

---

# **Checklist de Entrega**

### Hardware

* [ ] Protoboard montada
* [ ] Potenciômetro calibrado
* [ ] LED funcional

### Software

* [ ] Pico conecta ao WiFi
* [ ] PC conecta ao Pico
* [ ] Jogo inicia
* [ ] LED responde aos comandos
* [ ] Vitória funcional
* [ ] Timeout funcional
