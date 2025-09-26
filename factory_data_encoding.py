"""数据预处理，输入工单数据和UPH数据，输出job list"""
import os.path as osp
from collections import defaultdict

# 统计每一个订单需要多少UPH（一天）
def cal_uph_one_date(uph_path,date_job_sort,date):
    uph_dict = defaultdict(list)
    for i in date_job_sort[date]:
        uph_dict[i] = []
    for line in open(osp.join(uph_path),encoding="gbk"):
        a = line.strip('\n')
        content = a.split(',')
        if id not in content:
            if "NB12" in content:
                if content[1] in date_job_sort[date].keys() and "ASS" in content[2] and content[6] == "2":
                    machine_id = ord(content[2][-1])-65
                    machine_duration = (int(date_job_sort[date][content[1]]) / int(content[3]))*60 #UPH->MIN
                    uph_dict[content[1]].append((machine_id,machine_duration,int(date_job_sort[date][content[1]]) )) #machine order number,quantity/uph
    # 将空的零件先剔除掉
    del_list = []
    for i in uph_dict.keys():
        if len(uph_dict[i]) == 0:
            del_list.append(i)
    for i in del_list:
        uph_dict.pop(i)
    return uph_dict

# 统计每一个订单需要多少UPH （一月）
def cal_uph_one_month(month):
    order_path = "LCFC data/t_ml_assy_atb.csv"
    uph_path = "LCFC data/t_ml_line_uph.csv"
    order_result = []
    model_set = set()
    date_list = set()
    date_job_sort = defaultdict()
    # 提取月份的日期
    for line in open(osp.join(order_path), encoding="gbk"):
        a = line.strip('\n')
        content = a.split(',')
        if id not in content:
            if "NB12" in content:
                model_set.add(content[1])
                order_result.append([content[1], content[3], content[4]])
                date_list.add(content[4])

    for i in date_list:
        date_job_sort[i] = {}

    # 将JOB按天添加到月份中
    for i in date_list:
        for j in order_result:
            if i == j[-1]:
                if j[0] not in date_job_sort[i].keys():
                    date_job_sort[i][j[0]] = int(j[1])
                else:
                    date_job_sort[i][j[0]] = date_job_sort[i][j[0]] + int(j[1])
    date_belongto_month = []
    for i in date_job_sort.keys():
        if len(month) == 1:
            if i[5] == month and i[6] == "/":
                date_belongto_month.append(i)
        else:
            if i[5] == month[0] and i[6] == month[1]:
                date_belongto_month.append(i)
    month_uph_dict = defaultdict(list)
    for d in date_belongto_month:
        uph_dict = cal_uph_one_date(uph_path,date_job_sort, d)
        month_uph_dict[d] = uph_dict
    return month_uph_dict

month_uph_dict = cal_uph_one_month("11")


# 计算machine的分布，即一个JOB可以由几个产线执行。
"""distirbute_machine = [[0] for n in range(30)]
for i in uph_dict.keys():
    distirbute_machine[len(uph_dict[i])][0] = distirbute_machine[len(uph_dict[i])][0]+1
print(distirbute_machine)
print(sum(i[0] for i in distirbute_machine))"""

# 工单拆分
def order_divide(problem,problem_model):
    model_type = set() #model 集合
    for i in problem_model.keys():
        model_type.add(problem_model[i][-1])
    p = []
    for i in range(max(problem_model.keys())):
        p.append((problem_model[i][-1],problem[i][0][0],problem[i][0][1],problem[i][0][2]))
    combine_problem = defaultdict()
    for i in model_type:
        combine_problem[i] = 0
    for i in p:
        combine_problem[i[0]] += i[-1]
    divide_problem = {}
    divide_problem_model = {}
    index = 0
    for i in combine_problem.keys():
        if combine_problem[i]>150:
            flag = combine_problem[i]
            while flag > 150:
                divide_problem_model[index] = (150,i)
                index += 1
                flag -= 150
            divide_problem_model[index] = (flag,i)
            index += 1
        else:
            divide_problem_model[index] = (combine_problem[i],i)
            index += 1
    uph_path = "data_processing/t_ml_line_uph.csv"
    # 记录所有型号的UPH
    model_uph = defaultdict(list)
    for line in open(osp.join(uph_path),encoding="gbk"):
        a = line.strip('\n')
        content = a.split(',')
        if id not in content:
            if "NB12" in content:
                if content[1] in model_type and "ASS" in content[2] and content[6] == "2":
                    machine_id = ord(content[2][-1])-65
                    machine_uph = int(content[3]) #UPH
                    model_uph[content[1]].append((machine_id,machine_uph))

    for i in divide_problem_model.keys():
        quantity = divide_problem_model[i][0]
        model = divide_problem_model[i][1]
        available_machine_uph = []
        for machine,uph in model_uph[model]:
            duration = (quantity/uph)*60
            available_machine_uph.append((machine,duration,quantity))
        divide_problem[i] = available_machine_uph #machine,duration,quantity

    return divide_problem,divide_problem_model





