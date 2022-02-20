# 交易冷却期：两笔相邻买卖之间至少相隔5天？
from base64 import encode
from cmath import sqrt
import csv
from encodings import utf_8
import numpy as np
f=open("code\\ljh\\data_deleted_first30days.csv",encoding="UTF_8")
data=np.loadtxt(f,delimiter=',')
status=[[1,0,0,1000]]  #每天的现金份额、黄金份额、比特币份额、总资产

gold_buy_standard=0.05
gold_sel_standard=-0.05
bit_buy_standard=0.3
bit_sel_standard=-0.3
gold_crate=0.01
bit_crate=0.02

for today in range(1,len(data)):

    # 获取每天的基本数据
    gold_price=data[today][1]
    gold_7zdf=data[today][2]
    # 如果是休假的后第一天，金价涨跌幅得往前顺移
    gold_on_temp=today-1
    while(data[gold_on_temp][1]==0):
        gold_on_temp-=1
    gold_1zdf=data[gold_on_temp][3]
    
    gold_std=data[today][5]
    bit_price=data[today][6]
    bit_7zdf=data[today][7]
    bit_1zdf=data[today-1][8]
    bit_std=data[today][10]
   
    # 获取昨天的status、今天的起始状态
    current_status=status[today-1]
    cash_share_current=current_status[0]
    gold_share_current=current_status[1]
    bit_share_current=current_status[2]
    total_asset=current_status[3]
    # 计算当前资产总值
    if gold_price==0:#闭市，无法交易黄金,即gold_1zdf=0,但是excel里填充的是均值不是0，所以得分类
        total_asset=gold_share_current*total_asset+bit_share_current*total_asset*(1+bit_1zdf/100)
    else:
        total_asset=gold_share_current*total_asset*(1+gold_1zdf/100)+bit_share_current*total_asset*(1+bit_1zdf/100)

    print("操盘第"+str(today)+"天,起手:"+"现金"+str(1-gold_share_current-gold_share_current)+
        "黄金:"+str(gold_share_current)+"比特币:"+str(bit_share_current)+"资产总值:"+str(total_asset))
    
    # 刷新默认操作
    gold_wanna_buy=False
    gold_wanna_sell=False
    bit_wanna_buy=False
    bit_wanna_sell=False
    gold_market_on=True

    # 黄金交易判断
    if(gold_price==0):# 不在交易日
        gold_market_on=False
    elif(gold_price!=0):
        if gold_7zdf>gold_buy_standard:# 买入标准
            gold_wanna_buy=True
        if gold_7zdf<gold_sel_standard:# 卖出标准
            gold_wanna_sell=True
    

    # 比特币交易判断
    if bit_7zdf>bit_buy_standard:# 买入标准
        bit_wanna_buy=True
    if bit_7zdf<bit_sel_standard:# 卖出标准
        bit_wanna_sell=True

    # 计算购买比例：
    gold_share_perfect=0
    bit_share_perfect=0
    if gold_wanna_buy==True or bit_wanna_buy==True:
        sharp_max=0
        for x in range(1,100):
            share=x/100
            sharp=(share*gold_7zdf*7+(1-share)*bit_7zdf*7)/sqrt(share*share*gold_std*gold_std+(1-share)*(1-share)*bit_std*bit_std)
            if sharp>sharp_max:
                sharp_max=sharp
                gold_share_perfect=share
                bit_share_perfect=1-share

    # 双买:
    if gold_wanna_buy==True and bit_wanna_buy==True:
        if cash_share_current==1 and gold_share_current==0 and bit_share_current==0: #手上全是现金，无资产，直接按比例购买
            gold_assest=gold_share_perfect*total_asset-gold_crate*gold_share_perfect*total_asset
            bit_assest=bit_share_perfect*total_asset-bit_crate*bit_share_perfect*total_asset
            total_asset=gold_assest+bit_assest
            gold_share_current=gold_assest/total_asset
            bit_share_current=bit_assest/total_asset
            temp=[0,gold_share_current,bit_share_current,total_asset]
            status.append(temp)
            print("day"+str(today)+",buy gold:"+str(gold_assest)+",buy bit:"+str(bit_assest))

        if cash_share_current>0 and gold_share_current>0 and bit_share_current==0: #有现金、黄金，没比特币，现金全买比特币
            gold_assest=gold_share_current*total_asset
            bit_assest=cash_share_current*total_asset-bit_crate*cash_share_current*total_asset
            total_asset=gold_assest+bit_assest
            gold_share_current=gold_assest/total_asset
            bit_share_current=bit_assest/total_asset
            temp=[0,gold_share_current,bit_share_current,total_asset]
            status.append(temp)
            print("day"+str(today)+",buy gold:"+str(0)+",buy bit:"+str(bit_assest))
        
        elif cash_share_current>0 and bit_share_current>0 and gold_share_current==0: #有现金、比特币，没比黄金，现金全买黄金
            bit_assest=bit_share_current*total_asset
            gold_assest=cash_share_current*total_asset-gold_crate*cash_share_current*total_asset
            total_asset=gold_assest+bit_assest
            gold_share_current=gold_assest/total_asset
            bit_share_current=bit_assest/total_asset
            temp=[0,gold_share_current,bit_share_current,total_asset]
            status.append(temp)
            print("day"+str(today)+",buy gold:"+str(gold_assest)+",buy bit:"+str(0))
        
        elif cash_share_current==0:# 没现金，啥也不买。。。。。。。。。。。。。可以调仓买，再改
            temp=[cash_share_current,gold_share_current,bit_share_current,total_asset]
            status.append(temp)

    # 一买一不变:
    if gold_wanna_buy==True and bit_wanna_buy==False and bit_wanna_sell==False:#黄金要买，比特币不变，
        if cash_share_current>0:#有现金，现金全买黄金
            bit_assest=bit_share_current*total_asset
            gold_assest=cash_share_current*total_asset-gold_crate*cash_share_current*total_asset
            total_asset=gold_assest+bit_assest
            gold_share_current=gold_assest/total_asset
            bit_share_current=bit_assest/total_asset
            temp=[0,gold_share_current,bit_share_current,total_asset]
            status.append(temp)
            print("day"+str(today)+",buy gold:"+str(gold_assest))
        elif cash_share_current==0:#没现金，另一个不能动，因此啥也不干
            temp=[cash_share_current,gold_share_current,bit_share_current,total_asset]
            status.append(temp)
    
    if bit_wanna_buy==True and gold_wanna_buy==False and gold_wanna_sell==False:#比特币要买，黄金不变，
        if cash_share_current>0:#有现金，现金全买比特币
            gold_assest=gold_share_current*total_asset
            bit_assest=cash_share_current*total_asset-bit_crate*cash_share_current*total_asset
            total_asset=gold_assest+bit_assest
            gold_share_current=gold_assest/total_asset
            bit_share_current=bit_assest/total_asset
            temp=[0,gold_share_current,bit_share_current,total_asset]
            status.append(temp)
            print("day"+str(today)+",buy bit:"+str(bit_assest))
        elif cash_share_current==0:#没现金，另一个不能动，因此啥也不干
            temp=[cash_share_current,gold_share_current,bit_share_current,total_asset]
            status.append(temp)
    
    #一买一卖
    if gold_wanna_buy==True and bit_wanna_sell==True: #要买黄金，卖比特币
        # 这样一来黄金的比例肯定是1，其他两个0，只要算一下佣金，更新总资产即可
        total_asset-=gold_crate*cash_share_current*total_asset+(gold_crate+bit_crate)*bit_share_current*total_asset
        temp=[0,1,0,total_asset]
    
    if bit_wanna_buy==True and gold_wanna_sell==True: #要买黄金，卖比特币
        # 这样一来黄金的比例肯定是1，其他两个0，只要算一下佣金，更新总资产即可
        total_asset-=gold_crate*cash_share_current*total_asset+(gold_crate+bit_crate)*bit_share_current*total_asset
        temp=[0,1,0,total_asset]


