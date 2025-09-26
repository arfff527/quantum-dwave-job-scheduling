
"""将结果转换成甘特图可视化"""
import matplotlib.pyplot as plt
import numpy as np
ax=plt.gca()
[ax.spines[i].set_visible(False) for i in ["top","right"]]

def draw_gantt(m,t):
    """甘特图
    m机器集
    t时间集
    """
    machine_start = {}
    for i in range(max(m)+1):
        machine_start[i] = 0

    for j in range(len(m)):#工序j
        i=m[j]-1 # 机器编号i
        if j==0:
            plt.barh(i,t[j]) # machine id, duration
            machine_start[i] += t[j]
           # plt.text(np.sum(t[:j+1])/8,i,'J%s T%s'%((j+1),t[j]),color="white",size=8)
        else:

            plt.barh(i,t[j],left=machine_start[i])
            machine_start[i] += t[j]
          #  plt.text(np.sum(t[:j])+t[j]/8,i,'J%s T%s'%((j+1),t[j]),color="white",size=8)


def solution_visualization(month_list,running_time, makespan, solution_list):
    job_num = len(solution_list)
    # draw gantt picture
    m = []
    t = []
    # print(solution_list)
    for i in range(job_num):
        m.append(solution_list[i][0])
        t.append(solution_list[i][1])

    draw_gantt(m, t)
    plt.yticks(np.arange(max(m)), np.arange(1, max(m) + 1))
    title = "month: " + str(month_list[0]) + " job num: " + str(job_num) + " makespan: " + str(
        int(makespan)) + " time:" + str(round((running_time), 2))
    plt.title(title, fontsize=12, color='r')
    plt.xlabel('total time/min')
    plt.ylabel('machine index')
    plt.savefig('month' + str(month_list) + '.png')
    plt.show()

"""测试代码"""
if __name__=="__main__":
    m = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    t = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    draw_gantt(m,t)
    plt.yticks(np.arange(max(m)),np.arange(1,max(m)+1))
    plt.show()