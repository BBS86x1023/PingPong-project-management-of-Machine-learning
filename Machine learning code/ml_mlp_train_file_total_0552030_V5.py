##特徵從八個變成6個
from mlp_model import models
import numpy as np
import pandas as pd
from mlp_model.layers import Neurons
from mlp_model.activations import Sigmoid, Relu, Linear
from mlp_model.losses import Logloss, MSE, Quantile

import random
import pickle
import os
import matplotlib.pyplot as plt

print("---------------------------------------------")
print("---- 1P Regression model -----------------------")
print("---------------------------------------------")
# REGRESSION
# Creating synthetic dataset
##-------------------------------------------------------------------------------------------------------##
# 定義 data 與 label
f=[]
#data_list 是放檔案裡的所有資料
data_list=[]
# n 指的是有多少個檔案
n = 0
## log_path 的變數，主要是檔案讀取位置
log_path="games\\pingpong\\log_1P\\"
for filename in os.listdir(log_path):
    with open(log_path+filename,'rb') as fi:
        f.append(fi)
        data_listi=pickle.load(fi)
        data_list.append(data_listi)
    n = n + 1
#-----len(data_list) 多少檔案匯入
print(len(data_list))
##-------------------------------------------------------------------------------------------------------##
# save each info separetely
## 宣告要讀取的資料
## Frame : 影像幀數 ，  Status : 目前遊戲狀態 ， Ballposition : 球(x,y)座標的位置
## PlatformPosition_1P : 平台玩家1P(x,y)的座標位置 ， PlatformPosition_2P : 平台玩家2P(x,y)的座標位置
## Ball_speed : 球移動速度
Frame=[]
Status=[]
Ballposition=[]
PlatformPosition_1P=[]
PlatformPosition_2P=[]
Ball_speed=[]
##把data_list裡的資料取出
for n in range(0,n-1):
    for i in range(0,len(data_list[n])):
        Frame.append(data_list[n][i].frame)
        Status.append(data_list[n][i].status)
        Ballposition.append(data_list[n][i].ball)
        Ball_speed.append(data_list[n][i].ball_speed)
        PlatformPosition_1P.append(data_list[n][i].platform_1P)
        PlatformPosition_2P.append(data_list[n][i].platform_2P)
#__________________________________________________________________________________________________________
##-------------------------------------------------------------------------------------------------------##
#開始把資料做分析
#把我們要的特徵與標籤定義好
#特徵主要是 : 球(x,y)座標、平台玩家1P(x,y)的座標位置、平台玩家2P(x,y)的座標位置、球的x移動量、球的y移動量
#標籤：平台玩家1P x座標的移動量，往右是 1、往左是-1、不動是0

PlatX_plus_20 = []
##-------------------------------------------------------------------------------------------------------##
##把list的資料型態轉成numpy陣列的資料型態
PlatformPosition_1P = np.array(PlatformPosition_1P)
PlatformPosition_2P = np.array(PlatformPosition_2P)
##-------------------------------------------------------------------------------------------------------##
## 70行目前不需要，放著或刪除並不影響整體程式
Ball_speed = np.array(Ball_speed)[:,np.newaxis]
## 以下兩行，只是看有多少列的資料
print(len(PlatformPosition_1P))
print(len(PlatformPosition_2P))
##-------------------------------------------------------------------------------------------------------##
##1P平台的原點往右移20個像素點 PlatformPosition_1P的x座標 往右移20個像素點
##2P平台的原點往右移20個像素點 PlatformPosition_2P的x座標 往右移20個像素點
##2P平台的原點往下移30個像素點 PlatformPosition_2P的y座標 往下移30個像素點
for i in range(0,len(PlatformPosition_1P)):
    PlatformPosition_1P[i][0] = PlatformPosition_1P[i][0] + 20
    PlatformPosition_2P[i][0] = PlatformPosition_2P[i][0] + 20
    PlatformPosition_2P[i][1] = PlatformPosition_2P[i][1] + 30 
