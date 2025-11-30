import paho.mqtt.client as mqtt

# Configurações do broker HiveMQ Cloud
BROKER = "2638385848004a349ca166f397873de7.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "admin"  # Substitua pelo usuário do HiveMQ
PASSWORD = "Admin1234"  # Substitua pela senha do HiveMQ
TOPIC = "kafika"  # Tópico usado pelo Publisher

# Alfabeto para a cifra de César
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def decrypt_cesar_cipher(data, key):
    """Descriptografa uma mensagem criptografada com a cifra de César."""
    result = []
    chunk_count = 0

    for char in data:
        if char != " ":
            is_upper = char.isupper()
            char = char.lower()
            if char in ALPHABET:
                index = (ALPHABET.index(char) - key) % len(ALPHABET)
                char = ALPHABET[index]
                if is_upper:
                    char = char.upper()
                key = (key + 1) % len(ALPHABET)
        else:
            chunk_count += 2
            key = (key + chunk_count) % len(ALPHABET)
        result.append(char)

    return "".join(result)


# Callback para conexão
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker HiveMQ!")
        client.subscribe(TOPIC)
    else:
        print(f"Falha ao conectar. Código de erro: {rc}")

# Callback para recebimento de mensagens
def on_message(client, userdata, msg):
    encrypted_msg = msg.payload.decode("utf-8")
    print(f"Mensagem criptografada recebida no tópico '{msg.topic}': {encrypted_msg}")

    # Descriptografar a mensagem
    decrypted_msg = decrypt_cesar_cipher(encrypted_msg, 3)
    print(f"Mensagem descriptografada: {decrypted_msg}")

# Configuração do cliente MQTT
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()  # Habilita TLS para conexão segura

client.on_connect = on_connect
client.on_message = on_message

# Conexão ao broker
print("Conectando ao broker MQTT...")
client.connect(BROKER, PORT)

# Loop para manter o cliente ativo
client.loop_forever()
