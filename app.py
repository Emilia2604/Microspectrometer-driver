#!/usr/bin/env python3  
#-*-coding: utf-8-*-
import sys
import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
import threading
import numpy as np
import math

from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import spectrometer
import dac
import odczyt

flaga=0
flag_offset=0
flag_source=0

path_offset='offset/offset_'
path_source='source/source_'
path_spectrum='spectrum/spectrum_'

def mode_get():
    wybor=var.get()
    return wybor

def led_set(x):
    wartosc=int(led.get())
    print(x)
    dac.MCP4726(wartosc*3)
    
window=tk.Tk()
window.title("Spectrometer")
window.geometry('1400x700')
window['bg']='ghost white'

class Contin(threading.Thread):
    def __init__(self,id, value):
        threading.Thread.__init__(self,name="Contin-%d" % (id,))
        self.value = value
    def run(self):
        while flaga!=0:
           chart()
           window.update()
           time.sleep(1)
           
def spr_absor():
    global flag_offset, flag_source
    if flag_offset==0 or flag_source==0:
        tk.messagebox.showwarning('Error','First measure the source and offset!')
    else:
        absorbance()
        
def pomiar(ilosc,sciezka):
    led_v=int(led.get())
    for x in range(0,ilosc):
        spectrometer.start()
        ypoint=spectrometer.ypoint
        path=sciezka+str(x)
        write(path,ypoint)     

def chart():
    global a
    spectrometer.start()
    xpoint=spectrometer.lam
    ypoint=spectrometer.ypoint
    led_v=int(led.get())   
    for x in range(0,288):
        ypoint[x]=ypoint[x]
    f = plt.Figure(figsize=(5,5), dpi=100)
    a = f.add_subplot(111)
    a.plot(xpoint,ypoint)
    a.set_xlabel('Wavelength [nm]')
    a.set_ylabel('Spectral flux a. u.')
    canvas = FigureCanvasTkAgg(f, window)
    canvas.get_tk_widget().grid(column=1, row=3, columnspan=4)
    
def chart2(y,opis):
    xpoint=spectrometer.lam
    f2 = plt.Figure(figsize=(5,5), dpi=100)
    a2 = f2.add_subplot(111)
    a2.plot(xpoint,y)
    a2.set_xlabel('Wavelength [nm]')
    a2.set_ylabel(opis)
    canvas = FigureCanvasTkAgg(f2, window)
    canvas.get_tk_widget().grid(column=5, row=3, columnspan=4)
    
def start():
    global flaga
    tryb=mode_get()
    flaga=1
    if tryb==1:
        chart()
    else:
        Contin(1,2).run()
    
def stop():
    global flaga
    flaga=0
    
def save():
    name = nazwa_e.get()
    czas = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    file_name=name+czas
    ypoint=spectrometer.ypoint
    write('spectrum/'+file_name,ypoint)
    fi=a.get_figure()
    fi.savefig('/home/pi/Desktop/spectrum/'+str(file_name)+'.png')
    
def save2():
    name = nazwa_e.get()
    czas = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    file_name=name+czas
    ypoint=absorbance()
    write('spectrum/'+file_name,ypoint)
    fi2=a2.get_figure()
    fi2.savefig('/home/pi/Desktop/spectrum/'+str(file_name)+'.png')
    
def offset():
    global path_offset,flag_offset
    dac.MCP4726(0)
    pomiar(20,path_offset)
    flag_offset=1
    
def source():
    global path_source,flag_source 
    pomiar(20,path_source)
    flag_source=1
    
def write(filename,pomiar):
    filepath='/home/pi/Desktop/'+str(filename)+'.txt'
    f = open(filepath, "w")
    tekst=str(led.get())+'\n'
    for x in range(0, len(pomiar)):
        tekst=tekst+str(pomiar[x])+'\n'
    f.write(tekst)
    
def averange(filepath):
    path='/home/pi/Desktop/'+str(filepath)
    ilosc=20
    yp=np.zeros((ilosc,288))
    #odczyt z plikow
    for y in range(0,ilosc):
        ylin=[]
        filepath=path+str(y)+'.txt'
        f=open(filepath,'r')
        linie = f.readlines()
        print(linie)
        for line in linie:
            ylin.append(line.replace('\n',''))
        for x in range(0,288):
            yp[y,x]=float(ylin[x+1])
    #srednia
    print(yp)
    suma=np.zeros((288)) # wynik liczenia sredniej
    xp=np.zeros((288)) 
    for y in range (0,288):
        sumaa=0
        for x in range(0,ilosc):
            sumaa=sumaa+yp[x,y]
        suma[y]=sumaa/ilosc
    return suma    
    
def absorbance():
    global path_source, path_offset
    noise=np.zeros((288))
    i0=np.zeros((288))
    spectrometer.start()
    ix=spectrometer.ypoint
    noise=averange(path_offset)
    i0=averange(path_source)
    absorbancey=np.zeros((288))
    for x in range(0,288):
        try:
            absorbancey[x]=math.log10(i0[x]/ix[x])
        except:
            tk.messagebox.showwarning('Error','First measure the source and offset!')
    chart2(absorbancey,'absorbance a. u.')
    return absorbancey

var = IntVar()

f = plt.Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)
a.plot([1,2],[1,3])
canvas = FigureCanvasTkAgg(f, window)
canvas.get_tk_widget().grid(column=1, row=3, columnspan=4)

bgg=window.cget('background')

single1=Radiobutton(window,text="Single", variable=var, value=1, background='ghost white')
single1.grid(column=1, row=1)
single2=Radiobutton(window,text="Continous", variable=var, value=2, background='ghost white')
single2.grid(column=2, row=1)

paramll=ttk.Label(window, text=" Power\n LED[%]", font=("Arial Bold",15), background='ghost white')
paramll.grid(column=0, row=0)
paramtl=ttk.Label(window, text=" Mode", font=("Arial Bold",15), background='ghost white')
paramtl.grid(column=1, row=0)

led = Scale(window, background='ghost white',command=led_set)
led.grid(column=0, row=1,rowspan=2)

nazwa_l=ttk.Label(window, text='File name',font=("Arial Bold",10), background='ghost white')
nazwa_l.grid(column=5,row=0)
nazwa_e=ttk.Entry(window, width=10, background='ghost white')
nazwa_e.grid(column=5, row=1)

start=tk.Button(window, text='START', bg="green", command=start)
start.grid(column=3, row=1)

stop=tk.Button(window, text='STOP', bg="red", command=stop)
stop.grid(column=4, row=1)

save_b=tk.Button(window, text='SAVE', command=save)
save_b.grid(column=1, row=4)

save_b2=tk.Button(window, text='SAVE', command=save2)
save_b2.grid(column=5, row=4)

source_b=tk.Button(window, text='SOURCE', command=source)
source_b.grid(column=6, row=2)

offset_b=tk.Button(window, text='OFFSET', command=offset)
offset_b.grid(column=7, row=2)

abso_b=tk.Button(window, text='ABSORBANCE', command=spr_absor)
abso_b.grid(column=8, row=2)

window.mainloop()