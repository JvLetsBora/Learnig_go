package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"os"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
	godotenv "github.com/joho/godotenv"
)

var connectHandler mqtt.OnConnectHandler = func(client mqtt.Client) {
	fmt.Println("Connected")
}

var connectLostHandler mqtt.ConnectionLostHandler = func(client mqtt.Client, err error) {
	fmt.Printf("Connection lost: %v", err)
}

type Teste struct {
	testeDuracao int
	msg          string
	testing      bool
}

type Msg_nova struct {
	Msg    string `json:"msg"`
	Codigo int    `json:"codigo"`
}

type Loja struct {
	Freezer   SensorData `json:"Freezer"`
	Geladeira SensorData `json:"Geladeira"`
}

type SensorData struct {
	SensorId    string `json:"sensor_id"`
	Timestamp   int64  `json:"timestamp"`
	Tipo        string `json:"Tipo"`
	Temperatura int    `json:"Temperatura"`
	Limite      int
	min         int
	max         int
}

func NovaLoja() Loja {
	return Loja{
		Freezer:   NovoSensor("Freezer", -28, 0, "lj98b01"),
		Geladeira: NovoSensor("Geladeira", -2, 20, "lj01f01"),
	}
}

func nova_msg(t Teste) Msg_nova {
	return Msg_nova{
		Msg:    t.msg,
		Codigo: t.testeDuracao,
	}
}

func NovoSensor(tipo string, min int, max int, id string) SensorData {
	return SensorData{
		SensorId:    id,
		Timestamp:   time.Now().Unix(),
		Tipo:        tipo,
		Temperatura: rand.Intn(int(max-min)) + int(min),
		Limite:      8,
		min:         min,
		max:         max,
	}
}

var condition = 0

func publiStart(teste Teste) {

	err := godotenv.Load(".env")
	if err != nil {
		fmt.Printf("Error loading .env file: %s", err)
	}

	var broker = os.Getenv("BROKER_ADDR")
	var port = 8883
	opts := mqtt.NewClientOptions()
	opts.AddBroker(fmt.Sprintf("tls://%s:%d", broker, port))
	opts.SetClientID("Publisher")
	opts.SetUsername(os.Getenv("HIVE_USER"))
	opts.SetPassword(os.Getenv("HIVE_PSWD"))
	opts.OnConnect = connectHandler
	opts.OnConnectionLost = connectLostHandler

	client := mqtt.NewClient(opts)
	if token := client.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}
	condition = teste.testeDuracao
	if teste.testing {
		for condition >= 0 {

			time.Sleep(time.Duration(1 * time.Second))
			condition -= 1
			currentData := nova_msg(teste)
			jsonData, _ := json.Marshal(currentData)
			token := client.Publish("qualidadeAr", 1, false, jsonData)
			token.Wait()
			fmt.Println(string(jsonData))

		}
	} else {
		currentData := NovaLoja()
		jsonData, _ := json.Marshal(currentData)
		token := client.Publish("qualidadeAr", 1, false, jsonData)
		token.Wait()
		fmt.Println(string(jsonData))
	}
	select {
	case <-time.After(time.Second * time.Duration(teste.testeDuracao)):
		fmt.Println("Cliente desconectado.")
		condition = 0
		client.Disconnect(250)

	}
}

// func main() {
// 	teste := Teste{testeDuracao: 30, msg: "oi"}
// 	publiStart(teste)
// }
