import pygame
import serial
import sys

# -----------------------------
# CONFIG SERIAL
# -----------------------------
PORTA = "COM3"        
BAUD = 115200

try:
    ser = serial.Serial(PORTA, BAUD, timeout=0.02)
except:
    print("Erro ao abrir porta serial!")
    sys.exit(1)

# -----------------------------
# CONFIG PYGAME
# -----------------------------
pygame.init()
LARGURA, ALTURA = 500, 200
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Leitura do Pico – Pygame Monitor")

fonte = pygame.font.SysFont("arial", 32)

# cores
COR_FUNDO = (20, 20, 20)
COR_TEXTO = (255, 255, 255)
COR_BARRA = (0, 200, 255)

valor = 0.0  # valor lido do Pico


# -----------------------------
# LOOP PRINCIPAL
# -----------------------------
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ser.close()
            pygame.quit()
            sys.exit()

    # -----------------------------
    # LER SERIAL
    # -----------------------------
    try:
        linha = ser.readline().decode().strip()
        if linha.startswith("VAL:"):
            valor_str = linha.split(":")[1]
            valor = float(valor_str)
    except:
        pass

    # -----------------------------
    # DESENHO NA TELA
    # -----------------------------
    tela.fill(COR_FUNDO)

    # Texto grande do valor
    txt = fonte.render(f"Valor: {valor:.2f}%", True, COR_TEXTO)
    tela.blit(txt, (20, 20))

    # Barra proporcional
    largura_barra = int((valor) * (LARGURA - 40))
    pygame.draw.rect(tela, COR_BARRA, (20, 100, largura_barra, 40))

    pygame.display.update()
    clock.tick(60)
