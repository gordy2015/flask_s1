from flask_sqlalchemy import SQLAlchemy
import datetime,random

def randomnum():
    for i in range(0, 10):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # 生成当前时间
        randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:  #如果生成的随机数小于10,则补0,以凑足两位数
            randomNum = str(0) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum
