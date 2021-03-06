import numpy as np
import pandas as pd
import Machine
import Task
import time
import Parameters
import Optimization
from Gantt_graph import Gantt
from Reform_task import reform_task
from Instantiate_task import instantiate_task
from State_transform import state_transform
import Scheduling
from numpy.lib.function_base import _quantile_dispatcher
# from thop import profile

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
# import gym
from matplotlib import pyplot as plt
import sys
import Nature_DQN
from Gantt_graph import Gantt

class DQN_main(object):
    def __init__(self):
        self

    def DQN(self,information_network,task_set,machine_set):
        scheduling = Scheduling.Scheudling()
        # machine = Machine.Machine()
        # task = Task.Task()
        # task_set = task.load_task(1, 1)
        # machine_set = machine.load_machine(1, 1)
        machine_num = np.shape(machine_set)[0]
        task_num = np.shape(task_set)[0]
        temp = np.zeros([task_num, 1])
        task_set = np.hstack((task_set, temp))
        state_num = np.shape(task_set)[1]
        dqn = Nature_DQN.DQN(state_num, task_num)
        dqn.eval_net.load_state_dict(torch.load('./model_dic/nn_2000.pth'))
        dqn.eval_net.eval()
        # task_set = reform_task(task_set)
        # task_set = instantiate_task(task_set)
        for parameters in dqn.eval_net.parameters():
            print(parameters)
        # print(dqn.parameters())
        N_ACTIONS = task_num
        N_STATES = state_num
        BATCH_SIZE = 16
        Epoch = 1
        MEMORY_CAPACITY = 40
        CountOpers = np.zeros(N_ACTIONS)
        PopCountOpers = []
        #    dqn = DQN(N_STATES, N_ACTIONS)
        total_fitness = np.zeros(Epoch)
        s = task_set
        s_ = task_set
        task_size = np.shape(task_set)[0]
        task_set = reform_task(task_set)

        print('\nCollecting experience...')
        for i_episode in range(0, Epoch):
            action_choosen = np.zeros((1, task_num))
            processor = np.zeros([int(task_set[task_size - 1][1]), 3])  # ??????????????????????????????????????????????????????????????????=???????????????
            # total_fitness[i_episode] = 0
            for t in range(N_ACTIONS):
                t_start = time.time()
                a = dqn.choose_action(s)
                a = int(a)
                # print(t)
                # qianxu_neibubianhao = task_set[a][2]
                while action_choosen[0][a] == 1:
                    a = np.random.randint(0, task_num)
                # 0:id  1:???????????????  2:????????????  3:?????????????????????????????????  4:????????????  5:???????????? 6:????????????
                # darenwu_a = np.int(task_set[a][1]) #??????a??????????????????
                # qianxurenwu =np.int(processor[np.int(darenwu_a-1)][0])
                # if np.int(task_set[qianxurenwu-1][2]+1) != np.int(task_set[a][2]):
                #     a = np.int(task_set[qianxurenwu+1-1-1][0]-1)
                # if task_set[qianxurenwu-1][2]+1 != task_set[a][2] and qianxurenwu != 0:
                #     a = np.random.randint(1, task_num+1)
                # if qianxurenwu == 0:
                #     a = np.random.randint(1, task_num+1)
                # print("action:"+str(a))
                action_choosen[0][a] = 1

                s_ = state_transform(s, s_, a)
                information_network = np.ones([machine_num, machine_num])

                temp_a = a + 1

                action = np.reshape(temp_a, (-1, 1))

                if t == 0:
                    scheduling_result, temp_machine_set, processor = scheduling.arrange_task_to_machine_RL(action,
                                                                                                           task_set,
                                                                                                           machine_set,
                                                                                                           information_network,
                                                                                                           processor)
                    lie = np.shape(scheduling_result[0])[1]
                    temp_result = np.reshape(scheduling_result[0][0, :], (-1, lie))
                    temp_result = np.array(temp_result, dtype='int64')
                    temp_schedualing_result = np.zeros([1, lie])
                    for b in range(lie):
                        temp_schedualing_result[0][b] = int(temp_result[0][b])
                if t > 0:
                    scheduling_result, temp_machine_set, processor = scheduling.arrange_task_to_machine_RL(action,
                                                                                                           task_set,
                                                                                                           temp_machine_set,
                                                                                                           information_network,
                                                                                                           processor)
                    if scheduling_result[0][0, 0] != 0:
                        lie = np.shape(scheduling_result[0])[1]
                        temp_result = np.reshape(scheduling_result[0][0, :], (-1, lie))
                        temp_result = np.array(temp_result, dtype='int64')

                        # temp_schedualing_result = temp_result
                        # for b in range(lie):
                        #     temp_schedualing_result[0][b] = np.int(temp_result[0][b])
                        temp_schedualing_result = np.vstack((temp_schedualing_result, temp_result))
                        temp_schedualing_result = np.array(temp_schedualing_result, dtype='int64')
                fitness = scheduling.fitness_calculation_RL(scheduling_result, action)

                r = fitness[0]
                total_fitness[i_episode] = total_fitness[i_episode] + r
                # s = s.flatten()
                s_temp = s_.flatten()
                dqn.store_transition(s.flatten(), a, r, s_temp)
                if dqn.memory_counter > 50:
                    dqn.learn(BATCH_SIZE)
                CountOpers[a] += 1
                if i_episode % 5 == 0:
                    # print(i_episode, ' ', a)
                    PopCountOpers.append(CountOpers)
                    CountOpers = np.zeros(N_ACTIONS)
                s = s_

            # print(temp_schedualing_result)
            t_end = time.time()
            #print("?????????{}s".format(t_end - t_start))
        Gantt(temp_schedualing_result)
        return temp_schedualing_result,machine_set,task_set


if __name__ == '__main__':
    dqn = DQN_main()
    machine = Machine.Machine()
    task = Task.Task()
    task_set = task.load_task(1, 1)
    machine_set = machine.load_machine(1, 1)
    machine_num = np.shape(machine_set)[0]
    information_network = np.ones([machine_num,machine_num])
    # for i in range(5,13):
    #     information_network[0][i] = 0
    #     #information_network[1][i] = 0
    #     #information_network[2][i] = 0

    zuiyougeti = dqn.DQN(information_network,task_set,machine_set)[0]
    print(zuiyougeti)

'''
    for i in range(5,13):
        information_network[0][i] = 0
        information_network[1][i] = 0
        information_network[2][i] = 0
'''

