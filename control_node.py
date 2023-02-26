import igraph as ig
import networkx as nx

######################################################
#寻找 driver nodes
def find_control_node(G1_in):
    
    edge_tuple = []
    for o1 in G1_in.vs():
        for o2 in G1_in.vs():
            if o1!=o2 and G1_in.are_connected(o1,o2):
                edge_tuple.append((o1['name'] + '+', o2['name'] + '-'))


    G_bipartite = ig.Graph.TupleList(edge_tuple)
    for o in G_bipartite.vs():
        if o['name'][-1] == '+':
            o['type'] = 0

        else:
            o['type'] = 1



    isolated_nodes = []
    for o in G1_in.vs():
        temp = o['name'] + '+'
        if temp not in G_bipartite.vs()['name']:
            isolated_nodes.append(o['name'])


    mg = G_bipartite.maximum_bipartite_matching()


    control_nodes = []
    for i in range(0,len(mg.matching)):
        if mg.matching[i] < 0:
            a = G_bipartite.vs(i)['name'][0][0:-1]
            #print(a)
            if a not in control_nodes and G_bipartite.vs(i)['name'][0][-1] == '-':
                control_nodes.append(a)

    return control_nodes, isolated_nodes




######################################################
#把网络转化成 networkx 网络
def get_networkx_graph(G1_in):
    G_edgelist_index = G1_in.get_edgelist()

    G_edgelist_name = []

    for ep in G_edgelist_index:
        G_edgelist_name.append((G1_in.vs()[ep[0]]['name'],G1_in.vs()[ep[1]]['name']))
    
    G_nx = nx.from_edgelist(G_edgelist_name)

    return G_nx
    