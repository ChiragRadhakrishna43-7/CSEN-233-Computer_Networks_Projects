# Router simulator in a network
# To exercise routing algorithms
#
# Sin-Yaw Wang <swang24@scu.edu
#

# "links": routers directly connected, with a link cost
# "network" is the network that has all the routers in the universe
import json

class Router:
	# initialize per router variables
	def __init__(self, nm):
		self.name = nm	# name of the router
		self.links = {}	# a dictionary

	def addLink(self, l, c):
		self.links[l] =  c

	def __str__(self):
		return self.__repr__()

	# friendly output of router info in JSON syntax
	def __repr__(self):
		str = '{{"Router": "{}", '.format(self.name)
		if len(self.links) > 0:
			str += '"Links": {'
			str += json.dumps(self.links)
			str += '}'
		str += '}'
		return str
