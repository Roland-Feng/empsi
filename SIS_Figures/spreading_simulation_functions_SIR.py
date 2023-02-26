from unicodedata import name
from pickle_file import load_obj,save_obj
from tqdm import tqdm
import os
from datetime import datetime
import numpy as np
import networkx as nx
import igraph as ig
from ONet_fd import ONet_fd
import random as rd
import pandas as pd
import copy
from prettytable import PrettyTable

topn = 20

def spreading_simulation_empci_SIR(city='', simulation_times = 20, name_index = '_20', seed_ratio = 0.001, spread_ratio = 1, recover_ratio = 0.1, fn_index=''):
    
    #fd_increase1 = load_obj('fd_increase1')
    fd_increase2 = load_obj('fd_increase2')

    fd = fd_increase2[-1]
    save_time = '2020may'
    city_names = load_obj('occupations_city/' + save_time +'/city_names_'+ save_time)
    city_occupations = load_obj('occupations_city/' + save_time +'/city_occupations_'+ save_time)
    city_emp = load_obj('occupations_city/' + save_time +'/city_emp_'+ save_time)
    occupations_6digit = load_obj('osv_6digit/occupations_6digit_'+fd)

    ci_nodes_city_skillsim = load_obj('skillsim_ci_results/ci_nodes_city_skillsim_0')

    ## 考虑emp
    def emp_ci(ci_city):

        emp_ci_city = {}

        save_time = '2020may'
        city_codes = load_obj('occupations_city/' + save_time +'/city_codes_'+ save_time)
        city_emp = load_obj('occupations_city/' + save_time +'/city_emp_'+ save_time)

        for city_temp in city_codes:
            temp_lbci = []
            temp_names = []

            for i in range(0, len(ci_city[city_temp][1])):
                o = ci_city[city_temp][1][i]
                ci = ci_city[city_temp][0][i]
                temp_lbci.append(np.log(city_emp[city_temp][o]) * ci)
                temp_names.append(o)


            weighted_ci_values, weighted_ci_names = zip(*sorted(zip(temp_lbci,temp_names), reverse = True))

            emp_ci_city[city_temp] = [weighted_ci_values, weighted_ci_names]

        return emp_ci_city

    skillsim_emp_ci = emp_ci(ci_nodes_city_skillsim)



    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    print(city_names[city])

    fd = fd_increase2[-1]
    skillsim = load_obj('skillsim_6digit/skillsim_'+fd)

    def simulation_empci(step_number = 30):

        emp_temp = {}
        infection_now = {}
        infection_next = {}
        occu_temp = []
        for o in city_occupations[city]:
            if city_emp[city][o] != 0 and o in occupations_6digit:
                occu_temp.append(o)
                emp_temp[o] = city_emp[city][o]
                infection_now[o] = 0
                infection_next[o] = 0


        emp_total = 0
        for empttt in city_emp[city].values():
            emp_total += empttt

        starting_total = round(emp_total * seed_ratio)
        starting_average = round(starting_total / topn)

        starting_occu = []
        starting_occu_emp_temp = 0

        for o in skillsim_emp_ci[city][1][0:topn]:
            if city_emp[city][o] < starting_average:
                infection_now[o] = city_emp[city][o]
                infection_next[o] = city_emp[city][o]


            if city_emp[city][o] >= starting_average:
                infection_now[o] = starting_average
                infection_next[o] = starting_average


        infection_dict_list = []
        for step in tqdm(range(0,step_number)):
            for o1 in occu_temp:
                target_occu = np.random.choice(occu_temp, infection_now[o1])
                for o2 in target_occu:
                    if o2 != o1:
                        temp = np.random.uniform()
                        temp_pro = (emp_temp[o2] - infection_next[o2])/emp_temp[o2]
                        if temp < skillsim[o1][o2] * temp_pro * spread_ratio and infection_next[o2] < emp_temp[o2]:
                            infection_next[o2] += 1

                    if o2 == o1:
                    #    infection_next[o2] += 1
                        temp = np.random.uniform()
                        temp_pro = (emp_temp[o2] - infection_next[o2])/emp_temp[o2]
                        if temp < temp_pro * spread_ratio and infection_next[o2] < emp_temp[o2]:
                            infection_next[o2] += 1

            for o1 in occu_temp:
                temp_infection_next = infection_next[o1]
                temp = np.random.uniform()
                if temp < recover_ratio:
                    if temp_infection_next > 0:
                        temp_infection_next -= 1
                
                infection_now[o1] = temp_infection_next
                

            temp = copy.deepcopy(infection_now)

            infection_dict_list.append(temp)

        return infection_dict_list


    infection_dict_list_20 = []
    for i in range(0,simulation_times):
        infection_dict_list_20.append(simulation_empci(40))


    
    save_obj(infection_dict_list_20, 'spreading_analysis_SIR/'+fn_index + '/spreading_simulation_empci_SIR_' + 'ratio_' + '_'+city+'_'+name_index)


