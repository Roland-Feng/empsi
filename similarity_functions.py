## 相似性函数
import networkx as nx
import numpy as np

def similarity_calculate(o_skill,job1,job2,TS = 0.0):
    skill_temp = []
    importance1 = [] ## 仅存在于job1的skill的值
    importance2 = [] ## 仅存在于job2的skill的值
    importance_diff = [] ## 记录job1和job2的共同skill的区别
    
    ## 只统计 job1 和 job2 都有的 skill 
    for i in range(0,len(o_skill[job1][0])):
        s = o_skill[job1][0][i]
        if s in o_skill[job2][0]:
            j = o_skill[job2][0].index(s)
            skill_temp.append(s)
            importance_diff.append(o_skill[job1][1][i] - o_skill[job2][1][j])
            
    if len(skill_temp) == 0:
        return False
    
    for i in range(0,len(o_skill[job1][0])):
        s = o_skill[job1][0][i]
        if s not in skill_temp:
            importance1.append(o_skill[job1][1][i])
            
    for j in range(0,len(o_skill[job2][0])):
        s = o_skill[job2][0][j]
        if s not in skill_temp:
            importance2.append(o_skill[job2][1][j])
            
    norm_d = np.linalg.norm(np.array(importance_diff))
    norm_1 = np.linalg.norm(np.array(importance1))
    norm_2 = np.linalg.norm(np.array(importance2))
            
    similarity = 1/(1 + pow(norm_d,2) + pow(norm_1,2) + pow(norm_2,2))
    
    if similarity >= TS:
        return True
    
    return False


def get_rca(o_skill, job, skill):
    temp1 = sum(o_skill[job][1])
    temp2 = 0
    temp3 = 0
    for j in o_skill.keys():
        if skill in o_skill[j][0]:
            i = o_skill[j][0].index(skill)
            temp2 += o_skill[j][1][i]
            temp3 += sum(o_skill[j][1])

    
    if skill in o_skill[job][0]:
        i = o_skill[job][0].index(skill)
        temp = o_skill[job][1][i]
        
    rca = (temp/temp1)/(temp2/temp3)
    
    return rca
        
    
    
    
def rca_similarity(j_rca, job1, job2):
    
    d = np.linalg.norm(np.array(j_rca[job1]) - np.array(j_rca[job2]))
    
    return 1/(1+d)


