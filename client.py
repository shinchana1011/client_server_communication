import socket
from xor_cipher import xor_encrypt_decrypt

SERVER_HOST='127.0.0.1'
SERVER_PORT=5002

def send_msg():
    msg=input("enter your message:")
    key=input("enter encryption key:")

    encrypted_msg=xor_encrypt_decrypt(msg,key)

    payload=f"{encrypted_msg}|||{key}"

    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((SERVER_HOST,SERVER_PORT))
    client.send(payload.encode())

    encrypted_ack=client.recv(1024).decode()
    ack=xor_encrypt_decrypt(encrypted_ack,key)
    print(f"Server acknowledgement:{ack}")

    client.close()

if __name__=="__main__":
    send_msg()