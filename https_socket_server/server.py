import socket


#route add 192.168.0.102 mask 255.255.255.255 192.168.0.1 metric 1


class SocketServer:
    def __init__(self, host: str, port: int) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))
    
    def run(self) -> None:
        self.s.listen()
        conn, addr = self.s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                print(data)


if __name__ == "__main__":
    s = SocketServer("127.0.0.1", 5000)
    s.run()