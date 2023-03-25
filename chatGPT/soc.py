import socket
from threading import Thread

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('10.255.255.255', 1))
    IP = s.getsockname()[0]
    s.close()
    return IP

def scan_network(ip_address, port):
    """指定されたIPアドレスの指定されたポートに接続できるかどうかを調べる関数"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip_address, port))
        print(f"TCP connection established with {ip_address}")
        s.close()
        return True
    except:
        return False

availables = []
def process(ip_address):
    if scan_network(ip_address, 80):
        availables.append(ip_address)
        print(f"{ip_address} is available for TCP connection on port 80")


def main():
    # ローカルIPアドレスの取得
    local_ip = get_ip()
    print(f"Scanning network for TCP ports on {local_ip}")

    # IPアドレスの最後のセグメントを変えて、ポート番号80に接続を試みる
    threads = []
    for i in range(1, 255):
        ip_address = f"{local_ip.split('.')[0]}.{local_ip.split('.')[1]}.{local_ip.split('.')[2]}.{i}"
        thread = Thread(target=process, args=(ip_address,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(availables)



if __name__ == '__main__':
    main()