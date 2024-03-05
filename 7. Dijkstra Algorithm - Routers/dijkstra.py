# CSEN 233 Homework 7:
# Chirag Radhakrishna (cradhakrishna@scu.edu) SCU ID: 07700009612
# Dijkstra Algorithm
# ---------------------------------------------------------------
from netemulate import netEmulator
from queue import PriorityQueue
from router import Router
import logging
import random
import sys


logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s -%(message)s', filename = "csen233hw7RadhakrishnaChirag.logs", filemode = "a")
logger = logging.getLogger(__name__)

class Dijkstra(netEmulator):
	def __init__(self):
		super().__init__()

	# Homework #5
	def dijkstra(self, r1, r2):
                path = []
                logging.info("Obtaining the names of the two routers.")
                pair = [r for r in self.routers if r.name == r1 or r.name == r2]
                if len(pair) != 2:
                        logging.error(f"Invalid pair of routers:{pair}")
                        return None
                src, dest = pair
                dist = {router.name: float('inf') for router in self.routers}
                dist[src.name] = 0
                pr_queue = PriorityQueue()
                pr_queue.put((0, src.name))
                prev = {router.name: None for router in self.routers}
                while not pr_queue.empty():
                        curr_dist, curr_node = pr_queue.get()
                        if curr_node == dest.name:
                                logging.info("Shortest path found.")
                                while prev[curr_node]:
                                        path.append(curr_node)
                                        curr_node = prev[curr_node]
                                path.append(src.name)
                                path.reverse() if path[-1] == r1 else None
                        for router in self.routers:
                                if router.name == curr_node:
                                        for neighbor_node, weight in router.links.items():
                                                distance = curr_dist + weight
                                                if distance < dist[neighbor_node]:
                                                        dist[neighbor_node] = distance
                                                        prev[neighbor_node] = curr_node
                                                        pr_queue.put((distance, neighbor_node))
                t_cost = dist[dest.name]
                return path, t_cost

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print('need topology file')
	if len(sys.argv) <= 3:
		print('need node names')

	net=Dijkstra()
	logger.info(f"Loading json file {sys.argv[1]} for assistance in determining path between routers.")
	print('loading {}'.format(sys.argv[1]))
	net.rtInit(sys.argv[1])

	# this is where you test your homework
	# assign two routers and find their shortest path
	# than print out the path
	logger.info(f"Computing shortest path between routers {sys.argv[2]} and {sys.argv[3]} using Dijkstra algorithm.")
	shortest, cost = net.dijkstra(sys.argv[2], sys.argv[3])
	logger.info(f"Shortest path between {sys.argv[2]} and {sys.argv[3]} is calculated to be {shortest}.")
	logger.info(f"The cost of this path is found to be {cost}.")
	print(f"Shortest path between {sys.argv[2]} and {sys.argv[3]} is calculated to be {shortest}.")
