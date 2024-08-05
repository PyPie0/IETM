import sys
import utils
import ietm


if __name__ == "__main__":
	# WireShark rule: ip.src == 192.168.0.102 and ip.dst == 192.168.0.102
	if not utils.is_admin():
		print("[*] Administrator privilegies required!")
		sys.exit(code=1)
	i = ietm.IETM("ip.DstAddr == 192.168.0.102 and tcp.DstPort == 5000")
	i.run()

