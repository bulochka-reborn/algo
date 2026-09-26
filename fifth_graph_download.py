import osmnx as ox

city_name = "Скопье, Македония"
G = ox.graph_from_place(city_name, network_type="drive")

ox.save_graphml(G, filepath="skopie_network.graphml")