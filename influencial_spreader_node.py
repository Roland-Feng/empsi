import igraph as ig
from pickle_file import load_obj,save_obj
from tqdm import tqdm
import os
from datetime import datetime
import numpy as np
import networkx as nx
import igraph as ig


def ci_node(G, neighbor_order):

    ci_values = []
    ci_names = []

    isolated_nodes = []

    for o in G.vs():
        o_hoop_neighbor = G.neighborhood(o, order = neighbor_order, mindist = neighbor_order)
        temp = 0
        for ot in o_hoop_neighbor:
            temp += (G.degree(o) - 1) * (G.degree(ot) - 1)
            
        ci_values.append(temp)
        ci_names.append(o['name'])

        if G.degree(o) == 0:
            isolated_nodes.append(o['name'])


    ci_values, ci_names = zip(*sorted(zip(ci_values,ci_names), reverse = True))
    return [ci_values, ci_names], isolated_nodes





def degree_rank(G, nd):
    
    degree_list = []
    name_list = []
    
    for o in G.vs():
        degree_list.append(G.degree(o))
        name_list.append(o['name'])

    degree_list, name_list = zip(*sorted(zip(degree_list,name_list), reverse = True))

    return name_list.index(nd)


def weighted_ci(G, ndi, n_order):
    S = G.strength(ndi, weights = 'weight')
    temp_path = []
    neighbor_temp = G.neighborhood(ndi, order = 1, mindist = 1)
    for n in neighbor_temp:
        temp_path.append([ndi, n])

    for i in range(1, n_order):
        temp_path_new = []
        for p in temp_path:
            end_node = p[-1]
            non_backtracking_node = p[-2]
            neighbor_temp = G.neighborhood(end_node, order = 1, mindist = 1)
            for n in neighbor_temp:
                if n != non_backtracking_node:
                    temp_path_new.append(p + [n])

        temp_path = temp_path_new


    temp_ci = 0
    for p in temp_path:
        K = G.degree(p[-1]) - 1
        temp = S - G[ndi, p[1]]
        for i in range(0,len(p) - 1):
            temp  = temp * G[p[i], p[i + 1]]

        temp_ci += temp * K


    return temp_ci









def weighted_ci_node(G, n_order):
    weighted_ci_values = []
    weighted_ci_names = []

    weighted_isolated_nodes = []

    for o in G.vs():
        
        temp = weighted_ci(G, o.index, n_order)
            
        weighted_ci_values.append(temp)
        weighted_ci_names.append(o['name'])

        if G.degree(o) == 0:
            weighted_isolated_nodes.append(o['name'])


    weighted_ci_values, weighted_ci_names = zip(*sorted(zip(weighted_ci_values,weighted_ci_names), reverse = True))
    return [weighted_ci_values, weighted_ci_names], weighted_isolated_nodes









    
def unnormalized_osv_rca_weighted_ci (thre = 0, fd = 'db_25_0_text', h_order = 1):

    save_time = '2020may'
    city_codes = load_obj('occupations_city/' + save_time +'/city_codes_'+ save_time)
    city_names = load_obj('occupations_city/' + save_time +'/city_names_'+ save_time)
    city_occupations = load_obj('occupations_city/' + save_time +'/city_occupations_'+ save_time)
    city_occupations_names = load_obj('occupations_city/' + save_time +'/city_occupations_names_'+ save_time)
    city_emp = load_obj('occupations_city/' + save_time +'/city_emp_'+ save_time)

    #
    fd_osv_6digit = load_obj('osv_6digit/osv_6digit_'+fd)
    occupations_6digit = load_obj('osv_6digit/occupations_6digit_'+fd)
    occupations_6digit_names = load_obj('osv_6digit/occupations_6digit_names_'+fd)

    G = load_obj('rca_6digit_graph/rca_graph_6digit_'+fd)
    edge_sq = G.es.select(weight_gt=thre)
    G_in = G.subgraph_edges(edge_sq, delete_vertices = False)
    #G_in.es["weight"] = 1
    print(G_in.vcount(),G_in.ecount(),2*G_in.ecount()/G_in.vcount())


    ci_nodes_city_rca = {}
    isolated_nodes_city_rca = {}

    for city in tqdm(city_codes):
        occu_temp = []
        for o in city_occupations[city]:
            emp = city_emp[city][o]
            if (o in occupations_6digit) and (emp != 0):
                occu_temp.append(o)
                
                
        G1_in = G_in.induced_subgraph(occu_temp)
        ci_nodes_temp, isolated_nodes_temp = weighted_ci_node(G1_in,h_order)
        
        ci_nodes_city_rca[city] = ci_nodes_temp
        isolated_nodes_city_rca[city] = isolated_nodes_temp


    return ci_nodes_city_rca, isolated_nodes_city_rca, G_in