#############################################################################################################################################################################
#############################################################################################################################################################################
#############################################################################################################################################################################
#############################################################################################################################################################################





def spreading_simulation_emp_SIR(city='', simulation_times = 20, name_index = '_20', seed_ratio = 0.001, spread_ratio = 1, recover_ratio = 0.1, fn_index=''):

    ## fd_set 文件位置：'obj_fd_set/fd_set_' + fd
    ## o_s_vector 文件位置： 'obj_osv_n/osv_n_' + fd, skill的顺序文件是 'obj_o_s_vector/skill_list'
    fd_increase2 = load_obj('fd_increase2')

    fd = fd_increase2[-1]
    save_time = '2020may'
    city_names = load_obj('occupations_city/' + save_time +'/city_names_'+ save_time)
    city_occupations = load_obj('occupations_city/' + save_time +'/city_occupations_'+ save_time)
    city_emp = load_obj('occupations_city/' + save_time +'/city_emp_'+ save_time)
    occupations_6digit = load_obj('osv_6digit/occupations_6digit_'+fd)
    
    print(city_names[city])

    fd = fd_increase2[-1]
    skillsim = load_obj('skillsim_6digit/skillsim_'+fd)

    def simulation_emp(step_number = 30):
        
        emp_temp = {}
        emp_temp_list = []
        infection_now = {}
        infection_next = {}
        occu_temp = []
        for o in city_occupations[city]:
            if city_emp[city][o] != 0 and o in occupations_6digit:
                occu_temp.append(o)
                emp_temp[o] = city_emp[city][o]
                emp_temp_list.append(city_emp[city][o])
                infection_now[o] = 0
                infection_next[o] = 0


        emp_total = 0
        for empttt in city_emp[city].values():
            emp_total += empttt

        
        #topn = 1
        starting_total = round(emp_total * seed_ratio)
        starting_average = round(starting_total / topn)

        b, a = zip(*sorted(zip(emp_temp_list,occu_temp),reverse = True))


        starting_occu = []
        starting_occu_emp_temp = 0

        for o in a[0:topn]:
            if city_emp[city][o] < starting_average:
                infection_now[o] = city_emp[city][o]
                infection_next[o] = city_emp[city][o]


            if city_emp[city][o] >= starting_average:
                infection_now[o] = starting_average
                infection_next[o] = starting_average

        infection_dict_list = []
        for step in tqdm(range(0,step_number)):
            for o1 in occu_temp:
                target_occu = np.random.choice(occu_temp, infection_now[o1])
                for o2 in target_occu:
                    if o2 != o1:
                        temp = np.random.uniform()
                        temp_pro = (emp_temp[o2] - infection_next[o2])/emp_temp[o2]
                        if temp < skillsim[o1][o2] * temp_pro * spread_ratio and infection_next[o2] < emp_temp[o2]:
                            infection_next[o2] += 1


                    if o2 == o1:
                        #    infection_next[o2] += 1
                        temp = np.random.uniform()
                        temp_pro = (emp_temp[o2] - infection_next[o2])/emp_temp[o2]
                        if temp < temp_pro * spread_ratio and infection_next[o2] < emp_temp[o2]:
                            infection_next[o2] += 1



            for o1 in occu_temp:
                temp_infection_next = infection_next[o1]
                temp = np.random.uniform()
                if temp < recover_ratio:
                    if temp_infection_next > 0:
                        temp_infection_next -= 1
                
                infection_now[o1] = temp_infection_next

            temp = copy.deepcopy(infection_now)

            infection_dict_list.append(temp)

        return infection_dict_list


    infection_dict_list_20 = []
    for i in range(0,simulation_times):
        infection_dict_list_20.append(simulation_emp(40))



    save_obj(infection_dict_list_20, 'spreading_analysis_SIR/'+fn_index + '/spreading_simulation_emp_SIR_' + 'ratio_' + '_'+city+'_'+name_index)


#############################################################################################################################################################################
#############################################################################################################################################################################
#############################################################################################################################################################################
#############################################################################################################################################################################



