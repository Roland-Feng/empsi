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
## fd_set 文件位置：'obj_fd_set/fd_set_' + fd
## o_s_vector 文件位置： 'obj_osv_n/osv_n_' + fd, skill的顺序文件是 'obj_o_s_vector/skill_list'
fd_list = load_obj('folder_list')
#fd_increase1 = load_obj('fd_increase1')
fd_increase2 = load_obj('fd_increase2')
skill_list_std = load_obj('obj_osv_n/skill_list')
skill_dict = load_obj('skill_dict')
fd_time = load_obj('fd_time')
occupation_name = load_obj('occupation_name_increase2')

from influencial_spreader_node import unnormalized_osv_rca_weighted_ci,normalized_osv_rca_weighted_ci,jc_weighted_ci
from influencial_spreader_node import skillsim_weighted_ci
fd = fd_increase2[-1]

cognitive_score = ('cognitive_score_6digit_osv_n/cognitive_score_6digit_osv_n_'+ fd)

save_time = '2020may'
city_codes = load_obj('occupations_city/' + save_time +'/city_codes_'+ save_time)
city_names = load_obj('occupations_city/' + save_time +'/city_names_'+ save_time)
city_occupations = load_obj('occupations_city/' + save_time +'/city_occupations_'+ save_time)
city_occupations_names = load_obj('occupations_city/' + save_time +'/city_occupations_names_'+ save_time)
city_emp = load_obj('occupations_city/' + save_time +'/city_emp_'+ save_time)
state_abbr = load_obj('occupations_city/' + save_time +'/state_abbr_'+ save_time)
city_county_names = load_obj('occupations_city/' + save_time +'/city_county_names_'+ save_time)
city_geo_dict = load_obj('occupations_city/' + save_time +'/city_geo_dict_'+ save_time)
city_occupations_wage_median = load_obj('occupations_city/' + save_time +'/city_occupations_wage_median_'+ save_time)

occupations_6digit = load_obj('osv_6digit/occupations_6digit_'+fd)
occupations_6digit_names = load_obj('osv_6digit/occupations_6digit_names_'+fd)


fd = fd_increase2[-1]
thre = 0
ci_order = 2

ci_nodes_city_skillsim, isolated_nodes_city_skillsim, G_in = skillsim_weighted_ci(thre, fd, ci_order)


save_obj(ci_nodes_city_skillsim, 'skillsim_ci_results/ci_nodes_city_skillsim_0_order_2')