package main

import (
	"fmt"
	"os"
	"testing"

	godotenv "github.com/joho/godotenv"
)

// TestRecebimento garante que os dados enviados pelo simulador são recebidos pelo broker.
func TestRecebimento(t *testing.T) {

	fmt.Println("-> Teste de Recebimento iniciado.")
	momento_inicial := "nil24613#2335" // Uma sequência de caracteres contrá casualidade
	ponteiro := &momento_inicial
	teste := Teste{emTeste: true, testeDuracao: 3, textoTeste: ponteiro}
	mqttStart(teste)
	if *ponteiro == "nil24613#2335" {
		t.Fatalf("Menssagem não recebida")

	}
	fmt.Println("-> Teste de Recebimento finalizado.")
}

// TestValidacaoDados garante que os dados enviados pelo simulador chegam sem alterações.
func TestValidacaoDados(t *testing.T) {
	err := godotenv.Load("../.env")
	if err != nil {
		fmt.Printf("Error loading .env file: %s", err)
	}

	var msg_test = os.Getenv("MSG_TESTE")

	fmt.Println("-> Teste de validação dos dados iniciado.")
	momento_inicial := "nil24613#2335" // Uma sequência de caracteres contrá casualidade
	ponteiro := &momento_inicial
	teste := Teste{emTeste: true, testeDuracao: 3, textoTeste: ponteiro}
	mqttStart(teste)
	if *ponteiro != msg_test {
		t.Fatalf("A mensagem teste não foi validada! Esperado %s, o que veio foi %s", *ponteiro, msg_test)

	}
	fmt.Println("-> Teste de validação dos dados finalizado.")
}
