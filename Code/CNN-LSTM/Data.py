import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import torch 
from torch import nn
from torch.autograd import Variable
import os


path = os.getcwd()
dir = os.listdir(path + '/modelData')
datalist = []
for i in dir:
    datalist.append(i)
datalist = sorted(datalist, key=lambda x: int(x[3:5]))

def nor(str):
    max = np.max(str)
    min = np.min(str)
    str = (str - min) / (max - min)
    return str, max, min

def create_average(voltage, current, speed, length):
    Vavg, Iavg, Uavg = [], [], []
    for i in range(len(voltage)):
        if i < length:
            Vavg.append(np.mean(voltage[:i+1]))
            Iavg.append(np.mean(current[:i+1]))
            Uavg.append(np.mean(speed[:i+1]))
        else:
            Vavg.append(np.mean(voltage[i-(length-1):i+1]))
            Iavg.append(np.mean(current[i-(length-1):i+1]))
            Uavg.append(np.mean(speed[i-(length-1):i+1]))
    return np.array(Vavg), np.array(Iavg), np.array(Uavg)
 
def create_newData(filename):
    data_csv = pd.read_csv(path + '/modelData/' + filename)
    SoC = list(data_csv.values[:,1])
    speed = list(data_csv.values[:,5])
    voltage = list(data_csv.values[:,4])
    current = list(data_csv.values[:,3])
    temperature = list(data_csv.values[:,2])
    SoC, SoC_max, SoC_min = nor(SoC)
    voltage, v_max, v_min = nor(voltage)
    current, c_max, c_min = nor(current)
    temperature, t_max, t_min = nor(temperature)
    speed, s_max, s_min = nor(speed)

    Vavg, Iavg, Uavg = create_average(voltage, current, speed, 50)

    data = np.vstack((SoC, voltage, current, temperature, speed, Vavg, Iavg, Uavg)).T
    df = pd.DataFrame(data, columns=['SoC','Voltage', 'Current', 'Temperature', 'Speed', 'Vavg', 'Iavg', 'Uavg'], dtype='double')
    df.to_csv(path + '/newModelData/' + 'SoC' + filename[3:5] + '.csv', index=False)

def get_data():
    for i in datalist:
        create_newData(i)
    print('done')


