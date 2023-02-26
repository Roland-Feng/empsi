from pickle_file import load_obj,save_obj

algo_list = ['emp', 'empci','strength','log_emp_strength','random']
#algo_list = ['strength','log_emp_strength']
city = '31080'

# for algo_wd in algo_list:
#     temp_merged = []
    
#     for i in range(0,20):
#         temp = load_obj('spreading_analysis/' + 'spreading_simulation_'+algo_wd + '_ratio_' + '_'+city+'__' + str(i+1)+'_400seeds')
#         temp_merged.append(temp[0])
        
        
#     save_obj(temp_merged, 'spreading_analysis/' + city+'_merged_spreading_simulation_'+ algo_wd + '_ratio_' + '_'+city+'_20_400seeds')
    
##固定比例
for algo_wd in algo_list:
    temp_merged = []
    
    for i in range(0,20):
        temp = load_obj('spreading_analysis_SIR/' + 'spreading_simulation_'+algo_wd + '_SIR_ratio_' + '_'+city+'__' + str(i+1))
        temp_merged.append(temp[0])
        
        
    save_obj(temp_merged, 'spreading_analysis_SIR/' + city+'_merged_spreading_simulation_'+ algo_wd + '_SIR_ratio_' + '_'+city+'_20')