def spreading_simulation_strength_SIR(city='', simulation_times = 20, name_index = '_20', seed_ratio = 0.001, spread_ratio = 1, recover_ratio = 0.1, fn_index=''):
    
    ## fd_set 文件位置：'obj_fd_set/fd_set_' + fd
    ## o_s_vector 文件位置： 'obj_osv_n/osv_n_' + fd, skill的顺序文件是 'obj_o_s_vector/skill_list'
    #fd_increase1 = load_obj('fd_increase1')
    fd_increase2 = load_obj('fd_increase2')
    fd = fd_increase2[-1]

    save_time = '2020may'
    city_occupations = load_obj('occupations_city/' + save_time +'/city_occupations_'+ save_time)
    city_names = load_obj('occupations_city/' + save_time +'/city_names_'+ save_time)
    city_emp = load_obj('occupations_city/' + save_time +'/city_emp_'+ save_time)
    occupations_6digit = load_obj('osv_6digit/occupations_6digit_'+fd)
    
    ###################################################################################################

    thre = 0
    G = load_obj('skillsim_6digit_graph/skillsim_graph_6digit_'+fd)
    edge_sq = G.es.select(weight_gt=thre)
    G_in = G.subgraph_edges(edge_sq, delete_vertices = False)
    #G_in.es["weight"] = 1
    print(G_in.vcount(),G_in.ecount(),2*G_in.ecount()/G_in.vcount())

    strength_nodes = {}
    occu_temp = []
    for o in city_occupations[city]:
        emp = city_emp[city][o]
        if (o in occupations_6digit) and (emp != 0):
            occu_temp.append(o)


    G1_in = G_in.induced_subgraph(occu_temp)
    strength_values_temp = []
    strength_nodes_temp = []
    for o in occu_temp:
        strength_nodes_temp.append(o)
        strength_values_temp.append(G1_in.strength(o,weights = 'weight'))

    s_values_temp, s_nodes_temp = zip(*sorted(zip(strength_values_temp,strength_nodes_temp), reverse=True))
    strength_nodes[city] = s_nodes_temp


    ############################################################################################

    print(city_names[city])

    fd = fd_increase2[-1]
    skillsim = load_obj('skillsim_6digit/skillsim_'+fd)

    def simulation_strength(step_number = 30):
        emp_temp = {}
        infection_now = {}
        infection_next = {}
        occu_temp = []
        for o in city_occupations[city]:
            if city_emp[city][o] != 0 and o in occupations_6digit:
                occu_temp.append(o)
                emp_temp[o] = city_emp[city][o]
                infection_now[o] = 0
                infection_next[o] = 0


        emp_total = 0
        for empttt in city_emp[city].values():
            emp_total += empttt

        #topn = 1
        starting_total = round(emp_total * seed_ratio)
        starting_average = round(starting_total / topn)

        starting_occu = []
        starting_occu_emp_temp = 0

        for o in strength_nodes[city][0:topn]:
            if city_emp[city][o] < starting_average:
                infection_now[o] = city_emp[city][o]
                infection_next[o] = city_emp[city][o]


            if city_emp[city][o] >= starting_average:
                infection_now[o] = starting_average
                infection_next[o] = starting_average

        infection_dict_list = []
        for step in tqdm(range(0,step_number)):
            for o1 in occu_temp:
                target_occu = np.random.choice(occu_temp, infection_now[o1])
                for o2 in target_occu:
                    if o2 != o1:
                        temp = np.random.uniform()
                        temp_pro = (emp_temp[o2] - infection_next[o2])/emp_temp[o2]
                        if temp < skillsim[o1][o2] * temp_pro * spread_ratio and infection_next[o2] < emp_temp[o2]:
                            infection_next[o2] += 1

                    if o2 == o1:
                        #    infection_next[o2] += 1
                        temp = np.random.uniform()
                        temp_pro = (emp_temp[o2] - infection_next[o2])/emp_temp[o2]
                        if temp < temp_pro * spread_ratio and infection_next[o2] < emp_temp[o2]:
                            infection_next[o2] += 1



            for o1 in occu_temp:
                temp_infection_next = infection_next[o1]
                temp = np.random.uniform()
                if temp < recover_ratio:
                    if temp_infection_next > 0:
                        temp_infection_next -= 1
                
                infection_now[o1] = temp_infection_next

            temp = copy.deepcopy(infection_now)

            infection_dict_list.append(temp)

        return infection_dict_list


    infection_dict_list_20 = []
    for i in range(0,simulation_times):
        infection_dict_list_20.append(simulation_strength(40))


    save_obj(infection_dict_list_20, 'spreading_analysis_SIR/'+fn_index + '/spreading_simulation_strength_SIR_' + 'ratio_' + '_'+city+'_'+name_index)


