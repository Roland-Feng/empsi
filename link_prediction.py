import numpy as np
import igraph as ig
import random
from tqdm import tqdm
import copy

def get_p_matrix(G, edge_tuple_s):

    N = G.vcount()

    G_delta = copy.deepcopy(G)
    G_delta.delete_edges()
    G_delta.es['weight'] = 0

    for e in edge_tuple_s:
        G_delta.add_edge(e[0],e[1])
        G_delta[e[0],e[1]] = e[2]

    M = G.get_adjacency(attribute='weight')

    la, ve = np.linalg.eig(list(M))
    la = la.real
    ve = ve.real
    A_delta = np.array(list(G_delta.get_adjacency(attribute = 'weight')))

    A_temp = np.zeros((N, N))

    for i in range(0,N):
        l_delta_k = np.dot(np.dot(ve[:,i], A_delta), ve[:,i])/np.dot(ve[:,i].T, ve[:,i])
        #print(l_delta_k, la[i])
        A_temp += (la[i].real + l_delta_k.real)*np.matmul(ve[:,i].reshape(N,1), ve[:,i].reshape(1,N))

    return A_temp




def spm(G,spm_pro):

    edge_tuple = []
    for e in G.es:
        edge_tuple.append((e.tuple[0],e.tuple[1],e['weight']))
    
    
    edge_tuple_s = random.sample(edge_tuple, np.int(spm_pro*G.ecount()))
    G.delete_edges(edge_tuple_s)

    A_p = get_p_matrix(G, edge_tuple_s)

    for e in edge_tuple_s:
        G.add_edge(e[0],e[1])
        G[e[0],e[1]] = e[2]

    return A_p

    
    




def spm_matrix(G, spm_t, spm_pro):

    m_temp = np.zeros((G.vcount(), G.vcount()))
    for i in tqdm(range(0,spm_t)):
        m_temp += spm(G, spm_pro)

    return m_temp/spm_t


##--------------------------------------------------------------
def top_l(ary, n):
    """Returns the n largest indices from a numpy array."""
    flat = ary.flatten()
    indices = np.argpartition(flat, -n)[-n:]
    indices = indices[np.argsort(-flat[indices])]
    return np.unravel_index(indices, ary.shape)

##---------------------------------------------------------------


def WRA(G):
    neighbors_dict = {}
    strength_dict = {}
    node_list = []
    for v in G.vs():
        neighbors_dict[v.index] = G.neighbors(v)
        strength_dict[v.index] = G.strength(v)
        node_list.append(v.index)

    A_temp = np.zeros((G.vcount(),G.vcount()))

    for x in node_list:
        for y in node_list:
            temp = 0
            for z in neighbors_dict[y]:
                if z in neighbors_dict[x]:
                    if strength_dict[z] != 0:
                        temp += (G[x,z] + G[y,z])/strength_dict[z]

                    if strength_dict[z] == 0:
                        temp += 0

            A_temp[x,y] = temp
            A_temp[y,x] = temp

    return A_temp

##===========================================================

def WAA(G):
    neighbors_dict = {}
    strength_dict = {}
    node_list = []
    for v in G.vs():
        neighbors_dict[v.index] = G.neighbors(v)
        strength_dict[v.index] = G.strength(v)
        node_list.append(v.index)

    A_temp = np.zeros((G.vcount(),G.vcount()))

    for x in node_list:
        for y in node_list:
            temp = 0
            for z in neighbors_dict[y]:
                if z in neighbors_dict[x]:
                    if strength_dict[z] != 0:
                        temp += (G[x,z] + G[y,z])/np.log(1 + strength_dict[z])

                    if strength_dict[z] == 0:
                        temp += 0

            A_temp[x,y] = temp
            A_temp[y,x] = temp

    return A_temp


##=============================================================
def WCN(G):
    neighbors_dict = {}
    node_list = []
    for v in G.vs():
        neighbors_dict[v.index] = G.neighbors(v)
        node_list.append(v.index)

    A_temp = np.zeros((G.vcount(),G.vcount()))

    for x in node_list:
        for y in node_list:
            temp = 0
            for z in neighbors_dict[y]:
                if z in neighbors_dict[x]:
                    temp += G[x,z] + G[y,z]

            A_temp[x,y] = temp
            A_temp[y,x] = temp

    return A_temp


##============================================================== 
def node_2_node(G1,G2):
    n2n = {}
    for i in range(0,G1.vcount()):
        for j in range(0, G2.vcount()):
            if tuple(G1.vs.find(i)['name']) == tuple(G2.vs.find(j)['name']):
                n2n[i] = j
                
    return n2n


    