##-------------------------------------------------------------------------------------------------------##
## PlatX_1P_next 目前平台1P的x座標
## PlatformPosition_1P[1:,0][:,np.newaxis] 把一維的列陣列轉換為二維的行陣列
PlatX_1P_next = PlatformPosition_1P[1:,0][:,np.newaxis]
## (目前平台1P的x座標) - (上一個平台1P的x座標) = 平台1P的移動量
## 把一維的列陣列轉換為二維的行陣列
## 除5，主要是因為移動量為5或-5，所以定義標籤1為往右和-1往左，0則不動
instruct = (PlatX_1P_next - (PlatformPosition_1P[0:len(PlatformPosition_1P)-1,0][:,np.newaxis]))/5
##-------------------------------------------------------------------------------------------------------##
##球變化量與球移動方向
##上一個球x座標從一維的列陣列轉換為二維的行陣列
BallX_position = np.array(Ballposition)[:,0][:,np.newaxis]
BallX_position_next = BallX_position[1:,:]
##(目前球x座標) - (上一個球x座標) = 球x座標變化量
Ball_Vx = BallX_position_next - BallX_position[0:len(BallX_position_next),0][:,np.newaxis]
##上一個球y座標從一維的列陣列轉換為二維的行陣列
BallY_position = np.array(Ballposition)[:,1][:,np.newaxis]
BallY_position_next = BallY_position[1:,:]
##(目前球y座標) - (上一個球y座標) = 球y座標變化量
Ball_Vy = BallY_position_next - BallY_position[0:len(BallY_position_next),0][:,np.newaxis]
##-------------------------------------------------------------------------------------------------------##
##列的資料數量必須是相同的
##所以底下4行主要是把列資料數量與球的x、y的變化量的列資料數量必須相同
PlatformPosition_1P = PlatformPosition_1P[0:len(PlatformPosition_1P)-1,:]
PlatformPosition_2P = PlatformPosition_2P[0:len(PlatformPosition_2P)-1,:]
Ball_speed = Ball_speed[0:len(Ball_speed)-1]
Ballarray=np.array(Ballposition[:-1])
##-------------------------------------------------------------------------------------------------------##
#Select some features to make x #Select instructions as y
#資料(輸入特徵) Ballarray,PlatformPosition_1P,PlatformPosition_2P,Ball_Vx,Ball_Vy
#標籤(輸出結果)
data = np.hstack((Ballarray,PlatformPosition_1P,Ball_Vx,Ball_Vy,instruct))
##-------------------------------------------------------------------------------------------------------##
##資料打亂是為了讓多層神經網路在學習結果更好
##資料打亂
np.random.shuffle(data)
##-------------------------------------------------------------------------------------------------------##
##暫存資料x與y，主要是給後面的train_data_x和train_data_y 好讓資料切割成train與test兩種資料
buffer_data_y = []
buffer_data_x = []
##-------------------------------------------------------------------------------------------------------##
## 資料切割
##從data資料裡分出"特徵"與"標籤"
for i in range(len(data)):
    buffer_data_y.append(data[i][6])
    buffer_data_x.append(data[i][0:6])
