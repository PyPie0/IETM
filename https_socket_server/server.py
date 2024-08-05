import socket
from scapy.layers.inet import TCP, IP
from scapy.all import *




HOST = "192.168.0.102"
PORT = 5000

class SocketServer:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        self.s.bind((HOST, PORT))
        self.s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        self.s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    def packet_handler(self, ip_layer: IP) -> None:
        if not ip_layer.haslayer(TCP):
            return
        ip_layer.show()
        tcp_layer = ip_layer.getlayer(TCP)
        if tcp_layer.flags == "S":
            response = (
                    IP(src=ip_layer.dst, dst=ip_layer.src) / 
                    TCP(sport=tcp_layer.dport, dport=tcp_layer.sport, seq=100, ack=tcp_layer.seq+1, flags="SA")
                ) 
            send(response)
            return
        if b"GET" in bytes(tcp_layer.payload):
            payload = b"HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body><h1>IETM response</h1></body></html>"
            response = (
                    IP(src=ip_layer.dst, dst=ip_layer.src) / 
                    TCP(sport=tcp_layer.dport, dport=tcp_layer.sport, seq=tcp_layer.ack, ack=tcp_layer.seq+len(bytes(tcp_layer)), flags="PAF") /
                    payload
                ) 
            send(response)
            return
    
    def run(self) -> None:
        print("[*] Started.")
        for i in range(300):
            try:
                packet = IP(self.s.recvfrom(65565)[0])
                self.packet_handler(packet)
            except KeyboardInterrupt:
                print("[*] Stoped.")
                break


if __name__ == "__main__":
    s = SocketServer()
    s.run()