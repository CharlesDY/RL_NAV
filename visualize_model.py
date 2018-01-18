import numpy as np
import os
import csv
import time
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot,savefig
from matplotlib.pyplot import cm

import pandas as pd

'''''
这里是把训练数据的十个模型与真值做差，看看哪个模型比较好
'''''
Data = np.zeros((5,18,548,421,10))
TruthData = np.zeros((5,18,548,421))

X = 548
Y = 421
DATE = 5
HOUR = 18
MODULE = 10


def load_data(filePath,tfilePath):
    with open(filePath,newline='') as csvfile:
        testreader = csv.reader(csvfile)
        row_num = 0

        for row in testreader:
            row_num = row_num + 1
            if row_num == 1:
                continue
            x_id = int(row[-6])-1
            y_id = int(row[-5])-1
            date = int(row[-4])-3
            hour = int(row[-3])-3
            mode = int(row[-2])-1
            wind = float(row[-1])

            Data[date][hour][x_id][y_id][mode] = wind
    
    with open(tfilePath,newline='') as csvfile:
        testreader = csv.reader(csvfile)
        row_num = 0

        for row in testreader:
            row_num = row_num + 1
            if row_num == 1:
                continue
            x_id = int(row[-5])-1
            y_id = int(row[-4])-1
            date = int(row[-3])-3
            hour = int(row[-2])-3
            wind = float(row[-1])

            TruthData[date][hour][x_id][y_id] = wind

def drawDifference(filePath,tfilePath):
    Data = pd.read_csv(filePath)
    Data = Data['wind'].values.reshape((DATE,HOUR,X,Y))
    # x => m
    #Data = np.swapaxes(Data,2,4)
    # x => y
    #Data = np.swapaxes(Data,3,4)
    TruthData = pd.read_csv(tfilePath)
    TruthData = TruthData['wind'].values.reshape((DATE,HOUR,X,Y))

    print('read done')
    
    differ = np.zeros((X,Y))

    for d in range(DATE):
        for h in range(HOUR):
            '''AVG = np.zeros((X,Y))
            for m in range(MODULE):
                AVG = AVG + Data[d][h][m]
                differ = Data[d][h][m] - TruthData[d][h]
                plt.imsave(arr = differ,cmap='gray',fname = '../data/modelPic/'+str(d)+'_'+str(h)+'_'+str(m)+'.png',format = 'png',origin = 'lower')
                plt.imsave(arr = Data[d][h][m],cmap='gray',fname = '../data/modelPic/'+str(d)+'_'+str(h)+'_'+str(m)+'_t' + '.png',format = 'png',origin = 'lower')
                print('pic '+str(d)+'_'+str(h)+'_'+str(m)+'.png'+' saved')
            AVG = AVG / MODULE'''
            arr = np.zeros((X,Y))
            arr = Data[d][h]
            plt.imsave(arr = arr,cmap='gray',fname = '../data/modelPic/'+str(d)+'_'+str(h)+'_avg'+'.png',format = 'png',origin = 'lower')
            lm = (1 + (TruthData[d][h] >= 1) - (arr >= 1)) * 10
            plt.imsave(arr = lm,cmap='gray',fname = '../data/modelPic/'+str(d)+'_'+str(h)+'_lm'+'.png',format = 'png',origin = 'lower')
            plt.imsave(arr = (arr >= 1),cmap='gray',fname = '../data/modelPic/'+str(d)+'_'+str(h)+'_avg_b'+'.png',format = 'png',origin = 'lower')
            
            diff = np.zeros((X,Y))
            s_diff = 0
            for x in range(X):
                for y in range(Y):
                    if TruthData[d][h][x][y] > 0.7 and Data[d][h][x][y] < 0.7:
                        diff[x][y] = 1
                        s_diff = s_diff + 1
            print("S_Diff = %d"%s_diff)
            plt.imsave(arr = diff,cmap='gray',fname = '../data/modelPic/'+str(d)+'_'+str(h)+'_diff'+'.png',format = 'png',origin = 'lower')
            s = sum(sum(abs(TruthData[d][h]-Data[d][h])))

            print("Sum  = %d"%s)

def draw_true(tfilePath):
    TruthData = pd.read_csv(tfilePath)
    TruthData = TruthData['wind'].values.reshape((DATE,HOUR,X,Y))
    for d in range(DATE):
        for h in range(HOUR):
            plt.imsave(arr = TruthData[d][h],cmap='gray',fname = '../data/modelPic/'+str(d)+'_'+str(h)+'.png',format = 'png',origin = 'lower')
            plt.imsave(arr = (TruthData[d][h] >= 1),cmap='gray',fname = '../data/modelPic/'+str(d)+'_'+str(h)+ '_b' +'.png',format = 'png',origin = 'lower')

tfilePath = '../data/In_situMeasurementforTraining_201712.csv'
filePath = '../data/result/pred_train.csv'


if __name__ == '__main__':
    print(filePath)
    drawDifference(filePath,tfilePath)
    draw_true(tfilePath)