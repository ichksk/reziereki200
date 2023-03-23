#同一セグメント内の2つのデバイスで
#TCP通信を使ってファイルを送受信する
#モバイルも対応させる
#同一セグメント外=>TCPトンネリング

import socket
from threading import Thread


class Peer:
    def __init__(self):
        self.my_ip = self.get_ip()
        self.my_port = 49000
        self.buff = 4096


    def start(self, opponent):
        self.opponent_ip, self.opponent_port = opponent
        thread_client = Thread(target=self.client)
        thread_client.start()

        thread_server = Thread(target=self.server)
        thread_server.start()

    def client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            while True:
                if input("if ready, type OK:") == "OK":break
            s.connect((self.opponent_ip, self.opponent_port))

            while True:
                msg = input("")
                s.sendall(msg.encode("utf-8"))

    def server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.my_ip, self.my_port))
            s.listen(5)
            connection, address = s.accept()
            while True:
                data = connection.recv(self.buff)
                print(data.decode("utf-8"))

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
        s.close()
        return IP

if __name__ == "__main__":
    # ip = input("ip>>>")
    ip = "192.168.1.36"
    port = 49000
    peer = Peer()
    peer.start((ip, port))