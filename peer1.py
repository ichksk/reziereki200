#同一セグメント内の2つのデバイスで
#TCP通信を使ってファイルを送受信する
#モバイルも対応させる
#同一セグメント外=>TCPトンネリング

import os
from peer import Peer

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    my_port = 49000
    peer = Peer(my_port)
    peer.start(("192.168.1.18", 49001))