import os
import socket
from threading import Thread

class Peer:
    def __init__(self):
        self.my_ip = self.get_ip()
        self.my_port = 29000
        self.buff = 4096
        self.mode = "chat"
        self.running = True

    def start(self, opponent):
        self.opponent_ip, self.opponent_port = opponent
        thread_client = Thread(target=self.client)
        thread_server = Thread(target=self.server)
        thread_client.start()
        thread_server.start()
        thread_client.join()
        thread_server.join()

    def client(self):
        with  socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            while True:
                result = s.connect_ex((self.opponent_ip, self.opponent_port))
                if result == 0:
                    print("接続成功!")
                    break
                print("接続中、、、")

            print(f"モード：{self.mode}")
            while self.running:
                msg = input(">>>")
                if msg == "quit":
                    self.running = False
                    s.sendall(msg.encode("utf-8"))
                elif msg in  ["chat", "file"]:
                    self.change_mode(msg)
                    s.sendall(msg.encode("utf-8"))
                else:
                    if self.mode == "file":
                        #send file
                        if os.path.isfile(msg):
                            with open(msg, "rb") as f:
                                while True:
                                    chunk = f.read(self.buff)
                                    s.sendall(chunk)
                                    if len(chunk) == 0:
                                        print("Read Done")
                                        break
                        else:
                            print(f"{msg}というファイルは無い")
                    elif self.mode == "chat":
                        #send text
                        s.sendall(msg.encode("utf-8"))


    def server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.my_ip, self.my_port))
            s.listen(1)
            connection, address = s.accept()
            while self.running:
                msg = connection.recv(self.buff)
                if msg == b"quit":
                    self.running = False
                elif msg in [b"chat", b"file"]:
                    self.change_mode(msg.decode("utf-8"))
                else:
                    if self.mode == "chat":
                        print(msg.decode("utf-8"))
                    elif self.mode == "file":
                        with open("test", "ab") as f:
                            f.write(msg)
                        if len(msg) != self.buff:
                            print("Write Done")

    def change_mode(self, mode:str):
        print(f"MODE:{self.mode} -> {mode}")
        self.mode = mode

    def get_ip(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect(("10.255.255.255", 1))
            IP = s.getsockname()[0]
        return IP

    def find_peers(self):
        def scan_lan(ip_address, port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    s.connect((ip_address, port))
                peers.append(ip_address)
            except:
                pass

        threads = []
        peers = []
        for i in range(1, 255):
            ip_address = f"{self.my_ip.split('.')[0]}.{self.my_ip.split('.')[1]}.{self.my_ip.split('.')[2]}.{i}"
            thread = Thread(target=scan_lan, args=(ip_address, self.my_port))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return peers

if __name__ == "__main__":
    p = Peer()
    thread = Thread(target=p.server)
    thread.start()