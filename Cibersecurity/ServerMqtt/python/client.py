import time
import paho.mqtt.client as paho
from paho import mqtt

class ClienteMQTT:
    def __init__(self, client_id, username, password, broker, port, topic_subscribe):
        self.client = paho.Client(client_id=client_id, protocol=paho.MQTTv5)
        self.client.username_pw_set(username, password)
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.broker = broker
        self.port = port
        self.topic_subscribe = topic_subscribe
        
        # Configurar callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.on_publish = self.on_publish

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print(f"Cliente {client._client_id.decode()} conectado ao broker com código {rc}")
        self.client.subscribe(self.topic_subscribe, qos=1)

    def on_message(self, client, userdata, msg):
        print(f"[{msg.topic}] {msg.payload.decode()}")

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print(f"Cliente {client._client_id.decode()} inscrito no tópico. QoS: {granted_qos}")

    def on_publish(self, client, userdata, mid, properties=None):
        print(f"Mensagem publicada com ID {mid}")

    def conectar(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def publicar(self, topico, mensagem):
        self.client.publish(topico, payload=mensagem, qos=1)

    def desconectar(self):
        self.client.loop_stop()
        self.client.disconnect()


class ServidorMQTT:
    def __init__(self, username, password, broker, port):
        self.clientes = []
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password

    def adicionar_cliente(self, client_id, topic_subscribe):
        cliente = ClienteMQTT(
            client_id=client_id,
            username=self.username,
            password=self.password,
            broker=self.broker,
            port=self.port,
            topic_subscribe=topic_subscribe,
        )
        self.clientes.append(cliente)
        return cliente

    def iniciar(self):
        for cliente in self.clientes:
            cliente.conectar()

    def parar(self):
        for cliente in self.clientes:
            cliente.desconectar()


# Exemplo de uso
if __name__ == "__main__":
    broker = "2638385848004a349ca166f397873de7.s1.eu.hivemq.cloud"
    port = 8883
    username = "admin"
    password = "Admin1234"
    topic_subscribe = "serviço/grupo2"

    # Criar servidor e adicionar clientes
    servidor = ServidorMQTT(username, password, broker, port)

    cliente1 = servidor.adicionar_cliente(client_id="cliente1", topic_subscribe=topic_subscribe)
    cliente2 = servidor.adicionar_cliente(client_id="cliente2", topic_subscribe=topic_subscribe)

    servidor.iniciar()

    # Publicar mensagens
    time.sleep(1)  # Aguardar conexão
    cliente1.publicar("serviço/grupo2", "Katalan On")
    cliente2.publicar("serviço/grupo2", "Enrique On")

    time.sleep(5)  # Manter o programa em execução para testes
    servidor.parar()
