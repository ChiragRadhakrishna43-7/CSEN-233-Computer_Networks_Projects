# Router simulator in a network
# To exercise routing algorithms
#
# Sin-Yaw Wang <swang24@scu.edu
#
import sys
import os
import json
import router

# a nework emulator
class netEmulator:
	def __init__(self):
		pass

	# load the topology from a JSON file
	# return None if fail
	def rtInit(self, fname):
		try:
			f=open(fname, 'r')
		except:
			print('failed to open {}'.format(fname))
			return None

		try:
			net = json.load(f)
		except:
			print('{} not in JSON format'.format(fname))
			return None

		f.close()
		self.routers=[]

		# process the JSON file
		# instantiate a "Router" for each one in the JSON file
		# add links per topology
		# after getting all the routers, initialize the forwarding table
		for rtr in net['Network']:
			r=router.Router(rtr['Router'])
			r.network = self;
			for l,c in rtr['Links'].items():
				r.addLink(l, c)
			self.routers.append(r)
	
	def __str__(self):
		return self.__repr__()

	# friendly output of router info in JSON syntax
	def __repr__(self):
		str = '{"Network": ['
		for r in net.routers[:-1]:
			str += '{},\n'.format(r)
		for r in net.routers[-1:]:
			str += '{}]'.format(r)
		str += '}'
		return str;

# test for network initialization
if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print('need topology file')

	net = netEmulator()
	net.rtInit(sys.argv[1])
	print(net)
