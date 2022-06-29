#!/usr/bin/env python3  
#-*-coding: utf-8-*-
import sys
#sys.path.insert(0,'/home/pi/Desktop/pliki')

import matplotlib.pyplot as plt
import numpy as np

import codecs
import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
#from Tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox
#from events import Events
import re
import serial
#from PIL import ImageTk,Image

napis=''
lam=[]
ypoint=np.zeros((288))

try:
    ser=serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600)
    print('dziala')
except:
    print('nie dziala')
    
def UART_I():
    global ser,napis,napis2
    serialstring=''
    time.sleep(0.01)
    if(ser.in_waiting>0):
        serialstring=ser.read_until('\n',1600)#ser.read(16)
        
#         print (serialstring)
        napis=napis+str(serialstring)

def start():
    global napis,lam, ypoint
    try:
        ser=serial.Serial(
        port='/dev/ttyACM0',
        baudrate=9600)
        print('dziala')
    except:
        print('nie dziala')
    x=0
    while x!=3:
        UART_I()
        x=x+1
   
    if re.search('5000',napis):
        print('jest')
    napis2=re.sub(r"[b'nr \\]", '', napis)
    napis=''

    napis4=napis2.split('V')

    pix=[]
    flag=0

    for i in range(0,600):
        if(napis4[i]=='5000'):
            print('jest')
            if flag==0:
                flag=1
        if flag==1 and len(pix)<282 and napis4[i]!='5000':
            if len(pix)<1:
                pix.append(int(napis4[i]))
                #print('za ,maly')
            else:
                pix.append(int(napis4[i]))
        
#print(pix)
#print(len(pix))
    lam=[]
    mnoznik=495/287
    for x in range (0,288):
        lam.append(round(325+mnoznik*x,2))
#print(lam)

    ypoint=np.zeros((288))
    yp=190
    ypoint[0]=pix[2]
    for x in range(1,120):
        ypoint[x]=pix[x]
#for i in range(50,120):
 #   ypoint[i]=pix[i+20]
    for y in range(190,236):
        ypoint[yp]=pix[y]
        yp=yp+1
        ypoint[yp]=pix[y]
        yp=yp+1
    
    for yx in range(120,190):
        ypoint[yx]=pix[yx]
    
    for za in range(282,288):
        ypoint[za]=pix[280]
    
    print(ypoint)
#print(len(ypoint))
    

    
    
    plt.plot(lam,ypoint)
    plt.ylabel('Spectral flux a. u.')
    plt.xlabel('Wavelength [nm]')
    plt.grid(b=True,which='major')
    plt.minorticks_on()
    plt.grid(b=True,which='minor',alpha=0.2)
   # plt.show()


#start()
