import threading, queue, time, socket, pygame
import random

PICO_HOST = "192.168.43.206"
PICO_PORT = 8009
RECONNECT_INTERVAL = 2.0
SEND_THROTTLE_MS = 40

WIDTH, HEIGHT = 900, 600
FPS = 60
TARGET_MIN = 40
TARGET_MAX = 60
WIN_TIME = 8.0

pico_value = 0.0
pico_lock = threading.Lock()
cmd_queue = queue.Queue()
rx_queue = queue.Queue(maxsize=200)
sock_lock = threading.Lock()
running = True

_last_send_ms = 0
_last_send_ms_lock = threading.Lock()

sock = None


def read_with_noise(value, noise_level=0.05):
    noise = (random.random() * 2 - 1) * noise_level
    return value * (1 + noise)





def tcp_reader_thread(host, port, rx_q):
    global sock, running, pico_value
    while running:
        if sock is None:
            try:
                s = socket.socket()
                s.settimeout(5.0)
                s.connect((host, port))
                s.settimeout(0.5)  # timeout para recv não bloquear muito
                with sock_lock:
                    sock = s
                print("Conectado ao Pico:", host, port)
            except Exception as e:
                # falha ao conectar
                try:
                    s.close()
                except:
                    pass
                sock = None
                # aguardar e tentar de novo
                time.sleep(RECONNECT_INTERVAL)
                continue

        # se conectado, leia dados
        try:
            data = sock.recv(4096)
            if not data:
                # desconectou
                print("Desconectado pelo servidor")
                try:
                    sock.close()
                except:
                    pass
                sock = None
                time.sleep(RECONNECT_INTERVAL)
                continue

            # dividir por linhas (pode vir várias linhas)
            try:
                text = data.decode('utf-8', errors='ignore')
            except:
                text = repr(data)

            lines = text.split("\n")
            for line in lines:
                if not line:
                    continue

                try:
                    rx_q.put_nowait(line)
                except queue.Full:
                    pass

                # interpreta VAL:
                if line.upper().startswith("VAL:"):
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        try:
                            v = float(parts[1])
                            with pico_lock:
                                pico_value = read_with_noise(v, 0.05)
                        except:
                            pass

        except socket.timeout:
            # sem dados, continue loop para checar comandos a enviar
            pass
        except Exception as e:
            print("Erro no recv:", e)
            try:
                if sock:
                    sock.close()
            except:
                pass
            sock = None
            time.sleep(RECONNECT_INTERVAL)

    try:
        if sock:
            sock.close()
    except:
        pass
    sock = None

def tcp_writer_thread():
    global sock, running
    while running:
        try:
            cmd = cmd_queue.get(timeout=0.1)
        except queue.Empty:
            continue

        if not isinstance(cmd, (bytes, bytearray)):
            try:
                cmd = str(cmd).encode('utf-8')
            except:
                continue

        wrote = False
        start_time = time.time()

        while running and not wrote:
            if sock is None:
                time.sleep(0.05)
                if time.time() - start_time > 5.0:
                    break
                continue

            try:
                with sock_lock:
                    sock.sendall(cmd)
                wrote = True
            except Exception as e:
                print("Erro ao enviar:", e)
                try:
                    if sock:
                        sock.close()
                except:
                    pass
                sock = None
                time.sleep(0.1)

        time.sleep(0.01)

def send_command_ascii(line_str):
    global _last_send_ms
    now_ms = int(time.time() * 1000)
    with _last_send_ms_lock:
        if now_ms - _last_send_ms < SEND_THROTTLE_MS:
            return False
        _last_send_ms = now_ms

    if not line_str.endswith("\n"):
        line_str += "\n"

    try:
        cmd_queue.put_nowait(line_str.encode("utf-8"))
        return True
    except queue.Full:
        return False

