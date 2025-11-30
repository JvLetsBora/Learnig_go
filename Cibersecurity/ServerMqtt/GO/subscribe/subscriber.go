package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
	godotenv "github.com/joho/godotenv"
)

type Teste struct {
	emTeste      bool
	testeDuracao int
	textoTeste   *string
}

// Alfabeto utilizado para a cifra
const alphabet = "abcdefghijklmnopqrstuvwxyz"

// Função para criptografar usando a Cifra de César
func cesarCipher(data string, key int) string {
	var result strings.Builder
	chunkCount := 0

	for _, char := range data {
		if char != ' ' {
			isUpper := char >= 'A' && char <= 'Z'
			char = rune(strings.ToLower(string(char))[0])
			index := strings.IndexRune(alphabet, char)

			if index != -1 {
				index = (index + key) % len(alphabet)
				char = rune(alphabet[index])
				if isUpper {
					char = rune(strings.ToUpper(string(char))[0])
				}
				key = (key + 1) % len(alphabet)
			}
		} else {
			chunkCount += 2
			key = (key + chunkCount) % len(alphabet)
		}
		result.WriteRune(char)
	}

	return strings.ToLower(result.String())
}

// Função para descriptografar usando a Cifra de César
func decryptCesarCipher(data string, key int) string {
	var result strings.Builder
	chunkCount := 0

	for _, char := range data {
		if char != ' ' {
			isUpper := char >= 'A' && char <= 'Z'
			char = rune(strings.ToLower(string(char))[0])
			index := strings.IndexRune(alphabet, char)

			if index != -1 {
				index = (index + len(alphabet) - key) % len(alphabet)
				char = rune(alphabet[index])
				if isUpper {
					char = rune(strings.ToUpper(string(char))[0])
				}
				key = (key + 1) % len(alphabet)
			}
		} else {
			chunkCount += 2
			key = (key + chunkCount) % len(alphabet)
		}
		result.WriteRune(char)
	}

	return strings.ToLower(result.String())
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
