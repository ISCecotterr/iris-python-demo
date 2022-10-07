# This code retrieves the network neighbours global generated by:
# src > ObjectScript > Embedded > Networks.cls with the CreateNetwork() classmethod

import irisnative
import networkx as nx
import matplotlib.pyplot as plt
import json

# Make connection to IRIS; parameters are (hostname, port, namespace, username, password)
connection = irisnative.createConnection("localhost", 1972, "USER", "SuperUser", "SYS")
print("\nConnection successful!")


# Create an IRIS object
myIris = irisnative.createIris(connection)


# Get the desired global
nodeGlobal = myIris.get("^nodeGlobal")
print("\nProceeding to construct graph...\n")


# Retrieving the neighbour list for each node:
i = 0
key = ""
neighbour_list_all = []
while key != None:
    neighbour_list = myIris.get(f"^nodeGlobal({i})")
    # Remember to convert back from JSON to a Python list, or else our append won't work as intended
    neighbour_list_all.append(json.loads(neighbour_list))
    # Using the nextSubscript() method to traverse the sibling nodes of ^nodeGlobal(0) in ascending order (works like $order in ObjectScript)
    key = myIris.nextSubscript(False,f"^nodeGlobal({i})") # if key == None, there are no more sibling nodes
    print("Node " + str(i) + " has neighbours: " + str(neighbour_list))
    i += 1
print("Found " + str(i) + " nodes!")

print("\n" + str(neighbour_list_all))
# Recreating the network:
# Thanks to Yuhang Xia for the following code and expertise on networkx

network = nx.Graph()

for node in range(len(neighbour_list_all)):
    network.add_edges_from(zip([node]*len(neighbour_list_all[node]),neighbour_list_all[node]))

nx.draw(network, with_labels = True)


# Save the network as a .png
plt.savefig("/irisdev/app/Network.png", dpi = 300)

print("\nGraph image saved to irisdev/app/Network.png")