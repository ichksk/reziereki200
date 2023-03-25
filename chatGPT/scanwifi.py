from scapy.all import ARP, Ether, srp

# ネットワーク範囲を指定
target_ip = "192.168.1.0/24"

# ARPパケットを作成
arp = ARP(pdst=target_ip)

# Etherフレームを作成
ether = Ether(dst="ff:ff:ff:ff:ff:ff")

# ARPリクエストとEtherフレームを組み合わせて送信
packet = ether/arp
result = srp(packet, timeout=3, verbose=0)[0]

# スキャン結果を表示
clients = []
for sent, received in result:
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})

print("Scanned devices:")
print("IP" + " "*18 + "MAC")
for client in clients:
    print("{:16}    {}".format(client['ip'], client['mac']))