#############################################################################################################################################################################
#############################################################################################################################################################################
#############################################################################################################################################################################
#############################################################################################################################################################################




def spreading_simulation_log_emp_strength_SIR(city='', simulation_times = 20, name_index = '_20', seed_ratio = 0.001, spread_ratio = 1, recover_ratio = 0.1, fn_index=''):
    ## fd_set 文件位置：'obj_fd_set/fd_set_' + fd
    ## o_s_vector 文件位置： 'obj_osv_n/osv_n_' + fd, skill的顺序文件是 'obj_o_s_vector/skill_list'
    fd_increase2 = load_obj('fd_increase2')
    fd = fd_increase2[-1]
    save_time = '2020may'
    
    ###################################################################################################
    thre = 0

    city_names = load_obj('occupations_city/' + save_time +'/city_names_'+ save_time)
    city_occupations = load_obj('occupations_city/' + save_time +'/city_occupations_'+ save_time)
    city_emp = load_obj('occupations_city/' + save_time +'/city_emp_'+ save_time)
    occupations_6digit = load_obj('osv_n_6digit/occupations_6digit_'+fd)
    
    G = load_obj('skillsim_6digit_graph/skillsim_graph_6digit_'+fd)
    edge_sq = G.es.select(weight_gt=thre)
    G_in = G.subgraph_edges(edge_sq, delete_vertices = False)
    #G_in.es["weight"] = 1
    print(G_in.vcount(),G_in.ecount(),2*G_in.ecount()/G_in.vcount())

    strength_nodes = {}
    occu_temp = []
    for o in city_occupations[city]:
        emp = city_emp[city][o]
        if (o in occupations_6digit) and (emp != 0):
            occu_temp.append(o)
            
    G1_in = G_in.induced_subgraph(occu_temp)
    strength_values_temp = []
    strength_nodes_temp = []

    for o in occu_temp:
        strength_nodes_temp.append(o)
        strength_values_temp.append(G1_in.strength(o,weights = 'weight') * np.log(city_emp[city][o]))

    s_values_temp, s_nodes_temp = zip(*sorted(zip(strength_values_temp,strength_nodes_temp), reverse=True))

    strength_nodes[city] = s_nodes_temp


    ############################################################################################
    print(city_names[city])

    fd = fd_increase2[-1]
    skillsim = load_obj('skillsim_6digit/skillsim_'+fd)

    def simulation_strength(step_number = 30):
        emp_temp = {}
        infection_now = {}
        infection_next = {}
        occu_temp = []
        for o in city_occupations[city]:
            if city_emp[city][o] != 0 and o in occupations_6digit:
                occu_temp.append(o)
                emp_temp[o] = city_emp[city][o]
                infection_now[o] = 0
                infection_next[o] = 0


        emp_total = 0
        for empttt in city_emp[city].values():
            emp_total += empttt

        #topn = 1
        starting_total = round(emp_total * seed_ratio)
        starting_average = round(starting_total / topn)

        starting_occu = []
        starting_occu_emp_temp = 0

        for o in strength_nodes[city][0:topn]:
            if city_emp[city][o] < starting_average:
                infection_now[o] = city_emp[city][o]
                infection_next[o] = city_emp[city][o]


            if city_emp[city][o] >= starting_average:
                infection_now[o] = starting_average
                infection_next[o] = starting_average

        infection_dict_list = []
        for step in tqdm(range(0,step_number)):
            for o1 in occu_temp:
                target_occu = np.random.choice(occu_temp, infection_now[o1])
                for o2 in target_occu:
                    if o2 != o1:
                        temp = np.random.uniform()
                        temp_pro = (emp_temp[o2] - infection_next[o2])/emp_temp[o2]
                        if temp < skillsim[o1][o2] * temp_pro * spread_ratio and infection_next[o2] < emp_temp[o2]:
                            infection_next[o2] += 1

                    if o2 == o1:
                        #    infection_next[o2] += 1
                        temp = np.random.uniform()
                        temp_pro = (emp_temp[o2] - infection_next[o2])/emp_temp[o2]
                        if temp < temp_pro * spread_ratio and infection_next[o2] < emp_temp[o2]:
                            infection_next[o2] += 1


            for o1 in occu_temp:
                temp_infection_next = infection_next[o1]
                temp = np.random.uniform()
                if temp < recover_ratio:
                    if temp_infection_next > 0:
                        temp_infection_next -= 1
                
                infection_now[o1] = temp_infection_next

            temp = copy.deepcopy(infection_now)

            infection_dict_list.append(temp)

        return infection_dict_list


    infection_dict_list_20 = []
    for i in range(0,simulation_times):
        infection_dict_list_20.append(simulation_strength(40))


    save_obj(infection_dict_list_20, 'spreading_analysis_SIR/'+fn_index + '/spreading_simulation_log_emp_strength_SIR_' + 'ratio_' + '_'+city+'_'+name_index)

