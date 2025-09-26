from qubo_building import *
from factory_data_encoding import *
from gantt_visualization import *
import time
from dwave_qbsolv import QBSolv
import hybrid

# qpu 求解器定义
def qpu_solver():
    workflow = hybrid.Loop(
        hybrid.RacingBranches(
        hybrid.InterruptableTabuSampler(),
        hybrid.EnergyImpactDecomposer(size=30, rolling=True, rolling_history=0.75)
        | hybrid.QPUSubproblemAutoEmbeddingSampler()
        | hybrid.SplatComposer()) | hybrid.ArgMin(), convergence=1)
    return hybrid.HybridSampler(workflow)

# 处理的月份
month_list = [9]
problem,problem_model = generate_factory_data(month_list) # MONTH: 6,7
problem,problem_model = order_divide(problem,problem_model)

# JOB的数量
job_num = max(problem.keys())+1

# 总机器数量 NB12 15条产线
machine_number = 15

# 创建QUBO
Q = getQuboMatrix(problem, machine_number)
start_time = time.time() # 时间函数，测试运行时间
# CPU求解器
response = QBSolv().sample_qubo(Q)
# QPU求解器
#response = qpu_solver().sample_qubo(Q) # DWAVE4000
result = list(response.samples())
result = result[0]
end_time = time.time()
running_time = start_time - end_time
print("computing time: ",running_time) #输出运行时间
print(validation(problem,machine_number,result)) # 验证有效解
matrix,makespan,solution_list,machine_list = decoding_result(problem,machine_number,result)
print("makespan: ",makespan)

# 绘制甘特图
solution_visualization(month_list,running_time, makespan, solution_list)

