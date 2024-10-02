import socket
import numpy as np
import cv2  # Para manipulação de imagem, se não tiver, instale via 'pip install opencv-python'

def face_detection(image):
    # Conversão de imagem de bytes para formato que o OpenCV entende
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detecta as faces e retorna as coordenadas
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    return faces

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
        faces = face_detection(img_np)

        if len(faces) > 0:
            # Formatar as coordenadas das faces em uma string
            face_data = f"{len(faces)} "  # Número de rostos detectados
            for (x, y, w, h) in faces:
                face_data += f"{x},{y},{w},{h} "  # Adicionar as coordenadas
            face_data = face_data.strip() + '\n'  # Adiciona '\n' para a detecção via Serial.readStringUntil('\n')
            print(f"Enviando coordenadas: {face_data}")
        else:
            # Nenhum rosto detectado, envia "0\n"
            face_data = "0\n"
            print("Nenhum rosto detectado.")

        # Enviando as coordenadas para o ESP32 como string
        conn.sendall(face_data.encode())
        print("Coordenadas dos rostos enviadas com sucesso!")
        
    except Exception as e:
        print(f"Erro durante a conexão: {e}")
    except KeyboardInterrupt:
        print("Servidor encerrado manualmente (Ctrl+C).")
        return
    finally:
        conn.close()
        print("Conexão encerrada.")

def start_server(host='192.168.43.162', port=8000):
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