#############################################################################################################################################################################
#############################################################################################################################################################################
#############################################################################################################################################################################
#############################################################################################################################################################################




def spreading_simulation_random_SIR(city='', simulation_times = 20, name_index = '_20', seed_ratio = 0.001, spread_ratio = 1, recover_ratio = 0.1, fn_index=''):
    #fd_increase1 = load_obj('fd_increase1')
    fd_increase2 = load_obj('fd_increase2')
    fd = fd_increase2[-1]
    save_time = '2020may'
    
    city_names = load_obj('occupations_city/' + save_time +'/city_names_'+ save_time)
    city_occupations = load_obj('occupations_city/' + save_time +'/city_occupations_'+ save_time)
    
    city_emp = load_obj('occupations_city/' + save_time +'/city_emp_'+ save_time)

    occupations_6digit = load_obj('osv_6digit/occupations_6digit_'+fd)
    
    ci_nodes_city_skillsim = load_obj('skillsim_ci_results/ci_nodes_city_skillsim_0')
    print(city_names[city])
    skillsim = load_obj('skillsim_6digit/skillsim_'+fd)

    def simulation_random(step_number = 30):
        emp_temp = {}
        infection_now = {}
        infection_next = {}
        occu_temp = []
        for o in city_occupations[city]:
            if city_emp[city][o] != 0 and o in occupations_6digit:
                occu_temp.append(o)
                emp_temp[o] = city_emp[city][o]
                infection_now[o] = 0
                infection_next[o] = 0


        emp_total = 0
        for empttt in city_emp[city].values():
            emp_total += empttt

        #topn = 1
        starting_total = round(emp_total * seed_ratio)
        starting_average = round(starting_total / topn)

        starting_occu_random = np.random.choice(ci_nodes_city_skillsim[city][1], len(ci_nodes_city_skillsim[city][1]), replace = False)

        starting_occu = []
        starting_occu_emp_temp = 0

        for o in starting_occu_random[0:topn]:
            if city_emp[city][o] < starting_average:
                infection_now[o] = city_emp[city][o]
                infection_next[o] = city_emp[city][o]


            if city_emp[city][o] >= starting_average:
                infection_now[o] = starting_average
                infection_next[o] = starting_average
                
        infection_dict_list = []
        for step in tqdm(range(0,step_number)):
            for o1 in occu_temp:
                target_occu = np.random.choice(occu_temp, infection_now[o1])
                for o2 in target_occu:
                    if o2 != o1:
                        temp = np.random.uniform()
                        temp_pro = (emp_temp[o2] - infection_next[o2])/emp_temp[o2]
                        if temp < skillsim[o1][o2] * temp_pro * spread_ratio and infection_next[o2] < emp_temp[o2]:
                            infection_next[o2] += 1

                    if o2 == o1:
                        #    infection_next[o2] += 1
                        temp = np.random.uniform()
                        temp_pro = (emp_temp[o2] - infection_next[o2])/emp_temp[o2]
                        if temp < temp_pro * spread_ratio and infection_next[o2] < emp_temp[o2]:
                            infection_next[o2] += 1


            for o1 in occu_temp:
                temp_infection_next = infection_next[o1]
                temp = np.random.uniform()
                if temp < recover_ratio:
                    if temp_infection_next > 0:
                        temp_infection_next -= 1
                
                infection_now[o1] = temp_infection_next

            temp = copy.deepcopy(infection_now)

            infection_dict_list.append(temp)

        return infection_dict_list


    infection_dict_list_20 = []
    for i in range(0,simulation_times):
        infection_dict_list_20.append(simulation_random(40))



    save_obj(infection_dict_list_20, 'spreading_analysis_SIR/'+fn_index + '/spreading_simulation_random_SIR_' + 'ratio_' + '_'+city+'_'+name_index)