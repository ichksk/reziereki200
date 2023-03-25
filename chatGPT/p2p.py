import socket
import threading

# ホストとポートの設定
HOST = "127.0.0.1"
PORT = 8080

# 接続する相手のIPアドレスとポート番号
OTHER_HOST = "127.0.0.1" # 相手のIPアドレス
OTHER_PORT = 8081 # 相手のポート番号

# サーバーを開始する
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

# クライアントからの接続を待つ
print("Waiting for connection...")

# 相手のサーバーに接続する
peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peer.connect((OTHER_HOST, OTHER_PORT))
print("Connected to peer:", (OTHER_HOST, OTHER_PORT))

# クライアントからの接続を受け入れる
client, address = server.accept()
print("Connected to client:", address)

# メッセージを送信する関数
def send_message(sock):
    while True:
        message = input()
        sock.send(message.encode())

# メッセージを受信する関数
def receive_message(sock):
    while True:
        message = sock.recv(1024)
        print("Received message:", message.decode())

# 送受信用のスレッドを作成する
send_thread = threading.Thread(target=send_message, args=[peer])
receive_thread = threading.Thread(target=receive_message, args=[client])

# スレッドを開始する
send_thread.start()
receive_thread.start()