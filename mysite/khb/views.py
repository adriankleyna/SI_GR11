from django.conf import settings
import os
from django.shortcuts import render
import json
import numpy
import random
import statistics

def fitness(rowSize,capacityMax):
   return abs(capacityMax-rowSize)

def sum(lista):
   suma=0
   for x in range(len(lista)):
      suma=suma+lista[x]
   return suma

def nice_list(lista):
   for x in range(len(lista)):
    print(lista[x])

def index(request):
    context = {}
    return render(request, 'khb/index.html', context)

def index1(request):
    post_iteracje=request.POST['iteracje']
    post_capacity=request.POST['capacity']
    zakres_rozwiazan=20
    zakres_paczek_w_rozwiazaniu=10
    hm = [] #harmonic memory
    ilosc_iteracji = (int(post_iteracje)) 
    fp = [] #funkcja przystosowania
    capacityMax=(int(post_capacity))  #cm^3
    iteracja=0
    hmcr=70
    temp=0
    temp_list=[]
    new_hm_row=[]
    allData = [] # all json data 20000 records
    suma=0
    capacityCheck=0
    minFP=0
    toChange=0
    loopFailCheck=0
    par=15
    randomValue=0

    with open('hm.json') as f:
        hm = json.load(f)

    with open('hm.json') as f:
        hm0 = json.load(f)
    
    with open('dataSet.json') as f:
        allData = json.load(f)

    #tworzymy macierz FP dla danych z pliku hm.json
    for x in range(20):
        fp.append(fitness(sum(hm[x]),capacityMax))

    fp0=fp.copy()
  

    while(iteracja<ilosc_iteracji):
        #HMCR
        r1=random.randint(1,100)
        r2=random.randint(1,100)
        if(r1<hmcr):
            while(temp<zakres_paczek_w_rozwiazaniu):
                for x in range(zakres_rozwiazan):
                    temp_list.append(hm[x][temp])
                value=random.choice(temp_list)
                if(capacityCheck+value<=capacityMax):
                    new_hm_row.append(value)
                    temp=temp+1
                    capacityCheck=capacityCheck+value
                else:
                    loopFailCheck=loopFailCheck+1
                if(loopFailCheck==15):
                    new_hm_row.clear()
                    capacityCheck=0
                    temp=0
                    loopFailCheck=0
            #PAR
            if(r2<par):
                randomNumber=random.randint(0,19999)
                tempVolume=float(allData[randomNumber]['sizeX'])*float(allData[randomNumber]['sizeY'])*float(allData[randomNumber]['sizeZ'])
                tempVolume=round(tempVolume,2)
                if(tempVolume+capacityCheck>capacityMax):
                    while(tempVolume+capacityCheck<capacityMax):
                        randomValue=random.randint(0,len(new_hm_row))
                        randomNumber=random.randint(0,19999)
                        tempVolume=float(allData[randomNumber]['sizeX'])*float(allData[randomNumber]['sizeY'])*float(allData[randomNumber]['sizeZ'])
                        tempVolume=round(tempVolume,2)
                        if(tempVolume+capacityCheck<capacityMax):
                            new_hm_row[randomValue]=tempVolume
            temp_list.clear()
        else:
            while(temp<zakres_paczek_w_rozwiazaniu):
                randomNumber=random.randint(0,19999)
                tempVolume=float(allData[randomNumber]['sizeX'])*float(allData[randomNumber]['sizeY'])*float(allData[randomNumber]['sizeZ'])
                tempVolume=round(tempVolume,2)
                if(capacityCheck+tempVolume<=capacityMax):
                    temp=temp+1
                    new_hm_row.append(tempVolume)
                    capacityCheck=capacityCheck+tempVolume
                else:
                    loopFailCheck=loopFailCheck+1
                if(loopFailCheck==15):
                    new_hm_row.clear()
                    capacityCheck=0
                    temp=0
                    loopFailCheck=0
                tempVolume=0

        #policzenie funkcji przystosowania
        difference=abs(fitness(sum(new_hm_row),capacityMax))

        for x in range(len(fp)):
            if(fp[x]>minFP):
                minFP=fp[x]
                toChange=x

        if(difference<minFP):
            for x in range(len(new_hm_row)):
                hm[toChange][x]=new_hm_row[x]
            fp[toChange]=fitness(sum(new_hm_row),capacityMax)

        temp=0
        new_hm_row.clear()
        temp_list.clear()
        iteracja=iteracja+1
        capacityCheck=0
        minFP=0
        loopFailCheck=0

    
    najValues = hm[fp.index(min(fp))]
    naj = sum(hm[fp.index(min(fp))])
    context = {'naj':naj,'najValues':najValues,'fp':fp,'hm':hm,'fp0':fp0,'hm0':hm0}
    return render(request, 'khb/index1.html', context)

