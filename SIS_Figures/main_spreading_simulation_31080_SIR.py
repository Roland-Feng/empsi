import os

def submitJob(slurmFile, jobName, jobID, functionName, inputs_list):
    
    a,b,c,d,sc, rc, f_n_index = inputs_list
    with open(slurmFile, 'w') as fs:
        # write to the slurm file
        fs.writelines("#!/bin/bash\n")
        fs.writelines("#SBATCH --job-name={}\n".format(jobName))
        fs.writelines("#              d-hh:mm:ss\n")
        fs.writelines("#SBATCH --time=2:30:00\n")
        fs.writelines("#SBATCH --cpus-per-task=1\n")
        fs.writelines("#SBATCH --mem-per-cpu=1GB\n")
        fs.writelines("#SBATCH -o spreading_simulation_submit_files_SIR/outputfiles/"+f_n_index+'_'+a+"_"+c+"_output.{}.out # STDOUT\n".format(jobID))

        string_run_python_directory = "python3 {} {} {} {} {} {} {} {}".format(os.path.join(functionName),a,b,c,float(d), float(sc), float(rc), f_n_index)
        fs.writelines(string_run_python_directory)

    # send the job
    os.system("sbatch {}".format(slurmFile))
    
    
    
algo_list = ['emp', 'empci','strength','log_emp_strength','random']
city = '31080'

target_ratio = 0.002

import sys

spread_ratio = float(sys.argv[1])
recover_rate = float(sys.argv[2])

file_name_index = city + '_' + str(spread_ratio).replace('.','-') + '_' + str(recover_rate).replace('.','-')


path = 'obj/spreading_analysis_SIR/' + file_name_index
path=path.strip()
isExists=os.path.exists(path)
if not isExists:
    os.makedirs(path)
    print('created')
    
    
for algoName in algo_list:
    for i in range(0,20):
        if os.path.exists(path+'/'+'spreading_simulation_'+algoName+'_SIR_ratio_'+'_'+city+'_'+str(i+1)+'.pkl'):
            os.remove(path+'/'+'spreading_simulation_'+algoName+'_SIR_ratio_'+'_'+city+'_'+str(i+1)+'.pkl')
            
            
            
path_merge = 'obj/spreading_analysis_SIR/merged_' + file_name_index + '/'
path_merge=path_merge.strip()
isExists=os.path.exists(path_merge)
if not isExists:
    os.makedirs(path_merge)
    print('created')


if isExists:
    del_list = os.listdir(path_merge)
    for f in del_list:
        file_path = os.path.join(path_merge, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
            


##固定比例
for algo_wd in algo_list:
    for i in range(0,20):
        slurmFile_name = 'spreading_simulation_submit_files_SIR/' + 'submited_files/' + file_name_index +'_submit_' + algo_wd  +'_' +str(i)+'.job'
        job_name = 'job_submit_' + algo_wd +'_'+ str(i)
        function_name = 'spreading_simulation_20_'+city+'_SIR.py'
    
        submitJob(slurmFile_name, job_name, i+1, function_name,[algo_wd, i+1,city,target_ratio, spread_ratio, recover_rate,file_name_index])
        
        
print('done!')