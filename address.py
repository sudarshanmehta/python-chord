from settings import SIZE

# Helper function to determine if a key falls within a range
def inrange(c, a, b):
	# is c in [a,b)?, if a == b then it assumes a full circle
	# on the DHT, so it returns True.
	a = a % SIZE
	b = b % SIZE
	c = c % SIZE
	if a < b:
		return a <= c and c < b
	return a <= c or c < b

class Address:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = int(port)

    def __hash__(self):
        return hash("%s:%s" % (self.ip, self.port)) % SIZE

    def __lt__(self, other):
        return (self.ip, self.port) < (other.ip, other.port)

    def __eq__(self, other):
        return (self.ip, self.port) == (other.ip, other.port)

    def __str__(self):
        return "[\"%s\", %s]" % (self.ip, self.port)


