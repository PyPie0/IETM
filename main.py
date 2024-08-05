import sys
import utils

import ietm



if __name__ == "__main__":
	if not utils.is_admin():
		print("[*] Administrator privilegies required!")
		sys.exit(code=1)
	i = ietm.IETM("ip.DstAddr == 127.0.0.1 and tcp.DstPort == 5000")
	i.run()

