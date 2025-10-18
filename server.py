import socket
import threading
from datetime import datetime
from xor_cipher import xor_encrypt_decrypt

HOST='0.0.0.0'
PORT=5002

def handle_client(client_socket, addr):
    try:
        print(f"{datetime.now()} connection from {addr}")

        # Receive full payload
        payload = client_socket.recv(1024).decode()

        # Split message and key
        if '|||' in payload:
            encrypted_msg, key = payload.split('|||', 1)
        else:
            print(f"{datetime.now()} Invalid payload from {addr}")
            client_socket.close()
            return

        # Decrypt message
        msg = xor_encrypt_decrypt(encrypted_msg, key)
        print(f"{datetime.now()} received from {addr}: {msg}")

        # Send acknowledgment
        ack = f"Message received at {datetime.now()}"
        encrypted_ack = xor_encrypt_decrypt(ack, key)
        client_socket.send(encrypted_ack.encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


def start_server():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((HOST,PORT))
    server.listen()
    print(f"[*] server listening on {HOST}:{PORT}")

    while True:
        client_sock,addr=server.accept()
        client_thread=threading.Thread(target=handle_client,args=(client_sock,addr))
        client_thread.start()

if __name__=="__main__":
    start_server()