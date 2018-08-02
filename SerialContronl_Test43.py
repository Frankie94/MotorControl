# -*- coding: gb18030 -*-
"""
Created on Wed Aug  1 15:40:58 2018

@author: Fangkai\

@contact: kai.fang@siat.ac.cn

"""

import serial 
import time 

log = 0

s = serial.Serial('com4', 115200, timeout=2)

MotionCommand= bytes([0X08,0X0F,0XF0,0X24,0XA2,0X41,0X89,0X00,0X00,0X97,
                0X08,0X0F,0XF0,0X24,0XA0,0X55,0X53,0X00,0X55,0XC8, 
                0X08,0X0F,0XF0,0X24,0X9E,0X10,0X00,0X00,0X27,0X00, 
                0X08,0X0F,0XF0,0X59,0X09,0XDF,0XFF,0X00,0X00,0X47, 
                0X08,0X0F,0XF0,0X59,0X09,0XBF,0XC1,0X87,0X01,0X71, 
                0X08,0X0F,0XF0,0X59,0X09,0XFF,0XFF,0X40,0X00,0XA7, 
                0X04,0X0F,0XF0,0X01,0X08,0X0C, 
                0X04,0X0F,0XF0,0X70,0X0F,0X82,0X04,0X0F,0XF0,0X04,0X08,0X0F
                ])

s.write(MotionCommand)

while True: 
    log += 1
    
    localtime = time.asctime(time.localtime(time.time()))       
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    
    AposReq= bytes([0X08,0X0F,0XF0,0XB0,0X05,0X0F,0XF1,0X02,0X28,0XE6])
    s.write(AposReq)
    
    n = s.read(15)
    
    datas =''.join(map(lambda x:('/x' if len(hex(x))>=4 else '/x0')+hex(x)[2:],n))
    
    new_datas = datas.split("/x")
    
    for i in range(1,15):
        if new_datas[i] == "02" and new_datas[i+1] == "28":
            if i <= 10:
                need = new_datas[i+4]+new_datas[i+5]+new_datas[i+2]+new_datas[i+3]
            elif i == 11:
                need = new_datas[15]+new_datas[1]+new_datas[13]+new_datas[14]
            elif i == 12:
                need = new_datas[1]+new_datas[2]+new_datas[14]+new_datas[15]
            elif i == 13:
                need = new_datas[2]+new_datas[3]+new_datas[15]+new_datas[1]
            elif i == 14:
                need = new_datas[3]+new_datas[4]+new_datas[1]+new_datas[2]               
    
    my_need = int(hex(int(need,16)),16)
    positionSI = 2*3.1416*my_need/4/6400/1
       
    print(local_time,datas,positionSI) 
   
    if log > 20:
        s.close()
        break
    
    time.sleep(0.1)