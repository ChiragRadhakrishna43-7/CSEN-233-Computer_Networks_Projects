# CSEN 233 Extra Credit 4
#
# Student Details:
# Chirag Radhakrishna (cradhakrishna@scu.edu) SCU ID: 07700009612
#
# Minimum Spanning Tree Implementation for given network topology (KRUSKAL Algorithm).
# ------------------------------------------------------------------------------------

import sys
import random
import logging
from router import Router
from netemulate import netEmulator

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s -%(message)s', filename = "csen233ec4RadhakrishnaChirag.logs", filemode = "a")
logger = logging.getLogger(__name__)

class Kruskal_MST(netEmulator):
    def __init__(self):
        super().__init__()

    def Kruskal_algo(self): # This function computes the Minimum Spanning Tree.
        start = generate_router()
        logger.info(f'The router selected at random is: {start}.')
        minimum_spanning_tree = [] #list of edges constituting the Minimum Spanning Tree.
        edge_set = []
        for edge in self.routers:
            for neighbours, cost in edge.links.items():
                if(neighbours, edge.name, cost) not in edge_set:
                    edge_set.append((edge.name, neighbours, cost)) #obtaining all edges between the various routers.
        """
        Sorting the edges between various routers in ascending order.
        This is the first step of the Kruskal Algorithm.
        """
        edge_set = sorted(edge_set, key = lambda x: x[2])

        parent = {}
        for router in self.routers:
            parent[router.name] = router.name
        for each_edge in edge_set:
            r1, r2, edge_weight = each_edge
            root1 = r1
            while parent[root1] != root1:
                root1 = parent[root1]
            root2 = r2
            while parent[root2] != root2:
                root2 = parent[root2]
            if root1 != root2:
                minimum_spanning_tree.append((r1, r2, edge_weight))
                parent[root1] = root2
        return minimum_spanning_tree
            
def generate_router(): #Generates a random router from the 20 routers available in net.json.
    number = random.randint(1, 20)
    router = ''
    if number < 10:
        router = 'R0' + str(number)
    else:
        router = 'R' + str(number)
    return router

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Need topology file.')
    net = Kruskal_MST()
    logger.info(f"Loading the topology file: {sys.argv[1]}.")
    net.rtInit(sys.argv[1])
    logger.info("Implementing Kruskal algorithm to find minimum spanning tree.")
    mst = net.Kruskal_algo()
    logger.info("Obtained the minimum spanning tree.")
    for each_edge in mst:
        logger.info(f"{each_edge[0]} -----> {each_edge[1]}: {each_edge[2]}.")
    
        
    

        