def normalized_osv_rca_weighted_ci (thre = 0, fd = 'db_25_0_text', h_order = 1):
    
    save_time = '2020may'
    city_codes = load_obj('occupations_city/' + save_time +'/city_codes_'+ save_time)
    city_names = load_obj('occupations_city/' + save_time +'/city_names_'+ save_time)
    city_occupations = load_obj('occupations_city/' + save_time +'/city_occupations_'+ save_time)
    city_occupations_names = load_obj('occupations_city/' + save_time +'/city_occupations_names_'+ save_time)
    city_emp = load_obj('occupations_city/' + save_time +'/city_emp_'+ save_time)

    #
    fd_osv_6digit = load_obj('osv_n_6digit/osv_n_6digit_'+fd)
    occupations_6digit = load_obj('osv_n_6digit/occupations_6digit_'+fd)
    occupations_6digit_names = load_obj('osv_n_6digit/occupations_6digit_names_'+fd)

    G = load_obj('rca_n_6digit_graph/rca_n_graph_6digit_'+fd)
    edge_sq = G.es.select(weight_gt=thre)
    G_in = G.subgraph_edges(edge_sq, delete_vertices = False)
    #G_in.es["weight"] = 1
    print(G_in.vcount(),G_in.ecount(),2*G_in.ecount()/G_in.vcount())

    ci_nodes_city_rca_n = {}
    isolated_nodes_city_rca_n = {}

    for city in tqdm(city_codes):
        occu_temp = []
        for o in city_occupations[city]:
            emp = city_emp[city][o]
            if (o in occupations_6digit) and (emp != 0):
                occu_temp.append(o)
                
                
        G1_in = G_in.induced_subgraph(occu_temp)
        ci_nodes_temp, isolated_nodes_temp = weighted_ci_node(G1_in,h_order)
        
        ci_nodes_city_rca_n[city] = ci_nodes_temp
        isolated_nodes_city_rca_n[city] = isolated_nodes_temp


    return ci_nodes_city_rca_n, isolated_nodes_city_rca_n, G_in




def skillsim_weighted_ci(thre = 0, fd = 'db_25_0_text', h_order = 1):
    
    save_time = '2020may'
    city_codes = load_obj('occupations_city/' + save_time +'/city_codes_'+ save_time)
    city_names = load_obj('occupations_city/' + save_time +'/city_names_'+ save_time)
    city_occupations = load_obj('occupations_city/' + save_time +'/city_occupations_'+ save_time)
    city_occupations_names = load_obj('occupations_city/' + save_time +'/city_occupations_names_'+ save_time)
    city_emp = load_obj('occupations_city/' + save_time +'/city_emp_'+ save_time)

    #

    fd_osv_6digit = load_obj('osv_n_6digit/osv_n_6digit_'+fd)
    occupations_6digit = load_obj('osv_n_6digit/occupations_6digit_'+fd)
    occupations_6digit_names = load_obj('osv_n_6digit/occupations_6digit_names_'+fd)

    G = load_obj('skillsim_6digit_graph/skillsim_graph_6digit_'+fd)
    edge_sq = G.es.select(weight_gt=thre)
    G_in = G.subgraph_edges(edge_sq, delete_vertices = False)
    #G_in.es["weight"] = 1
    print(G_in.vcount(),G_in.ecount(),2*G_in.ecount()/G_in.vcount())

    ci_nodes_city_skillsim = {}
    isolated_nodes_city_skillsim = {}

    for city in tqdm(city_codes):
        occu_temp = []
        for o in city_occupations[city]:
            emp = city_emp[city][o]
            if (o in occupations_6digit) and (emp != 0):
                occu_temp.append(o)
                
                
        G1_in = G_in.induced_subgraph(occu_temp)
        ci_nodes_temp, isolated_nodes_temp = weighted_ci_node(G1_in,h_order)
        
        ci_nodes_city_skillsim[city] = ci_nodes_temp
        isolated_nodes_city_skillsim[city] = isolated_nodes_temp

    return ci_nodes_city_skillsim, isolated_nodes_city_skillsim, G_in



def jc_weighted_ci(thre = 0, fd = 'db_25_0_text', h_order = 1):
    
    save_time = '2020may'
    city_codes = load_obj('occupations_city/' + save_time +'/city_codes_'+ save_time)
    city_names = load_obj('occupations_city/' + save_time +'/city_names_'+ save_time)
    city_occupations = load_obj('occupations_city/' + save_time +'/city_occupations_'+ save_time)
    city_occupations_names = load_obj('occupations_city/' + save_time +'/city_occupations_names_'+ save_time)
    city_emp = load_obj('occupations_city/' + save_time +'/city_emp_'+ save_time)

    #
    fd_osv_6digit = load_obj('osv_n_6digit/osv_n_6digit_'+fd)
    occupations_6digit = load_obj('osv_n_6digit/occupations_6digit_'+fd)
    occupations_6digit_names = load_obj('osv_n_6digit/occupations_6digit_names_'+fd)

    G = load_obj('job_complementarity_6digit_graph/jc_graph_6digit_'+fd)
    edge_sq = G.es.select(weight_gt=thre)
    G_in = G.subgraph_edges(edge_sq, delete_vertices = False)
    print(G_in.vcount(),G_in.ecount(),2*G_in.ecount()/G_in.vcount())

    ci_nodes_city_jc = {}
    isolated_nodes_city_jc = {}

    for city in tqdm(city_codes):
        occu_temp = []
        for o in city_occupations[city]:
            emp = city_emp[city][o]
            if (o in occupations_6digit) and (emp != 0):
                occu_temp.append(o)
                
                
        G1_in = G_in.induced_subgraph(occu_temp)
        ci_nodes_temp, isolated_nodes_temp = weighted_ci_node(G1_in,h_order)
        
        ci_nodes_city_jc[city] = ci_nodes_temp
        isolated_nodes_city_jc[city] = isolated_nodes_temp

    return ci_nodes_city_jc, isolated_nodes_city_jc, G_in
    