import socket
import json

def receive_data(host='192.168.43.162', port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        try:
            while True:
                data = s.recv(1024)
                if not data:
                    break
                data_dict_array = json.loads(data.decode('utf-8'))
                print(data_dict_array, "\n")
                print("Data received from the server.")
        except KeyboardInterrupt:
            print("Client shutdown due to keyboard interrupt (Ctrl+C).")
        except Exception as e:
            print(f"An error occurred during data reception: {e}")
            

if __name__ == "__main__":
    receive_data()