buffer_data_y = np.array(buffer_data_y)[:,np.newaxis]
buffer_data_x = np.array(buffer_data_x)
##-------------------------------------------------------------------------------------------------------##
## percentage 為切割百分比，目前是80%
###example : percentage = 60
###train_data_x 從 data 資料分出百分之60%到訓練x裡，其餘40%到測試x裡。
###------------------------------------------------------------------###
percentage = 80
train_data_x = buffer_data_x[:int((len(buffer_data_x))*percentage/100)]
train_data_y = buffer_data_y[:int((len(buffer_data_y))*percentage/100)]
test_data_x = buffer_data_x[int((len(buffer_data_x))*percentage/100):]
test_data_y = buffer_data_y[int((len(buffer_data_y))*percentage/100):]
###------------------------------------------------------------------###
#__________________________________________________________________________________________________________
##-------------------------------------------------------------------------------------------------------##
###開始準備要訓練多層神經網路
##先定義要幾層神經網路與幾個神經元
## Neurons : 神經層
## units : 神經元
## activation : 激勵函數
## input_dim : 特徵數量
# Instantiating model object
model = models.BasicMLP()
## 第一層有50個神經元以及8組特徵，激勵函數使用 X>0。 (輸入層)
model.add(Neurons(units=50, activation=Relu(), input_dim=train_data_x.shape[1]))
## 第二層有30個神經元，激勵函數使用 X>0。
model.add(Neurons(units=50, activation=Relu()))
## 第三層有15個神經元，激勵函數使用 X>0。
model.add(Neurons(units=50, activation=Relu()))
## 第四層有5個神經元，激勵函數使用 X>0。
model.add(Neurons(units=50, activation=Relu()))
## 第五層有5個神經元，激勵函數使用 X>0。
model.add(Neurons(units=50, activation=Relu()))
model.add(Neurons(units=50, activation=Relu()))
model.add(Neurons(units=50, activation=Relu()))
## 第六層有1個神經元，激勵函數使用 X>0。 (輸出層)
model.add(Neurons(units=1, activation=Linear()))
##-------------------------------------------------------------------------------------------------------##
# Model train
## params : 參數
## learning_rate : 學習率
## n_epoch : 迭代次數
## print_rate : 每迭代100次，印出到終端介面
params = {"learning_rate": 0.0001, "n_epoch": 1000, "print_rate": 100}
## MSE : 均方誤差
loss = MSE()
## 印出多層神經網路架構
print(model.layers)
# 開始訓練
model.train(loss, train_data=[train_data_x, train_data_y], params=params)
##-------------------------------------------------------------------------------------------------------##
## 測試神經網路是否成功能預測結果
# Run predict on new data
predictions = model.predict(test_data_x)

# Evaluate model performance using the same metric it used to train
performance = loss.forward(predictions, test_data_y)
print(f"Prediction loss: {performance.mean()}")
print(predictions)
##-------------------------------------------------------------------------------------------------------##
## 把訓練好的model存成.sav檔
filename1="C:\\Users\\BBS\\Desktop\\Machin leaning final project\
\\game\\MLGame-master\\games\\pingpong\\ml\\mlp_model_1P_0552030_V5.sav"
pickle.dump(model, open(filename1, 'wb'))
##-------------------------------------------------------------------------------------------------------##


print("---------------------------------------------")
print("---- 2P Regression model -----------------------")
print("---------------------------------------------")
# REGRESSION
# Creating synthetic dataset
##-------------------------------------------------------------------------------------------------------##
# 定義 data 與 label
f=[]
#data_list 是放檔案裡的所有資料
data_list=[]
# n 指的是有多少個檔案
n = 0
## log_path 的變數，主要是檔案讀取位置
log_path="games\\pingpong\\log_2P\\"
for filename in os.listdir(log_path):
    with open(log_path+filename,'rb') as fi:
        f.append(fi)
        data_listi=pickle.load(fi)
        data_list.append(data_listi)
    n = n + 1
#-----len(data_list) 多少檔案匯入
print(len(data_list))
##-------------------------------------------------------------------------------------------------------##
# save each info separetely
## 宣告要讀取的資料
## Frame : 影像幀數 ，  Status : 目前遊戲狀態 ， Ballposition : 球(x,y)座標的位置
## PlatformPosition_1P : 平台玩家1P(x,y)的座標位置 ， PlatformPosition_2P : 平台玩家2P(x,y)的座標位置
## Ball_speed : 球移動速度
Frame=[]
Status=[]
Ballposition=[]
PlatformPosition_1P=[]
PlatformPosition_2P=[]
Ball_speed=[]
##把data_list裡的資料取出
for n in range(0,n-1):
    for i in range(0,len(data_list[n])):
        Frame.append(data_list[n][i].frame)
        Status.append(data_list[n][i].status)
        Ballposition.append(data_list[n][i].ball)
        Ball_speed.append(data_list[n][i].ball_speed)
        PlatformPosition_1P.append(data_list[n][i].platform_1P)
        PlatformPosition_2P.append(data_list[n][i].platform_2P)
