import sys
import utils
import ietm


if __name__ == "__main__":
	# WireShark rule: ip.src == 127.0.0.1 and ip.dst == 127.0.0.1
	if not utils.is_admin():
		print("[*] Administrator privilegies required!")
		sys.exit(code=1)
	i = ietm.IETM("ip.DstAddr == 127.0.0.1 and tcp.DstPort == 5000")
	i.run()

