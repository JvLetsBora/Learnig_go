# jogo_pico_pygame_clean.py
import threading, queue, time, serial, pygame

SERIAL_PORT = "COM3"
BAUD_RATE = 115200
SERIAL_TIMEOUT = 0.1
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
rx_queue = queue.Queue()
ser_lock = threading.Lock()
running = True
serial_conn = None
_last_send_ms = 0
_last_send_ms_lock = threading.Lock()

def serial_reader_thread(port, baud, timeout, rx_q):
    global serial_conn, running, pico_value
    while running:
        try:
            if serial_conn is None:
                try:
                    serial_conn = serial.Serial(port, baud, timeout=timeout)
                    try:
                        serial_conn.reset_input_buffer(); serial_conn.reset_output_buffer()
                    except Exception:
                        pass
                except Exception:
                    serial_conn = None
                    time.sleep(RECONNECT_INTERVAL)
                    continue
            line_bytes = serial_conn.readline()
            if not line_bytes:
                continue
            try:
                line = line_bytes.decode('utf-8', errors='ignore').strip()
            except:
                line = repr(line_bytes)
            try:
                rx_q.put_nowait(line)
            except queue.Full:
                pass
            if line.upper().startswith("VAL:"):
                parts = line.split(":", 1)
                if len(parts) == 2:
                    try:
                        v = float(parts[1])
                        with pico_lock:
                            pico_value = v
                    except:
                        pass
        except Exception:
            try:
                if serial_conn: serial_conn.close()
            except:
                pass
            serial_conn = None
            time.sleep(RECONNECT_INTERVAL)
    try:
        if serial_conn: serial_conn.close()
    except:
        pass
    serial_conn = None

def serial_writer_thread():
    global serial_conn, running
    while running:
        try:
            cmd = cmd_queue.get(timeout=0.1)
        except queue.Empty:
            continue
        if not isinstance(cmd, (bytes, bytearray)):
            try:
                cmd = str(cmd).encode()
            except:
                continue
        wrote = False
        write_attempt_time = time.time()
        while running and not wrote:
            if serial_conn is None:
                time.sleep(0.05)
                if time.time() - write_attempt_time > 5.0:
                    break
                continue
            try:
                with ser_lock:
                    serial_conn.write(cmd)
                    try:
                        serial_conn.flush()
                    except Exception:
                        pass
                wrote = True
            except Exception:
                try:
                    serial_conn.close()
                except:
                    pass
                serial_conn = None
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
        line_str = line_str + "\n"
    try:
        cmd_queue.put_nowait(line_str.encode("utf-8"))
        return True
    except queue.Full:
        return False

def led_on(): send_command_ascii("LED:ON")
def led_off(): send_command_ascii("LED:OFF")
def led_pwm(v): send_command_ascii(f"LED:PWM:{max(0,min(255,int(v)))}")

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
        inside = (TARGET_MIN <= val <= TARGET_MAX)
        if not victory:
            if inside:
                stability_timer += dt
                led_pwm(10)
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
        pygame.draw.circle(screen, color, (WIDTH // 2, HEIGHT // 2), radius)
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
    t_reader = threading.Thread(target=serial_reader_thread, args=(SERIAL_PORT, BAUD_RATE, SERIAL_TIMEOUT, rx_queue), daemon=True)
    t_writer = threading.Thread(target=serial_writer_thread, daemon=True)
    t_reader.start(); t_writer.start()
    try:
        run_game()
    except KeyboardInterrupt:
        running = False
    running = False
    time.sleep(0.15)
    print("Finalizado.")
