import networkx as nx 

G = nx.barabasi_albert_graph(n=1469, m=1 )
nx.write_gml(G, 'scalefree_gen.gml')