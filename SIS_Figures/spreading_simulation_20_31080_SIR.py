import sys

from spreading_simulation_functions_SIR import spreading_simulation_empci_SIR, spreading_simulation_emp_SIR,spreading_simulation_strength_SIR

from spreading_simulation_functions_SIR import spreading_simulation_log_emp_strength_SIR, spreading_simulation_random_SIR



algoName = sys.argv[1]
#simulation_run = sys.argv[2] + '_400seeds'


##固定比例
simulation_run = sys.argv[2]
city = sys.argv[3]
target_ratio = float(sys.argv[4])
spread_rate = float(sys.argv[5])
recover_rate = float(sys.argv[6])
fn_index = sys.argv[7]

print(simulation_run)

if algoName == 'emp':
    spreading_simulation_emp_SIR(city, 1, str(simulation_run), target_ratio, spread_rate, recover_rate, fn_index)
    
    
if algoName == 'empci':
    spreading_simulation_empci_SIR(city, 1, str(simulation_run), target_ratio, spread_rate, recover_rate, fn_index)
    
    
if algoName == 'strength':
    spreading_simulation_strength_SIR(city, 1, str(simulation_run), target_ratio, spread_rate, recover_rate, fn_index)
    
    
if algoName == 'log_emp_strength':
    spreading_simulation_log_emp_strength_SIR(city, 1, str(simulation_run), target_ratio, spread_rate, recover_rate, fn_index)
    
    
    
if algoName == 'random':
    spreading_simulation_random_SIR(city, 1, str(simulation_run), target_ratio, spread_rate, recover_rate, fn_index)
    
    
    
############################################merge files

from pickle_file import load_obj,save_obj
import os

tempi = 0
for i in range(0,20):
    if not os.path.exists('obj/spreading_analysis_SIR/'+fn_index +'/'+'spreading_simulation_'+algoName + '_SIR_ratio_' + '_'+city+'_' + str(i+1)+'.pkl'):
        break
        
    tempi += 1
        
        
if tempi == 20:
    path = 'obj/spreading_analysis_SIR/' + fn_index
    path=path.strip()
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print('created')


    path_merge = 'obj/spreading_analysis_SIR/merged_' + fn_index

    path_merge=path_merge.strip()
    isExists=os.path.exists(path_merge)
    if not isExists:
        os.makedirs(path_merge)
        print('created')


    temp_merged = []

    for i in range(0,20):
        temp = load_obj('spreading_analysis_SIR/' + fn_index + '/' + 'spreading_simulation_'+algoName + '_SIR_ratio_' + '_'+city+'_' + str(i+1))
        temp_merged.append(temp[0])
        
    save_obj(temp_merged, 'spreading_analysis_SIR/merged_' + fn_index + '/' + city+'_merged_spreading_simulation_'+ algoName + '_SIR_ratio_' + '_'+city+'_20')
    
    
tempi = 0
algo_list = ['emp', 'empci','strength','log_emp_strength','random']
for algN in algo_list:
    if os.path.exists('obj/spreading_analysis_SIR/merged_' + fn_index + '/' + city+'_merged_spreading_simulation_'+ algN + '_SIR_ratio_' + '_'+city+'_20.pkl'):
        tempi += 1
        
        
if tempi == 5:
    from plot_spreading_SIR_functions_31080 import plot_spreading_SIR
    plot_spreading_SIR(city, fn_index)