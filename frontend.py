from flask import Flask,request,render_template
import socket
from xor_cipher import xor_encrypt_decrypt

app=Flask(__name__)

SERVER_HOST='127.0.0.1'
SERVER_PORT=5002

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send',methods=['POST'])
def send_msg():
    message=request.form['message']
    key=request.form['key']

    encrypted_msg=xor_encrypt_decrypt(message,key)
    payload=f"{encrypted_msg}|||{key}"

    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((SERVER_HOST,SERVER_PORT))
    client.send(payload.encode())

    encrypted_ack=client.recv(1024).decode()
    ack=xor_encrypt_decrypt(encrypted_ack,key)

    client.close()

    return f"<h3>message:{message} <br> server acknowledgement:{ack}</h3>"

if __name__=='__main__':
    app.run(debug=True)
