import pygame
import serial
import sys


PORTA = "COM3"
BAUD = 115200

try:
    ser = serial.Serial(PORTA, BAUD, timeout=0.02)
except:
    print("Erro ao abrir porta serial!")
    sys.exit(1)


pygame.init()
LARGURA, ALTURA = 600, 300
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Calibração – Raspberry Pi Pico")

fonte = pygame.font.SysFont("arial", 32)
fonte_menor = pygame.font.SysFont("arial", 24)

COR_FUNDO = (20, 20, 20)
COR_TEXTO = (255, 255, 255)
COR_BARRA = (0, 200, 255)
COR_ALERTA = (255, 180, 0)

estado = "aguardando"   # aguardando | calibrando | calibrado | lendo

valor = 0.0
raw = 0
calib_min = None
calib_max = None

clock = pygame.time.Clock()


def escreve(texto, x, y, cor=COR_TEXTO, fonte_sel=fonte):
    img = fonte_sel.render(texto, True, cor)
    tela.blit(img, (x, y))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ser.close()
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                ser.close()
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_SPACE and estado == "aguardando":
                ser.write(b"CALIB_START\n")
                estado = "calibrando"


    try:
        linha = ser.readline().decode().strip()

        if not linha:
            pass
        elif linha.startswith("RAW:"):
            raw = int(linha.split(":")[1])
        elif linha.startswith("VAL:"):
            valor = float(linha.split(":")[1])
            estado = "lendo"
        elif linha.startswith("CALIB:START"):
            estado = "calibrando"
        elif linha.startswith("CALIB:OK:"):
            partes = linha.split(":")
            calib_min = int(partes[2].split(",")[0])
            calib_max = int(partes[2].split(",")[1])
            estado = "calibrado"

    except:
        pass


    tela.fill(COR_FUNDO)

    if estado == "aguardando":
        escreve("Pressione ESPAÇO para iniciar a calibração", 30, 40, COR_ALERTA)
        escreve("Aguarda comando...", 30, 120)

    elif estado == "calibrando":
        escreve("CALIBRANDO…", 30, 40, COR_ALERTA)
        escreve(f"Valor bruto (gire o potenciômetro): {raw}", 30, 120)
        pygame.draw.rect(tela, COR_BARRA, (30, 180, raw % (LARGURA - 60), 40))

    elif estado == "calibrado":
        escreve("Calibração concluída!", 30, 40, (0,255,0))
        escreve(f"Mínimo: {calib_min}", 30, 120)
        escreve(f"Máximo: {calib_max}", 30, 160)
        escreve("Aguardando valores escalados…", 30, 220)

    elif estado == "lendo":
        escreve(f"Valor escalado: {valor:.2f}%", 30, 40)
        largura_barra = int((valor / 100) * (LARGURA - 60))
        pygame.draw.rect(tela, COR_BARRA, (30, 120, largura_barra, 40))
        escreve("Pressione ESC para sair", 30, 200, COR_ALERTA)

    pygame.display.update()
    clock.tick(60)



















