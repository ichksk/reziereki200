import os
import socket
import threading
import time
import sys

def my_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('10.255.255.255', 1))
    IP = s.getsockname()[0]
    s.close()
    return IP

def subnet(ip:str) -> list:
    return [ip.replace(ip.split(".")[-1], str(i)) for i in range(1, 255)]

def close(is_running):
    try:
        while is_running():
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit()

class Match:
    def __init__(self):
        self.my_ip = my_ip()
        self.peer_ip = None
        self.match_port = 19000
        self.running = True
        self.event = threading.Event()

    def neighbors(self, my_ip:str, port) -> list:
        func_name = "scan_lan"
        def scan_lan(ip_address, port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                if s.connect_ex((ip_address, port)) == 0:
                    __neighbors.append({"name":socket.gethostbyaddr(ip_address)[0], "ip":ip_address})
                    s.close()

        __neighbors = []
        for ip in subnet(my_ip):
            if ip != my_ip:
                threading.Thread(target=scan_lan, args=(ip, port), name=func_name).start()

        for thread in threading.enumerate():
            if thread.name == func_name:
                thread.join()
        return __neighbors


    def publish(self):
        self.match_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.match_socket.bind((self.my_ip, self.match_port))
        self.match_socket.listen()
        while True:
            try:
                self.match_socket.accept()
            except OSError:
                break

        self.running = False

    def crawl(self):
        while True:
            print("Finding Neighbors...")
            n_list = self.neighbors(self.my_ip, self.match_port)
            if len(n_list) != 0:
                print("Neighbors around is :", *[n["name"] for n in n_list])
                if len(n_list) == 1:
                    idx = 0
                else:
                    idx = input("Which Neighbor? :")
                    try:
                        idx = int(idx)
                    except:
                        print(f"{idx} should be an integer")
                        continue
                if 0 <= idx <= len(n_list)-1 :
                    self.peer = n_list[idx]
                    self.peer_ip = n_list[idx]["ip"]
                    self.peer_name = n_list[idx]["name"]
                    self.match_socket.close()
                    break
        self.running = False

    def match(self):
        thread_publish = threading.Thread(target=self.publish, daemon=True)
        thread_crawl = threading.Thread(target=self.crawl, daemon=True)
        thread_publish.start()
        thread_crawl.start()
        close(lambda:self.running)

        return self.peer_ip


class Peer:
    def __init__(self):
        self.my_ip = my_ip()
        self.peer_ip = None
        self.fname_port = 29001
        self.port = 29000
        self.buff = 4096
        self.running = True
        self.is_connected = False

    def start(self, peer_ip):
        self.peer_ip = peer_ip
        client_thread = threading.Thread(target=self.client, daemon=True)
        server_thread = threading.Thread(target=self.server, daemon=True)
        client_thread.start()
        server_thread.start()
        close(lambda:self.running)

    def client(self):
        with  socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            while self.running:
                result = s.connect_ex((self.peer_ip, self.port))
                if result == 0:
                    if not self.is_connected:
                        print("CLIENT:接続", (self.peer_ip, self.port))
                        self.is_connected = True
                    break
            while self.running:
                msg = input(">>>")
                if msg == "quit":
                    print("QUIT")
                    s.sendall(msg.encode("utf-8"))
                    self.running = False
                else:
                    self.send(msg, s)


    def send(self, msg:str, s:socket.socket):
        if os.path.isfile(msg):
            with open(msg, "rb") as f:
                while True:
                    chunk = f.read(self.buff)
                    s.sendall(chunk)
                    if len(chunk) == 0:
                        print("Read Done")
                        break
        else:
            print(f"Could not find such file : {msg}")

    def server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.my_ip, self.port))
            s.listen(1)
            conn, addr = s.accept()
            if not self.is_connected:
                print(f"SERVER:接続：{addr}")
                self.is_connected = True
            while self.running:
                try:
                    msg = conn.recv(self.buff)
                    if msg == b"quit":
                        print("QUIT")
                        self.running = False
                    else:
                        self.write(msg)
                except ConnectionResetError:
                    print("CONNECTION RESET ERROR")
                    self.running = False

    def write(self, msg:bytes):
        with open("test", "ab") as f:
            f.write(msg)
        if len(msg) != self.buff:
            print("Write Done")


def main():
    os.chdir(os.path.dirname(__file__))
    m = Match()
    p = Peer()
    m.match()
    p.start(m.peer_ip)

if __name__ == "__main__":
    main()