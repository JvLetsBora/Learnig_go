import socket
import numpy as np
import cv2  # Para manipulação de imagem, se não tiver, instale via 'pip install opencv-python'
import struct
import time

# Configuração do tempo de execução
timeServerShutdown = 200

def face_detection(image):
    # Conversão de imagem de bytes para formato que o OpenCV entende
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return image

def handle_connection(conn, addr):
    print(f"Conectado por {addr}")

    try:
        # Recebendo o tamanho da imagem
        raw_size = conn.recv(4)
        if not raw_size:
            print("Falha ao receber o tamanho da imagem")
            return

        # Converte o tamanho para inteiro
        img_size = struct.unpack('<I', raw_size)[0]
        print(f"Tamanho da imagem recebido: {img_size} bytes")

        # Recebendo os bytes da imagem
        img_data = b""
        while len(img_data) < img_size:
            packet = conn.recv(img_size - len(img_data))
            if not packet:
                print("Conexão fechada enquanto recebia a imagem.")
                return
            img_data += packet
        
        print("Imagem recebida com sucesso!")

        # Convertendo os bytes para um numpy array de imagem
        np_arr = np.frombuffer(img_data, np.uint8)
        img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img_np is None:
            print("Falha ao decodificar a imagem.")
            return

        # Processamento da imagem (detecção de rostos)
        img_processed = face_detection(img_np)

        # Codificando a imagem processada para enviar de volta
        _, img_encoded = cv2.imencode('.jpg', img_processed)

        # Salva a imagem processada em um arquivo
        cv2.imwrite('./uploads/face_detection.jpg', img_processed)

        img_bytes = img_encoded.tobytes()

        # Enviando o tamanho da imagem processada
        conn.sendall(struct.pack('<I', len(img_bytes)))
        print(f"Enviando imagem processada de {len(img_bytes)} bytes.")

        # Enviando a imagem processada de volta ao ESP32
        conn.sendall(img_bytes)
        print("Imagem processada enviada com sucesso!")
        
    except Exception as e:
        print(f"Erro durante a conexão: {e}")
    finally:
        conn.close()
        print("Conexão encerrada.")

def start_server(host='192.168.43.162', port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servidor escutando em {host}:{port}")

        while True:
            try:
                conn, addr = s.accept()
                handle_connection(conn, addr)
            except KeyboardInterrupt:
                print("Servidor encerrado manualmente (Ctrl+C).")
                break
            except Exception as e:
                print(f"Erro no tratamento da conexão: {e}")

if __name__ == "__main__":
    start_server()
