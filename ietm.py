import pydivert
from scapy.layers.inet import TCP, IP
from scapy.all import *


load_layer("http")


class IETM:
	def __init__(self, rule: str) -> None:
		self.w = pydivert.WinDivert(rule)
		self.w.open()


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
				packet = IP(bytes(self.w.recv().raw)) # PyDivert packet to Scapy
				self.packet_handler(packet)
			except KeyboardInterrupt:
				print("[*] Stoped.")
				break


	def __del__(self) -> None:
		if hasattr(self, "w"):
			self.w.close()