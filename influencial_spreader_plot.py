from pickle import load
from control_node import get_networkx_graph
from pickle_file import load_obj, save_obj
import pandas as pd


def ci_plot(G_in, SOC, city, ci_nodes, save_sign, fd):

    save_time = '2020may'
    city_codes = load_obj('occupations_city/' + save_time +'/city_codes_'+ save_time)
    city_names = load_obj('occupations_city/' + save_time +'/city_names_'+ save_time)
    city_occupations = load_obj('occupations_city/' + save_time +'/city_occupations_'+ save_time)
    city_occupations_names = load_obj('occupations_city/' + save_time +'/city_occupations_names_'+ save_time)
    city_emp = load_obj('occupations_city/' + save_time +'/city_emp_'+ save_time)

    occupations_6digit = load_obj('osv_n_6digit/occupations_6digit_'+fd)
    occupations_6digit_names = load_obj('osv_n_6digit/occupations_6digit_names_'+fd)

    G_nx = get_networkx_graph(G_in)
    occupations_list = []
    emp_list = []
    occupation_name_list = []

    print(city_names[city])


    for o in city_occupations[city]:
        emp = city_emp[city][o]
        name = city_occupations_names[city][o]
        if o in occupations_6digit and emp != 0:
            occupations_list.append(o)
            emp_list.append(emp)
            occupation_name_list.append(name)
            
    control_nodes_list = ci_nodes[city][1][0:20]


    ## 按照sector分community

    soc_sector_list = []
    for i in SOC.keys():
        soc_sector_list.append(i)

    soc_num = []

    for o in G_nx.nodes:
        soc = o[0:2]
        soc_num.append(SOC[soc])
        
    from collections import Counter
    sector_list = list(Counter(soc_num).keys())
    print(sector_list)
    Counter(soc_num)

    community_index_sector = {}

    for o in G_nx.nodes:
        community_index_sector[o] = sector_list.index(SOC[o[0:2]])


    ###################################################################
    ###################################################################
    ###################################################################

    ## 把所有的控制节点聚合在一起
    # import pandas as pd
    # temp = []
    # for c in control_dict_list:
    #     for fd in fd_increase2_mini[-1:]:
    #         temp += c[fd]
            
            
    control_nodes = pd.Series(control_nodes_list)
    print(control_nodes.unique())
    pd.set_option('display.max.rows', 500)
    control_nodes_count = control_nodes.value_counts()
    print(control_nodes_count)

    print('============================================================')

    ###################################################################
    ###################################################################
    ###################################################################

    ## 全部节点的颜色，大小
    node_color_sector = [community_index_sector[n] for n in G_nx.nodes]
    node_size_gnx = []
    labels_control = {}

    emp_const = 59

    for n in G_nx.nodes:
        emp = emp_const
        if n in occupations_list:
            i = occupations_list.index(n)
            emp = emp_list[i]/sum(emp_list) * 30000 + 59
            
        node_size_gnx.append(emp)
        
        if n in control_nodes_count.index:
            if control_nodes_count[n] >= 1:
                labels_control[n] = n
            
        
    ###################################################################
    ###################################################################
    ###################################################################

    ## 颜色方案

    ## 先用cm.get_cmap得到颜色映射，再把一个float映射到rgb，在用to_hex把颜色映射成hex
    #from matplotlib import cm
    #co = cm.get_cmap('viridis',max(node_color_sector)+1)

    #print(co(1/5))

    #import matplotlib.colors as mcs

    #hex_color_list = []
    #for i in range(0,max(node_color_sector)+1):
    #    print(i/max(node_color_sector))
    #    hex_color_list.append(mcs.to_hex(co(i/(max(node_color_sector)))[0:3]))

    #print(hex_color_list)

    SOC_color = load_obj('SOC_color_'+str(len(list(set(list(SOC.values()))))))


    ###################################################################
    ###################################################################
    ###################################################################

    ## 分开节点，分开大小、颜色
    node_lists = []
    node_size_gnx_lists = []
    for i in range(0,max(node_color_sector)+1):
        node_size_gnx_lists.append([])
        node_lists.append([])


    ## 不在city的occupation
    occupation_not_in_city = []
    for n in G_nx.nodes:
        if n not in occupations_list:
            occupation_not_in_city.append(n)
        
    for c,s,n in zip(node_color_sector, node_size_gnx,G_nx.nodes):
        if n in occupations_list:
            node_size_gnx_lists[c].append(s)
            node_lists[c].append(n)

    # for c,s,n in zip(node_color_sector, node_size_gnx,G_nx.nodes):
    #     node_size_gnx_lists[c].append(s)
    #     node_lists[c].append(n)

        
    node_lists_sorted = []
    node_size_gnx_lists_sorted = []
    hex_color_list = []
    for nl, ns in zip(node_lists, node_size_gnx_lists):
        temps, templ = zip(*sorted(zip(ns,nl),reverse = True))
        node_lists_sorted.append(templ)
        node_size_gnx_lists_sorted.append(temps)
        hex_color_list.append(SOC_color[nl[0][0:2]])
        

    ###################################################################
    ###################################################################
    ###################################################################


    ## 分开画节点的情况
    import networkx as nx
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(20, 15))
    pos_gnx = nx.spring_layout(G_nx, k=0.15, seed=76421231)

    nx.draw_networkx_nodes(G_nx, pos = pos_gnx, nodelist = occupation_not_in_city,
                            node_color = 'gainsboro', node_size = emp_const, alpha = 0.76)

    for nc, ns, nl,s in zip(hex_color_list, node_size_gnx_lists_sorted, node_lists_sorted, sector_list):
        nx.draw_networkx_nodes(G_nx, pos = pos_gnx, nodelist = nl,
                            node_color = nc, node_size = ns, alpha = 0.76)
        
    for nc, ns, nl,s in zip(hex_color_list, node_size_gnx_lists_sorted, node_lists_sorted, sector_list):
        nx.draw_networkx_nodes(G_nx, pos = pos_gnx, nodelist = [nl[0]],
                            node_color = nc, label = s, node_size = [emp_const], alpha = 0.64)

    nx.draw_networkx_edges(G_nx, pos=pos_gnx,edge_color='gainsboro',width = 0.3)
    # nx.draw_networkx_labels(G_nx, pos = pos_gnx, labels = labels_control, font_size=14)

    # lx = []
    # ly = []
    # for a in pos_gnx.values():
    #     lx.append(a[0])
    #     ly.append(a[1])
        
    # o_list_label = []
    # x_list_label = []
    # y_list_label = []
    # for o in labels_control.keys():
    #     o_list_label.append(o)
    #     x_list_label.append(pos_gnx[o][0])
    #     y_list_label.append(pos_gnx[o][1])
        

    # y_list_label, x_list_label, o_list_label = zip(*sorted(zip(y_list_label, x_list_label, o_list_label)))


    # x_list= []
    # y_list = []
    # for o in pos_gnx.keys():
    #     x_list.append(pos_gnx[o][0])
    #     y_list.append(pos_gnx[o][1])
        

    # new_loc = {}

    # interval = (max(y_list) - min(y_list))/(2*len(o_list_label))
    # for i in range(0,len(o_list_label)):
    #     o = o_list_label[i]
    #     new_loc[o] = [min(x_list), min(y_list) + interval * 1 * len(o_list_label) + i * interval]
        
    # for o in o_list_label:
    #     plt.text(new_loc[o][0],new_loc[o][1], labels_control[o] + ': ' + occupations_6digit_names[o], fontsize = 12)

    font1 = {'family':'Times New Roman',
            'weight' : 'extra bold',
            'size'   : 28,
    }
    
    legend = plt.legend(prop=font1)
    plt.legend(scatterpoints = 1, ncol = 3)

    ax.margins(0.1, 0.05)
    fig.tight_layout()
    plt.axis("off")
    #plt.title(city_names[city],fontsize=30)

    if save_sign:
        plt.savefig(city_names[city] + '_empci_network.pdf',format = 'pdf')
    
    plt.show()