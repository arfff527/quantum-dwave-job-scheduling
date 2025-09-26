"""为问题创建QUBO表达式"""
from collections import defaultdict
from factory_data_encoding import cal_uph_one_month, cal_uph_one_date
machine_number = 15 # 一个产区的产线数量
"""定义QUBO，两个约束 1.一个JOB只能在一个machine上运行一次 2.只能在特定机器运行此JOB
3.增加惩罚函数，减少运行的时间。公式：machine_welcome_factor*0.12+processing_time"""
def getQuboMatrix(problem,machine_number):
    job_num = max(problem.keys())+1 #JOB的总数量
    Q = {}
    # 初始化Q
    for i in range(0, job_num * machine_number):  # number of jobs * number of alternate machines
        for j in range(0, job_num * machine_number):
            Q.update({(i, j): 0})
    # 只能在特定机器运行此JOB
    lam = job_num*machine_number
    for i in range(0, job_num):
        machine_list_for_single_job = [m[0] for m in problem[i]] # 记录每一个JOB的可行machine
        for j in range(0, machine_number):
            if j not in machine_list_for_single_job:
                Q.update({(i * machine_number + j, i * machine_number + j): lam * 2})
    # 一个JOB只能在一个machine上运行一次
    for i in range(job_num):
        for j in range(machine_number):
            for k in range(j + 1, machine_number):
                Q.update({(i * machine_number + j, i * machine_number + k): lam * 2})
            Q.update({(i * machine_number + j, i * machine_number + j): (
                        Q[(i * machine_number + j, i * machine_number + j)] - lam)})
    # 增加惩罚函数，减少运行的时间。
    machine_welcome_factor = cal_welcome_factor(problem, machine_number)
    for i in range(0, job_num):
        machine_list_for_single_job = [m[0] for m in problem[i]] # 记录每一个JOB的可行machine
        for j in range(0, machine_number):
            if j in machine_list_for_single_job:
                processing_time = find_job_processing_time(problem,i,j)
                Q.update({(i * machine_number + j, i * machine_number + j):Q[(i * machine_number + j, i * machine_number + j)]+machine_welcome_factor[j]*0.12+processing_time})
    return Q

"""计算JOB的processing_time"""
def find_job_processing_time(problem,job_index,machine_index):
    for machine,process_time,quantity in problem[job_index]:
        if machine == machine_index:
            return process_time

def cal_welcome_factor(problem,machine_number):
    """分别计算 a. 欢迎度因子(machine)。机器的受欢迎程度 即 welcome_factor.
    b. 时间因子b1&b2(job&machine)。机器在此JOB上的执行时间以及机器可以开始的时间。
    c*. 此JOB可用的机器数(job) 暂不考虑 
    d*. 机器的效率，机器平均UPH  暂不考虑
    一共四个因子 
    欢迎度高-能量值高，减少被选。
    执行时间长-能量值高，减少被选。
    *开始时间晚-能量值高，减少被选"""
    job_num = max(problem.keys())+1
    machine_welcome_factor = {}
    for i in range(machine_number):
        machine_welcome_factor[i] = 0
    for i in range(job_num):
        for machine,process_time,quantity in problem[i]:
            machine_welcome_factor[machine]+=1
    return machine_welcome_factor

#print("machine_welcome_factor",machine_welcome_factor)

# decoding result
def decoding_result(problem,machine_number,result):
    job_num = max(problem.keys())+1
    matrix = [] #记录解的matrix
    machine_list = {}
    solution_list = {} # {[job id]:(machine_num,duration)...}
    for i in range(machine_number):
        machine_list[i] = 0
    for i in range(job_num):
        l = []
        for j in range(machine_number):
            l.append(result[i*machine_number+j])
            if result[i*machine_number+j] == 1:
                for index in problem[i]:
                    if index[0] == j:
                        processing_time = index[1]
                        machine_list[j] += processing_time
                solution_list[i] = (j, processing_time)
        matrix.append(l)
    #for i in matrix:
        #print(i)
    #print("machine_list",machine_list)
    makespan = max(machine_list.values())
    return matrix,makespan,solution_list,machine_list

"""validation 验证解是否有效 """
def validation(problem,machine_number,result):
    job_num = max(problem.keys())+1
    for i in range(job_num):
        machine_list_for_single_job = [m[0] for m in problem[i]]
        l = []
        for j in range(machine_number):
            l.append(result[i * machine_number + j])
            if result[i * machine_number + j] == 1:
                if j not in machine_list_for_single_job: # 如果执行JOB的机器不在可运行的机器列表中，返回FALSE
                    print("Invalid solution: Job",i," cannot running on machine",j)
                    return False
        if sum(l)!=1:  # 如果一个JOB没有被执行一次，返回FALSE
            print("Invalid solution: Job", i, "only could be processed for 1 time")
            return False
    print("-----------------------Congratulations! Valid solution!--------------------------")
    return True

def generate_factory_data(monthlist):
    problem = defaultdict()
    job_num = 0
    problem_model = {}  # 存储每一个JOB的日期还有型号
    for i in monthlist:
        month_uph_dict = cal_uph_one_month(str(i))
        for i in month_uph_dict.keys():
            for j in month_uph_dict[i].keys():
                problem[job_num] = month_uph_dict[i][j]
                problem_model[job_num] = (i, j)
                job_num += 1
    return problem,problem_model