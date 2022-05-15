import numpy as np
import pandas as pd
import Machine
import Task
import Parameters
import Optimization
from Gantt_graph1 import Gantt1
from Reform_task import reform_task
class GA_main(object):
    def __init__(self):
        self

    def GA(self,information_network,task_set,machine_set):
        # 初始化参数
        parameters = Parameters.Parameters()
        max_generation, population_size, alpha, beta, gobal_best_fitness, length = parameters.parameter_setting()
        # 读取数据
        # print(task_set)
        # print(machine_set)
        print("数据读取完成")
        # print(task_set.shape[0])
        # 实例化子任务在能力包中的序号

        # 初始化种群
        optimization = Optimization.Optimization()
        task_set = reform_task(task_set)
        ini_population = optimization.initialization(population_size, task_set)
        # print(ini_population)
        # 开始迭代搜索
        gobal_best_fitness, gobal_best_individual = optimization.search_by_iteration(ini_population, max_generation,
                                                                                     task_set, machine_set, alpha, beta,
                                                                                     length, gobal_best_fitness,information_network)
        gobal_best_individual = np.array(gobal_best_individual)
        Gantt1(gobal_best_individual)
        return gobal_best_individual,machine_set,task_set


if __name__ == '__main__':
    ga=GA_main()
    machine = Machine.Machine()
    task = Task.Task()
    task_set = task.load_task(1, 1)
    # task_num = np.shape(task_set)[0]
    # temp = np.zeros([task_num, 1])
    # task_set1 = np.hstack((task_set, temp))
    machine_set = machine.load_machine(1, 1)
    machine_num = np.shape(machine_set)[0]
    information_network = np.ones([machine_num,machine_num])
    # for i in range(5,13):
    #     information_network[0][i] = 0
    #     #information_network[1][i] = 0
    #     #information_network[2][i] = 0

    zuiyougeti = ga.GA(information_network,task_set,machine_set)[0]
    print(zuiyougeti)

'''
    for i in range(5,13):
        information_network[0][i] = 0
        information_network[1][i] = 0
        information_network[2][i] = 0
'''