#__________________________________________________________________________________________________________
##-------------------------------------------------------------------------------------------------------##
#開始把資料做分析
#把我們要的特徵與標籤定義好
#特徵主要是 : 球(x,y)座標、平台玩家1P(x,y)的座標位置、平台玩家2P(x,y)的座標位置、球的x移動量、球的y移動量
#標籤：平台玩家2P x座標的移動量，往右是 1、往左是-1、不動是0

PlatX_plus_20 = []
##-------------------------------------------------------------------------------------------------------##
##把list的資料型態轉成numpy陣列的資料型態
PlatformPosition_1P = np.array(PlatformPosition_1P)
PlatformPosition_2P = np.array(PlatformPosition_2P)
##-------------------------------------------------------------------------------------------------------##
## 70行目前不需要，放著或刪除並不影響整體程式
Ball_speed = np.array(Ball_speed)[:,np.newaxis]
## 以下兩行，只是看有多少列的資料
print(len(PlatformPosition_1P))
print(len(PlatformPosition_2P))
##-------------------------------------------------------------------------------------------------------##
##1P平台的原點往右移20個像素點 PlatformPosition_1P的x座標 往右移20個像素點
##2P平台的原點往右移20個像素點 PlatformPosition_2P的x座標 往右移20個像素點
##2P平台的原點往下移30個像素點 PlatformPosition_2P的y座標 往下移30個像素點
for i in range(0,len(PlatformPosition_1P)):
    PlatformPosition_1P[i][0] = PlatformPosition_1P[i][0] + 20
    PlatformPosition_2P[i][0] = PlatformPosition_2P[i][0] + 20
    PlatformPosition_2P[i][1] = PlatformPosition_2P[i][1] + 30 
##-------------------------------------------------------------------------------------------------------##
## PlatX_2P_next 目前平台2P的x座標
## PlatformPosition_2P[1:,0][:,np.newaxis] 把一維的列陣列轉換為二維的行陣列
PlatX_2P_next = PlatformPosition_2P[1:,0][:,np.newaxis]
## (目前平台2P的x座標) - (上一個平台2P的x座標) = 平台2P的移動量
## 把一維的列陣列轉換為二維的行陣列
## 除5，主要是因為移動量為5或-5，所以定義標籤1為往右和-1往左，0則不動
instruct = (PlatX_2P_next - (PlatformPosition_2P[0:len(PlatformPosition_2P)-1,0][:,np.newaxis]))/5
##-------------------------------------------------------------------------------------------------------##
##球變化量與球移動方向
##上一個球x座標從一維的列陣列轉換為二維的行陣列
BallX_position = np.array(Ballposition)[:,0][:,np.newaxis]
BallX_position_next = BallX_position[1:,:]
##(目前球x座標) - (上一個球x座標) = 球x座標變化量
Ball_Vx = BallX_position_next - BallX_position[0:len(BallX_position_next),0][:,np.newaxis]
##上一個球y座標從一維的列陣列轉換為二維的行陣列
BallY_position = np.array(Ballposition)[:,1][:,np.newaxis]
BallY_position_next = BallY_position[1:,:]
##(目前球y座標) - (上一個球y座標) = 球y座標變化量
Ball_Vy = BallY_position_next - BallY_position[0:len(BallY_position_next),0][:,np.newaxis]
##-------------------------------------------------------------------------------------------------------##
##列的資料數量必須是相同的
##所以底下4行主要是把列資料數量與球的x、y的變化量的列資料數量必須相同
PlatformPosition_2P = PlatformPosition_2P[0:len(PlatformPosition_2P)-1,:]
PlatformPosition_1P = PlatformPosition_1P[0:len(PlatformPosition_1P)-1,:]
Ball_speed = Ball_speed[0:len(Ball_speed)-1]
Ballarray=np.array(Ballposition[:-1])
##-------------------------------------------------------------------------------------------------------##
#Select some features to make x #Select instructions as y
#資料(輸入特徵) Ballarray,PlatformPosition_1P,PlatformPosition_2P,Ball_Vx,Ball_Vy
#標籤(輸出結果) instruct
data = np.hstack((Ballarray,PlatformPosition_2P,Ball_Vx,Ball_Vy,instruct))
##-------------------------------------------------------------------------------------------------------##
##資料打亂是為了讓多層神經網路在學習結果更好
##資料打亂
np.random.shuffle(data)
##-------------------------------------------------------------------------------------------------------##
##暫存資料x與y，主要是給後面的train_data_x和train_data_y 好讓資料切割成train與test兩種資料
buffer_data_y = []
buffer_data_x = []
##-------------------------------------------------------------------------------------------------------##
## 資料切割
##從data資料裡分出"特徵"與"標籤"
for i in range(len(data)):
    buffer_data_y.append(data[i][6])
    buffer_data_x.append(data[i][0:6])
