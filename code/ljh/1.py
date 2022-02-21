# 交易冷却期：两笔相邻买卖之间至少相隔7天
from base64 import encode
from cmath import sqrt
import csv
from encodings import utf_8
import numpy as np
f=open("code\\ljh\\data_deleted_first30days.csv",encoding="UTF_8")
data=np.loadtxt(f,delimiter=',')
status=[[1,0,0,1000]]  #每天的现金份额、黄金份额、比特币份额、总资产

gold_buy_standard=0.0015
gold_sel_standard=-0.05
bit_buy_standard=0.25
bit_sel_standard=-0.15
gold_crate=0.01
bit_crate=0.02
gold_wait=0
bit_wait=0
gold_hold_day=0
bit_hold_day=0
gold_buy_times=0
bit_buy_times=0

for today in range(1,len(data)):
    if today==1527:
        print('stop')
    # 获取每天的基本数据
    gold_price=data[today][1]
    gold_7zdf=data[today][2]
    # 如果是休假的后第一天，金价涨跌幅得往前顺移
    gold_on_temp=today-1
    while(data[gold_on_temp][1]==0):
        gold_on_temp-=1
    gold_1zdf=data[gold_on_temp][3]
    
    # gold_std=data[today][5]#7日标准差
    gold_std=data[today][4]#7日下半标准差

    bit_price=data[today][6]
    bit_7zdf=data[today][7]
    bit_1zdf=data[today-1][8] 
    # bit_std=data[today][10] #7日标准差
    bit_std=data[today][9] #7日下半标准差
   
    # 获取昨天的status、今天的起始状态
    current_status=status[today-1]
    cash_share_current=current_status[0]
    gold_share_current=current_status[1]
    bit_share_current=current_status[2]

    if cash_share_current<0 or gold_share_current<0 or bit_share_current<0:
        print('stop')
    if gold_share_current!=0:
        gold_hold_day+=1
    if bit_share_current!=0:
        bit_hold_day+=1
    
    total_asset=current_status[3]
    # 计算当前资产总值
    if gold_price==0:#闭市，无法交易黄金,即gold_1zdf=0,但是excel里填充的是均值不是0，所以得分类
        total_asset=cash_share_current*total_asset+gold_share_current*total_asset+bit_share_current*total_asset*(1+bit_1zdf/100)
    else:
        total_asset=cash_share_current*total_asset+gold_share_current*total_asset*(1+gold_1zdf/100)+bit_share_current*total_asset*(1+bit_1zdf/100)

    # print("操盘第"+str(today)+"天,起手:"+"现金"+str(1-gold_share_current-bit_share_current)+
    #     "黄金:"+str(gold_share_current)+"比特币:"+str(bit_share_current)+"资产总值:"+str(total_asset))
    
    # 刷新默认操作
    gold_wanna_buy=False
    gold_wanna_sell=False
    bit_wanna_buy=False
    bit_wanna_sell=False
    gold_market_on=True

    # 黄金交易判断
    
    if bit_buy_times<3:
        bit_hold_avg=7
    else:
        bit_hold_avg=bit_hold_day/bit_buy_times

    if gold_buy_times<3:
        gold_hold_avg=7
    else:
        gold_hold_avg=gold_hold_day/gold_buy_times

    if(gold_price==0):# 不在交易日
        gold_market_on=False
    elif(gold_price!=0):
        if gold_wait<=0:
            if gold_7zdf>200*gold_crate/gold_hold_avg:# 买入标准
                gold_wanna_buy=True
            if gold_7zdf<0 :# 卖出标准
                gold_wanna_sell=True
                gold_wanna_buy=False
    

    # 比特币交易判断

    if bit_wait<=0:
        if bit_7zdf>200*bit_crate/bit_hold_avg:# 买入标准
            bit_wanna_buy=True
        if bit_7zdf<0 :# 卖出标准
            bit_wanna_sell=True
            bit_wanna_buy=False

    if data[today-1][8]+data[today-2][8]+data[today-3][8]+data[today-4][8]<-10:
        bit_wanna_sell=True
        bit_wanna_buy=False

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
            temp=[0,gold_share_current,bit_share_current,total_asset,today]
            status.append(temp)
            
            print("day"+str(today)+",buy gold:"+str(gold_assest)+",buy bit:"+str(bit_assest))
            gold_wait=7
            bit_wait=7
            bit_buy_times+=1
            gold_buy_times+=1
            # continue

        if cash_share_current>0 and gold_share_current>0 and bit_share_current==0: #有现金、黄金，没比特币，现金全买比特币
            gold_assest=gold_share_current*total_asset
            bit_assest=cash_share_current*total_asset-bit_crate*cash_share_current*total_asset
            total_asset=gold_assest+bit_assest
            gold_share_current=gold_assest/total_asset
            bit_share_current=bit_assest/total_asset
            temp=[0,gold_share_current,bit_share_current,total_asset,today]
            status.append(temp)
            
            print("day"+str(today)+",buy gold:"+str(0)+",buy bit:"+str(bit_assest))
            gold_wait-=1
            bit_wait=7
            bit_buy_times+=1
            # continue
        
        elif cash_share_current>0 and bit_share_current>0 and gold_share_current==0: #有现金、比特币，没比黄金，现金全买黄金
            bit_assest=bit_share_current*total_asset
            gold_assest=cash_share_current*total_asset-gold_crate*cash_share_current*total_asset
            total_asset=gold_assest+bit_assest
            gold_share_current=gold_assest/total_asset
            bit_share_current=bit_assest/total_asset
            temp=[0,gold_share_current,bit_share_current,total_asset,today]
            status.append(temp)
            print("day"+str(today)+",buy gold:"+str(gold_assest)+",buy bit:"+str(0))
            gold_wait=7
            bit_wait-=1
            gold_buy_times+=1
            # continue
        
        elif cash_share_current==0:# 没现金，可以调仓买
            # temp=[cash_share_current,gold_share_current,bit_share_current,total_asset,today]
            # status.append(temp)
            # # continue
            delta_share=gold_share_current-gold_share_perfect
            if(abs(delta_share)!=abs(bit_share_current-bit_share_perfect)):
                print("strange")
            # gold_assest=gold_share_current*total_asset+delta_share*total_asset-delta_share*total_asset
            # 分三种情况计算调仓之后的黄金、比特币比例
            commision=0
            case=0
            if gold_share_current==0 and bit_share_current==1:# 无现金，无黄金，全比特币；调仓就是卖比特币买黄金
                bit_assest=(1-abs(delta_share))*total_asset
                cash_assest=abs(delta_share)*total_asset
                commision+=abs(delta_share)*total_asset*bit_crate
                gold_assest=gold_share_current*total_asset+cash_assest*(1-gold_crate)
                commision+=cash_assest*gold_crate
                total_asset_new=gold_assest+bit_assest
                gold_share_perfect=gold_assest/total_asset_new
                bit_share_perfect=bit_assest/total_asset_new
                case=1

            
            if gold_share_current==1 and bit_share_current==0:# 无现金，无比特币，全黄金；调仓就是卖黄金买比特币
                gold_assest=(1-abs(delta_share))*total_asset
                cash_assest=abs(delta_share)*total_asset
                commision+=abs(delta_share)*total_asset*gold_crate
                bit_assest=bit_share_current*total_asset+cash_assest*(1-bit_crate)
                commision+=cash_assest*bit_crate
                total_asset_new=gold_assest+bit_assest
                gold_share_perfect=gold_assest/total_asset_new
                bit_share_perfect=bit_assest/total_asset_new
                case=2


            
            if gold_share_current==1 and bit_share_current==0:# 无现金，有比特币，有黄金
                if gold_share_current>=gold_share_perfect: # 黄金比例高于理论值，卖黄金，买比特币
                    gold_assest=(gold_share_current-abs(delta_share))*total_asset-abs(delta_share)*total_asset*gold_crate
                    cash_assest=abs(delta_share)*total_asset
                    commision+=abs(delta_share)*total_asset*gold_crate
                    bit_assest=bit_share_current*total_asset+cash_assest*(1-bit_crate)
                    commision+=cash_assest*bit_crate
                    total_asset_new=gold_assest+bit_assest
                    gold_share_perfect=gold_assest/total_asset_new
                    bit_share_perfect=bit_assest/total_asset_new
                
                if bit_share_current>=gold_share_perfect: # 比特币比例高于理论值，卖比特币，买黄金
                    bit_assest=(bit_share_current-abs(delta_share))*total_asset-abs(delta_share)*total_asset*bit_crate
                    cash_assest=abs(delta_share)*total_asset
                    commision+=abs(delta_share)*total_asset*bit_crate
                    gold_assest=gold_share_current*total_asset+cash_assest*(1-gold_crate)
                    commision+=cash_assest*gold_crate
                    total_asset_new=gold_assest+bit_assest
                    gold_share_perfect=gold_assest/total_asset_new
                    bit_share_perfect=bit_assest/total_asset_new

            # R_now=gold_share_current*total_asset*gold_7zdf*7+bit_share_current*total_asset*bit_7zdf*7
            # R_changed=gold_share_perfect*total_asset_new*gold_7zdf*7+bit_share_perfect*total_asset_new*bit_7zdf*7
            # std_now=sqrt(gold_share_current*gold_share_current*gold_std*gold_std+bit_share_current*bit_share_current*bit_std*bit_std)
            # std_changed=sqrt(gold_share_perfect*gold_share_perfect*gold_std*gold_std+bit_share_perfect*bit_share_perfect*bit_std*bit_std)
            # if (R_changed/std_changed-R_now/std_changed)*(std_now/2+std_changed/2)>commision:# 单位风险的收益乘调仓前后平均风险大于佣金，调仓
            #     temp=[0,gold_share_perfect,bit_share_perfect,total_asset_new,today]
            #     status.append(temp)
            #     print("day"+str(today)+"调仓")
            # else:
            #     temp=[cash_share_current,gold_share_current,bit_share_current,total_asset,today]
            #     status.append(temp)
            
            # 发现从不调仓，修改：若调仓比例大于百分之10则调
            if abs(delta_share)>0.1 :
                temp=[0,gold_share_perfect,bit_share_perfect,total_asset_new,today]
                status.append(temp)
                print("day"+str(today)+"调仓")
                if case==1:
                    gold_wait=7
                    bit_wait-=1
                    gold_buy_times+=1
                elif case==2:
                    gold_wait-=1
                    bit_wait=7
                    bit_buy_times+=1
                else:
                    gold_wait-=1
                    bit_wait-=1
            else:
                temp=[cash_share_current,gold_share_current,bit_share_current,total_asset,today]
                gold_wait-=1
                bit_wait-=1
                status.append(temp)



    # 一买一不变:
    if gold_wanna_buy==True and bit_wanna_buy==False and bit_wanna_sell==False:#黄金要买，比特币不变，
        if cash_share_current>0:#有现金，现金全买黄金
            if gold_share_current==0:# 本来没有黄金,第一次买
                gold_wait=7
                bit_wait-=1
                gold_buy_times+=1
            else:
                gold_wait-=1
                bit_wait-=1

            bit_assest=bit_share_current*total_asset
            gold_assest=gold_share_current*total_asset+cash_share_current*total_asset-gold_crate*cash_share_current*total_asset
            total_asset=gold_assest+bit_assest
            gold_share_current=gold_assest/total_asset
            bit_share_current=bit_assest/total_asset
            temp=[0,gold_share_current,bit_share_current,total_asset,today]
            status.append(temp)
            print("day"+str(today)+",buy gold:"+str(gold_assest))
            
            
            # continue
        elif cash_share_current==0:#没现金，另一个不能动，因此啥也不干
            temp=[cash_share_current,gold_share_current,bit_share_current,total_asset,today]
            status.append(temp)
            gold_wait-=1
            bit_wait-=1
            # continue
    
    if bit_wanna_buy==True and gold_wanna_buy==False and gold_wanna_sell==False:#比特币要买，黄金不变，
        if cash_share_current>0:#有现金，现金全买比特币
            if bit_share_current==0:#第一次买比特币
                bit_wait=7
                gold_wait-=1
                bit_buy_times+=1
            else:
                bit_wait-=1
                gold_wait-=1
            gold_assest=gold_share_current*total_asset
            bit_assest=bit_share_current*total_asset+cash_share_current*total_asset-bit_crate*cash_share_current*total_asset
            total_asset=gold_assest+bit_assest
            gold_share_current=gold_assest/total_asset
            bit_share_current=bit_assest/total_asset
            temp=[0,gold_share_current,bit_share_current,total_asset,today]
            status.append(temp)
            print("day"+str(today)+",buy bit:"+str(bit_assest))
            # continue
        elif cash_share_current==0:#没现金，另一个不能动，因此啥也不干
            temp=[cash_share_current,gold_share_current,bit_share_current,total_asset,today]
            status.append(temp)
            gold_wait-=1
            bit_wait-=1
            # continue
    
    #一买一卖
    if gold_wanna_buy==True and bit_wanna_sell==True: #要买黄金，卖比特币
        # 这样一来黄金的比例肯定是1，其他两个0，只要算一下佣金，更新总资产即可
        print("day"+str(today)+",buy gold:"+str(cash_share_current*total_asset+bit_share_current*total_asset)+
            ",sell bit:"+str(bit_share_current*total_asset))
        total_asset-=gold_crate*cash_share_current*total_asset+(gold_crate+bit_crate-gold_crate*bit_crate)*bit_share_current*total_asset
        temp=[0,1,0,total_asset,today]
        status.append(temp)
        if bit_share_current>0:

            bit_wait=7
        else:
            bit_wait-=1
        if gold_share_current!=1:#确实买了
             gold_wait=7
        else:# 没买
            gold_wait-=1
        if gold_share_current==0:# 第一次买
            gold_buy_times+=1
        # continue
    
    if bit_wanna_buy==True and gold_wanna_sell==True: #要买比特币，卖黄金
        # 这样一来比特币的比例肯定是1，其他两个0，只要算一下佣金，更新总资产即可
        print("day"+str(today)+",buy bit:"+str(cash_share_current*total_asset+gold_share_current*total_asset)+
            ",sell gold:"+str(gold_share_current*total_asset))
        total_asset-=bit_crate*cash_share_current*total_asset+(gold_crate+bit_crate-gold_crate*bit_crate)*gold_share_current*total_asset
        temp=[0,0,1,total_asset,today]
        status.append(temp)
        if gold_share_current>0:
            gold_wait=7
        else:
            gold_wait-=1
        if bit_share_current!=1:
             bit_wait=7
        else:
            bit_wait-=1
        if bit_share_current==0:
            bit_buy_times+=1
        # continue

    # 两不变
    if gold_wanna_buy==False and gold_wanna_sell==False and bit_wanna_buy==False and bit_wanna_sell==False:
        temp=[cash_share_current,gold_share_current,bit_share_current,total_asset,today]
        status.append(temp)
        bit_wait-=1
        gold_wait-=1
        # continue

    # 一个不变，一个卖出
    if gold_wanna_buy==False and gold_wanna_sell==False and bit_wanna_sell==True: #黄金不变，卖比特币
        print("day"+str(today)+",sell bit:"+str(bit_share_current*total_asset))
        gold_wait-=1
        if bit_share_current==0:
            bit_wait-=1
        else: 

            bit_wait=7
        cash_assest=cash_share_current*total_asset+bit_share_current*total_asset-bit_crate*bit_share_current*total_asset
        gold_assest=gold_share_current*total_asset
        total_asset=cash_assest+gold_assest
        gold_share_current=gold_assest/total_asset
        cash_share_current=cash_assest/total_asset
        temp=[cash_share_current,gold_share_current,0,total_asset,today]
        status.append(temp)

        # continue

    if bit_wanna_buy==False and bit_wanna_sell==False and gold_wanna_sell==True: #比特币不变，卖黄金
        print("day"+str(today)+",sell gold:"+str(gold_share_current*total_asset))
        bit_wait-=1
        if gold_share_current==0:
            gold_wait-=1
        else: 
            gold_wait=7
        cash_assest=cash_share_current*total_asset+gold_share_current*total_asset-gold_crate*gold_share_current*total_asset
        bit_assest=bit_share_current*total_asset
        total_asset=cash_assest+bit_assest
        bit_share_current=bit_assest/total_asset
        cash_share_current=cash_assest/total_asset
        temp=[cash_share_current,0,bit_share_current,total_asset,today]
        status.append(temp)
        # continue

    # 双卖出：
    if bit_wanna_sell==True and gold_wanna_sell==True:
        if gold_share_current==0:
            gold_wait-=1
        else: 
            gold_wait=7
        if bit_share_current==0:
            bit_wait-=1
        else: 
            bit_wait=7
        print("day"+str(today)+",sell gold:"+str(gold_share_current*total_asset)+",sell bit:"+str(bit_share_current*total_asset))
        # 现金比例为1，其他两项均为0，直接算一下扣除佣金的资产即可
        total_asset-=gold_crate*gold_share_current*total_asset+bit_crate*bit_share_current*total_asset
        temp=[1,0,0,total_asset,today]
        status.append(temp)
        # continue
    

    




with open('code\\ljh\\huice\\first.csv','w',newline='')as f:
    f_csv = csv.writer(f)
    f_csv.writerows(status)
