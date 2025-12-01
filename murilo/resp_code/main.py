from machine import ADC, Pin
import network
import socket
import time
import sys

WIFI_SSID = "Redmi 9C NFC"
WIFI_PASS = "Sacola1234"
PORT = 8000

def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)

    print("Conectando ao WiFi...")
    while not wlan.isconnected():
        time.sleep(0.3)

    print("Conectado! IP:", wlan.ifconfig()[0])
    return wlan.ifconfig()[0]

def start_server():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', PORT))
    s.listen(1)
    s.settimeout(1)
    print("Aguardando cliente na porta", PORT)
    return s

ADC_PIN = 26
LED_PIN = 21
SAMPLE_INTERVAL_MS = 50

CALIB_MIN = 0
CALIB_MAX = 65535

adc = ADC(ADC_PIN)
led_pin = Pin(LED_PIN, Pin.OUT)

rx_buffer = bytearray()
client = None
is_game_on = False

ema_val = None
last_send_ms = 0
last_sent_mapped = None

def map_raw_to_0_100(raw):
    r = max(CALIB_MIN, min(CALIB_MAX, raw))
    return (r / 65535.0) * 100.0

def tcp_send(line):
    global client
    if client is None:
        return
    
    if not line.endswith("\n"):
        line += "\n"

    try:
        client.send(line.encode())
    except:
        try:
            client.close()
        except:
            pass
        client = None

def handle_command(line):
    global is_game_on
    line = line.strip()
    if not line:
        return

    print("CMD:", line)

    parts = line.split(":")

    if parts[0].upper() == "LED":
        if len(parts) >= 2:
            if parts[1].upper() == "ON":
                led_pin.value(1)
            elif parts[1].upper() == "OFF":
                led_pin.value(0)

    elif parts[0].upper() == "COMMAND":
        cmd = parts[1].upper()

        if cmd == "PING":
            tcp_send("PONG")

        elif cmd == "START_GAME":
            is_game_on = True
            print("Jogo iniciado!")

TENSION_START = 0.1
TENSION_MAX = 10
TENSION_STEP = 0.1
TENSION_INTERVAL_MS = 200
tension = TENSION_START
last_tension_ms = time.ticks_ms()

wifi_connect()
server = start_server()

last_sample_ms = time.ticks_ms()
game_time = SAMPLE_INTERVAL_MS
tic = 0

print("\nServidor pronto!\n")

while True:

    if client is None:
        try:
            client, addr = server.accept()
            client.settimeout(0.1)
            print("Cliente conectado:", addr)
            rx_buffer = bytearray()
        except:
            pass

    now = time.ticks_ms()

    if time.ticks_diff(now, last_sample_ms) >= SAMPLE_INTERVAL_MS:
        last_sample_ms = now
        raw = adc.read_u16()
        mapped = map_raw_to_0_100(raw)
        tcp_send(f"VAL:{mapped:.2f}")

    if client:
        try:
            data = client.recv(128)
            if data:
                for b in data:
                    if b == 10:  # '\n'
                        handle_command(rx_buffer.decode())
                        rx_buffer = bytearray()
                    else:
                        rx_buffer.append(b)
        except:
            pass

    if is_game_on:

        tic = not tic
        led_pin.value(tic)

        # Tensão aumenta com o tempo
        if time.ticks_diff(now, last_tension_ms) >= TENSION_INTERVAL_MS:
            last_tension_ms = now

            if tension < TENSION_MAX:
                tension += TENSION_STEP
            else:
                tcp_send("LOSER_TIMEOUT")
                print("Fim — Tensão máxima atingida")
                led_pin.value(0)
                break

        # Reduz sleep conforme tensão aumenta
        game_time = int(1000 / (tension + 1))

    time.sleep_ms(game_time)