def led_on():  send_command_ascii("LED:ON")
def led_off(): send_command_ascii("LED:OFF")
def start_game(): send_command_ascii("COMMAND:START_GAME")
def win(): send_command_ascii("COMMAND:WIN")

def run_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menu - Equilibre o Núcleo")

    font = pygame.font.SysFont("Arial", 48)
    small_font = pygame.font.SysFont("Arial", 32)

    clock = pygame.time.Clock()
    menu_running = True

    button_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 50, 300, 100)

    while menu_running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(ev.pos):
                    start_game()
                    time.sleep(0.2)
                    run_game()
                    return

        screen.fill((10, 10, 25))

        # Título
        title = font.render("Equilibre o Núcleo", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        # Botão
        pygame.draw.rect(screen, (50, 120, 255), button_rect, border_radius=20)
        txt = small_font.render("Iniciar Jogo", True, (255, 255, 255))
        screen.blit(txt, (button_rect.centerx - txt.get_width()//2,
                          button_rect.centery - txt.get_height()//2))

        pygame.display.flip()
        clock.tick(60)

def run_game():
    global running, pico_value

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Equilibre o Núcleo (Integrado ao Pico)")

    font = pygame.font.SysFont("Arial", 32)
    clock = pygame.time.Clock()

    stability_timer = 0.0
    blink_timer = 0.0
    victory = False

    while running:
        dt = clock.tick(FPS) / 1000.0

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

        with pico_lock:
            val = pico_value

        inside = TARGET_MIN <= val <= TARGET_MAX

        if not victory:
            if inside:
                stability_timer += dt
            else:
                stability_timer = max(0.0, stability_timer - dt * 1.2)
                led_on()

            if stability_timer >= WIN_TIME:
                victory = True
                blink_timer = 0.0
                led_off()
        else:
            blink_timer += dt
            if int(blink_timer * 4) % 2 == 0:
                led_on()
            else:
                led_off()

        screen.fill((5, 5, 12))

        radius = 80 + int((val - 50) * 3)
        radius = max(20, min(radius, 200))

        color = (0, 150, 255) if inside else (255, 40, 40)
        pygame.draw.circle(screen, color, (WIDTH//2, HEIGHT//2), radius)

        pygame.draw.rect(screen, (40, 40, 40), (250, 500, 400, 20))
        bw = max(0, min(400, int(4 * val)))
        pygame.draw.rect(screen, color, (250, 500, bw, 20))

        screen.blit(font.render(f"Valor: {val:.2f}", True, (255, 255, 255)), (20, 20))
        screen.blit(font.render(f"Mantenha entre {TARGET_MIN} e {TARGET_MAX}", True, (255, 255, 255)), (20, 60))
        screen.blit(font.render(f"Estabilidade: {stability_timer:.1f}s", True, (255, 255, 255)), (20, 100))

        if victory:
            msg = font.render("Você estabilizou o núcleo!", True, (255, 255, 100))
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 180))

        pygame.display.flip()

    led_off()
    time.sleep(0.05)
    pygame.quit()

if __name__ == "__main__":
    t_reader = threading.Thread(target=tcp_reader_thread, args=(PICO_HOST, PICO_PORT, rx_queue), daemon=True)
    t_writer = threading.Thread(target=tcp_writer_thread, daemon=True)

    t_reader.start()
    t_writer.start()

    print("\n Testando conexão TCP com o Pico...")

    # envia PING
    send_command_ascii("COMMAND:PING")
    time.sleep(1.0)

    test_ok = False
    while not rx_queue.empty():
        linha = rx_queue.get()
        print("RX →", linha)
        if "PONG" in linha:
            test_ok = True

    if test_ok:
        print("Conexão OK! Pico respondeu ao PING.\n")
    else:
        print("Pico NÃO respondeu ao PING. Verifique IP/Firewall/Se está conectado.\n")

    try:
        run_menu()
    except KeyboardInterrupt:
        running = False

    running = False
    time.sleep(0.15)
    print("Finalizado.")
