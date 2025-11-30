package main

import (
	"fmt"
	"os"
	"testing"

	godotenv "github.com/joho/godotenv"
)

func TestMainConnected(t *testing.T) {
	err := godotenv.Load("../.env")
	if err != nil {
		fmt.Printf("Error loading .env file: %s", err)
	}

	var msg_test = os.Getenv("MSG_TESTE")
	//time.Sleep(2 * time.Second)
	teste := Teste{testeDuracao: 10, msg: msg_test, testing: true}
	publiStart(teste)
}
