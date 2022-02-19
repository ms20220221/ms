library(zoo)
library(tseries)
library(forecast)

data_raw = read.csv('C://Users//honor//Desktop//2022_MCM_ICM_Problems//BCHAIN-MKPRU_1.csv')
data_raw = ts(data_raw)
plot(data_raw,col=4,lwd=2,pch=8,type='o')

adf.test(data_raw)

for (i in 1:3) print(Box.test(data_raw,type="Ljung-Box",lag = 6*i))

a=auto.arima(data_raw,include.mean = T)
a

for(i in 1:3) print(Box.test(a$residual,type="Ljung-Box",lag=6*i))

a.fore=forecast(a,h=5)
a.fore

L1=a.fore$fitted-1.96*sqrt(a$sigma2)
U1=a.fore$fitted+1.96*sqrt(a$sigma2)
L2=ts(a.fore$lower[,2])
U2=ts(a.fore$upper[,2])
c1=min(data_raw,L1,L2)
c2=max(data_raw,L2,U2)
plot(data_raw,type="p",pch=8,ylim=c(c1,c2))
lines(a.fore$fitted,col=2,lwd=2)
lines(a.fore$mean,col=2,lwd=2)
lines(L1,col=4,lty=2)
lines(U1,col=4,lty=2)
lines(L2,col=4,lty=2)
lines(U2,col=4,lty=2)

ARIMA <-function(data,h){
  a <- tryCatch(
    {
      auto.arima(data,include.mean=T,method = 'ML')
    },error = function(e){
      arima(data,order = c(4,1,5),include.mean=T,method = 'ML')
    }
  )
  a.fore=forecast(a,h=h)
  return(a.fore)
}

lst = list()
for (i in 31:1826){
  data = data_raw[1:i]
  lst_sub = ARIMA(data,h=7)
  lst[[i-30]]=lst_sub
}

lst 

lst_result=list()
count<-1
while (count <=1826) {
  lst_result[[count]] = lst[[count]]$mean
  count=count+1
}
lst_result
write.csv(lst_result,file='C://Users//honor//Desktop//2022_MCM_ICM_Problems//result_bchain.csv',row.names = F,quote = F,sep = ',')
