class ONet_fd():
    
    def __init__(self, file_position, fd):
        self.file_position = file_position
        self.fd = fd
        self.occupation_skill = {}
        self.skill_dict = {}## skill 的 id 是 key，对应的值是 skill 的名字
        self.skill_id_list = []
        self.occupation_list = []


 ## 读取文件时间       
    def fd_time(self):
        try:
            file = open(self.file_position + '/Readme.txt')
        except:
            file = open(self.file_position + '/Read Me.txt')
            
        cur_num = 0
        for line in file.readlines():
            if cur_num == 1:
                curline = line.strip().split(" ")
                self.network_time = [curline[0],curline[-2]]
                return
            
            cur_num += 1


## 读取skill.txt         
    def fd_skills(self):
        file = open(self.file_position + '/Skills.txt')
        cur_num = 0
        for line in file.readlines():
            if cur_num != 0:
                curline = line.strip().split("\t")

                if curline[0] not in self.occupation_skill.keys():
                    self.occupation_skill[curline[0]] = [[],[]]
                    self.occupation_list.append(curline[0])

                if curline[1] not in self.occupation_skill[curline[0]][0]:
                    self.occupation_skill[curline[0]][0].append(curline[1])
                    if curline[3].strip().upper() == 'IM':
                        self.occupation_skill[curline[0]][1].append(float(curline[4]))


                if curline[1] not in self.skill_id_list:
                    self.skill_id_list.append(curline[1])

                self.skill_dict[curline[1]] = curline[2]

            cur_num += 1

            
## 读取abilities.txt       
    def fd_abilities(self):
        try:
            file = open(self.file_position + '/abilities.txt')
        except:
            file = open(self.file_position + '/ability.txt')

        cur_num = 0
        for line in file.readlines():
            if cur_num != 0:
                curline = line.strip().split("\t")

                if curline[0] not in self.occupation_skill.keys():
                    self.occupation_skill[curline[0]] = [[],[]]
                    self.occupation_list.append(curline[0])

                if curline[1] not in self.occupation_skill[curline[0]][0]:
                    self.occupation_skill[curline[0]][0].append(curline[1])
                    if curline[3].strip().upper() == 'IM':
                        self.occupation_skill[curline[0]][1].append(float(curline[4]))


                if curline[1] not in self.skill_id_list:
                    self.skill_id_list.append(curline[1])

                self.skill_dict[curline[1]] = curline[2]

            cur_num += 1
        

## 读取knowledge.txt          
    def fd_knowledge(self):
        file = open(self.file_position + '/Knowledge.txt')
        cur_num = 0
        for line in file.readlines():
            if cur_num != 0:
                curline = line.strip().split("\t")

                if curline[0] not in self.occupation_skill.keys():
                    self.occupation_skill[curline[0]] = [[],[]]
                    self.occupation_list.append(curline[0])

                if curline[1] not in self.occupation_skill[curline[0]][0]:
                    self.occupation_skill[curline[0]][0].append(curline[1])
                    if curline[3].strip().upper() == 'IM':
                        self.occupation_skill[curline[0]][1].append(float(curline[4]))


                if curline[1] not in self.skill_id_list:
                    self.skill_id_list.append(curline[1])

                self.skill_dict[curline[1]] = curline[2]

            cur_num += 1