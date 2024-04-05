package main

import (
	"encoding/json"
	"fmt"
	"os"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
	godotenv "github.com/joho/godotenv"
)

type Teste struct {
	emTeste      bool
	testeDuracao int
	textoTeste   *string
}

var connectHandler mqtt.OnConnectHandler = func(client mqtt.Client) {
	fmt.Println("Connected")
}

var connectLostHandler mqtt.ConnectionLostHandler = func(client mqtt.Client, err error) {
	fmt.Printf("Connection lost: %v", err)
}

type Msg_nova struct {
	Msg    string `json:"msg"`
	Codigo int    `json:"codigo"`
}

func mqttStart(teste Teste) {

	messagePubHandler := func(client mqtt.Client, msg mqtt.Message) {
		// Decodificar a carga útil JSON em uma estrutura de dados Go
		var message Msg_nova
		err := json.Unmarshal(msg.Payload(), &message)
		if err != nil {
			fmt.Println("Erro ao decodificar a carga útil JSON:", err)
			return
		}

		if message.Msg != "" {
			fmt.Println(message.Msg)
			*teste.textoTeste = string(message.Msg)
		}

	}
	err := godotenv.Load(".env")
	if err != nil {
		panic("GOOD")
	}

	var broker = os.Getenv("BROKER_ADDR")
	var port = 8883
	opts := mqtt.NewClientOptions()
	opts.AddBroker(fmt.Sprintf("tls://%s:%d", broker, port))
	opts.SetClientID("Subscriber")
	opts.SetUsername(os.Getenv("HIVE_USER"))
	opts.SetPassword(os.Getenv("HIVE_PSWD"))
	opts.SetDefaultPublishHandler(messagePubHandler)
	opts.OnConnect = connectHandler
	opts.OnConnectionLost = connectLostHandler

	client := mqtt.NewClient(opts)
	if token := client.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}

	if token := client.Subscribe("kafika", 1, nil); token.Wait() && token.Error() != nil {
		fmt.Println(token.Error())
		return
	}

	fmt.Println("Subscriber está rodando. Pressione CTRL+C para sair.")
	select {
	case <-time.After(time.Second * time.Duration(teste.testeDuracao)):
		fmt.Println("Cliente desconectado.")
		client.Disconnect(250)

	}

}

// func main() {
// 	var x string = "10"
// 	ponteiro := &x
// 	*ponteiro = "20"
// 	teste := Teste{emTeste: true, testeDuracao: 50, textoTeste: ponteiro}
// 	mqttStart(teste)
// }
