#!/usr/bin/env python
# coding: utf-8

# # 平稳性检验

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# In[2]:


gold=pd.read_csv('C://Users//honor//Desktop//2022_MCM_ICM_Problems//LBMA-GOLD.csv')


# In[3]:


gold['USD (PM)']=gold['USD (PM)'].fillna(gold['USD (PM)'].interpolate())


# In[4]:


gold = gold.drop('Date',axis=1)


# In[5]:


gold.to_csv('C://Users//honor//Desktop//2022_MCM_ICM_Problems//LBMA-GOLD_2.csv')


# In[5]:


from statsmodels.tsa.stattools import adfuller


# In[6]:


gold_result = adfuller(gold['USD (PM)']) #生成adf检验结果
print('The ADF Statistic of gold: %f' % gold_result[0])
print('The p value of gold: %f' % gold_result[1])


# In[6]:


gold_cha = np.diff(gold['USD (PM)'])


# In[8]:


gold_result_cha = adfuller(gold_cha) #生成adf检验结果
print('The ADF Statistic of gold_cha: %f' % gold_result_cha[0])
print('The p value of gold_cha: %f' % gold_result_cha[1])


# In[7]:


gold_cha_cha = pd.DataFrame(np.diff(gold_cha))


# In[8]:


gold_cha_cha.to_csv('C://Users//honor//Desktop//2022_MCM_ICM_Problems//gold_diff2.csv')


# In[10]:


gold_result_cha_cha = adfuller(gold_cha_cha) #生成adf检验结果
print('The ADF Statistic of gold_cha_cha: %f' % gold_result_cha_cha[0])
print('The p value of gold_cha_cha: %f' % gold_result_cha_cha[1])


# In[11]:


plt.plot(gold_cha)
plt.show()


# In[12]:


plt.plot(gold_cha_cha)
plt.show()


# # 纯随机性检验

# In[13]:


from statsmodels.stats.diagnostic import acorr_ljungbox


# In[14]:


###########纯随机性检验（白噪声检验）
print(acorr_ljungbox(gold_cha,lags=1))


# In[15]:


###########纯随机性检验（白噪声检验）
print(acorr_ljungbox(gold_cha_cha,lags=1))


# # 预测模型

# In[27]:


def Predict(data,length):
    from statsmodels.tsa.arima_model import ARMA
    from itertools import product

    # 设置p阶，q阶范围
    # product p,q的所有组合
    # 设置最好的aic为无穷大
    # 对范围内的p,q阶进行模型训练，得到最优模型
    ps = range(0, 6)
    qs = range(0, 6)
    parameters = product(ps, qs)
    parameters_list = list(parameters)

    best_aic = float('inf')
    results = []
    for param in parameters_list:
        try:
            model = ARMA(data, order=(param[0], param[1])).fit()
        except ValueError:
            print("参数错误：", param)
            continue
        aic = model.aic
        if aic < best_aic:
            best_model = model
            best_aic = model.aic
            best_param = param
    print('Best_param:',best_param)
    return np.array(list(best_model.forecast(length)[0]))


# In[21]:


def Reduction(np_lst,raw_data):
    
    data_diff_1_reduction = np_lst.cumsum() + (raw_data[raw_data.size-1]-raw_data[raw_data.size-2])
    data_diff_2_reduction = data_diff_1_reduction.cumsum() + raw_data[raw_data.size-1]
    return data_diff_2_reduction


# # 批量化处理数据

# In[22]:


gold.shape


# In[28]:


lst = []
for i in range(1000,1266):
    data = gold[:i]
    data_cha_cha = gold_cha_cha[:i-2]
    np_lst = Predict(data_cha_cha,7)
    lst.append(Reduction(np_lst,data))
lst

