# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 20:56:22 2020

@author: cyang
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os, glob
import seaborn as sns
#sns.set(style="darkgrid")

#from usgsGroundwaterR import USGSgroundwater

#from Modelingsimulations import Modelingsimulations

#from Macadataprocessing import Macadataprocessing


class Macadata:



    
    def __init__(self,basin,filepath,zone,rcp,ipunit=1,itunit=1,iplot=False): #,monthlyP,monthlyT,dailyP,dailyT):
        self.basin=basin
        self.filepath=filepath
        self.zone=zone
        self.rcp=rcp
        self.ipunit=ipunit    # 1 for inches, # 2 for mm
        self.itunit=itunit     # 1 for oC, # 2 for oF, #3 for Kelvn
        self.iplot=iplot
        self.dailyP, self.dailyT=self.obtain_dailydata()
        self.monthlyP, self.monthlyT=self.obtain_monthlyData()
        self.annualmeanP, self.annualmeanT=self.obtain_annualmeanData()
        


    def obtain_dailydata(self):  #,basin,rcp,filepath,zone,iplot):

        pathnew=os.path.join(self.filepath,'dataT')
        self.dailyT=self.Concate_dailydata(pathnew) #,self.basin,rcp=self.rcp,zone=self.zone) #pathnew,basin=self.basin,rcp=self.rcp,zone=self.zone)  ## daily data
        if self.itunit==1:
            self.dailyT=self.dailyT - 273.15   # from Kelvn to oC
        if self.itunit==2:   
            self.dailyT=(self.dailyT - 273.15)*9.0/5.0+32.0

		
        pathnew=os.path.join(self.filepath,'dataPre')
        self.dailyP=self.Concate_dailydata(pathnew) #,basin=self.basin,rcp=self.rcp,zone=self.zone)  ## daily data
        
        if self.ipunit==1:
            self.dailyP=self.dailyP*0.0393701   # convert to inches
        return self.dailyP, self.dailyT 

         

    def read_dailydata(self,fileb,zone='Recharge'):
   # print('In reading_data_rch ',zone)
   # print(fileb)
        data=pd.read_csv(fileb)
        data['Datetime']=pd.to_datetime(data['Datetime'])
        data=data.set_index('Datetime')
        rechColname=[col for col in data.columns if zone in col]
        newrechColname=[col.split('_')[2] for col in rechColname]
        df=data[rechColname]
        df.columns=newrechColname
        
        return df
    

    def Concate_dailydata(self,filepath):  #,filepath,basin,rcp,zone='Recharge'):
        
        os.chdir(filepath)
        csvftemp=glob.glob('*.csv')   
    #    print('in reading_concating_data ',zone)
        for file in csvftemp:
            if (self.basin in file) and ('hist' in file):
                histfile=os.path.join(filepath,file)
            if (self.basin in file) and (self.rcp in file):
                rcpfile=os.path.join(filepath,file)
        
        histdf=self.read_dailydata(histfile,self.zone)
        projdf=self.read_dailydata(rcpfile,self.zone)
        
        dailydf=pd.concat([histdf,projdf],axis=0)
        
        
        return dailydf
   

    
    def obtain_monthlyData(self): #,basin,rcp,filepath,iplot,zone):
        

    #     self.obtain_dailydata()

         self.monthlyT=self.dailyT.resample('M').mean()   ## monthly mean and convert to oC

         self.monthlyP=self.dailyP.resample('M').sum()             ## monthly precipitation 

         if self.iplot is True:   
            self.drawplot_raw()    
        
         return self.monthlyP,self.monthlyT   
        

    def obtain_annualmeanData(self): #,basin,rcp,filepath,iplot,zone):
        

   #      self.obtain_monthlyData()

         self.annualmeanT=self.dailyT.resample('Y').mean()   ## monthly mean and convert to oC

         self.annualmeanP=self.dailyP.resample('Y').sum()             ## monthly precipitation 

         if self.iplot is True:   
            self.drawplot_raw()    
        
         return self.annualmeanP,self.annualmeanT   




        