buffer_data_y = np.array(buffer_data_y)[:,np.newaxis]
buffer_data_x = np.array(buffer_data_x)
##-------------------------------------------------------------------------------------------------------##
## percentage 為切割百分比，目前是80%
###example : percentage = 60
###train_data_x 從 data 資料分出百分之60%到訓練x裡，其餘40%到測試x裡。
###------------------------------------------------------------------###
percentage = 80
train_data_x = buffer_data_x[:int((len(buffer_data_x))*percentage/100)]
train_data_y = buffer_data_y[:int((len(buffer_data_y))*percentage/100)]
test_data_x = buffer_data_x[int((len(buffer_data_x))*percentage/100):]
test_data_y = buffer_data_y[int((len(buffer_data_y))*percentage/100):]
###------------------------------------------------------------------###
#__________________________________________________________________________________________________________
##-------------------------------------------------------------------------------------------------------##
###開始準備要訓練多層神經網路
##先定義要幾層神經網路與幾個神經元
## Neurons : 神經層
## units : 神經元
## activation : 激勵函數
## input_dim : 特徵數量
# Instantiating model object
model = models.BasicMLP()
## 第一層有50個神經元以及8組特徵，激勵函數使用 X>0。 (輸入層)
model.add(Neurons(units=50, activation=Relu(), input_dim=train_data_x.shape[1]))
## 第二層有30個神經元，激勵函數使用 X>0。
model.add(Neurons(units=50, activation=Relu()))
## 第三層有15個神經元，激勵函數使用 X>0。
model.add(Neurons(units=50, activation=Relu()))
## 第四層有5個神經元，激勵函數使用 X>0。
model.add(Neurons(units=50, activation=Relu()))
## 第五層有5個神經元，激勵函數使用 X>0。
model.add(Neurons(units=50, activation=Relu()))
model.add(Neurons(units=50, activation=Relu()))
model.add(Neurons(units=50, activation=Relu()))
## 第六層有1個神經元，激勵函數使用 X>0。 (輸出層)
model.add(Neurons(units=1, activation=Linear()))
##-------------------------------------------------------------------------------------------------------##
# Model train
## params : 參數
## learning_rate : 學習率
## n_epoch : 迭代次數
## print_rate : 每迭代100次，印出到終端介面
params = {"learning_rate": 0.0001, "n_epoch": 1000, "print_rate": 100}
## MSE : 均方誤差
loss = MSE()
## 印出多層神經網路架構
print(model.layers)
# 開始訓練
model.train(loss, train_data=[train_data_x, train_data_y], params=params)
##-------------------------------------------------------------------------------------------------------##
## 測試神經網路是否成功能預測結果
# Run predict on new data
predictions = model.predict(test_data_x)

# Evaluate model performance using the same metric it used to train
performance = loss.forward(predictions, test_data_y)
print(f"Prediction loss: {performance.mean()}")
print(predictions)
##-------------------------------------------------------------------------------------------------------##
## 把訓練好的model存成.sav檔
filename1="C:\\Users\\BBS\\Desktop\\Machin leaning final project\
\\game\\MLGame-master\\games\\pingpong\\ml\\mlp_model_2P_0552030_V5.sav"
pickle.dump(model, open(filename1, 'wb'))
##-------------------------------------------------------------------------------------------------------##