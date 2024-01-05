import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
import plot 

class einstein_class():
    def __init__(self):
        self.avo=6.02214179e+23
        self.kb=1.3806505e-23
        self.apfu=1
        
    def einstein_fun(self, tt, eps):    
        return self.apfu*3*self.avo*self.kb*((eps/tt)**2)*np.exp(eps/tt)/((np.exp(eps/tt)-1)**2)
    
    def einstein_2_fun(self,tt,eps1,eps2):
        f1=self.apfu*3*self.avo*self.kb/2.
        f2=((eps1/tt)**2)*np.exp(eps1/tt)/((np.exp(eps1/tt)-1)**2)
        f3=((eps2/tt)**2)*np.exp(eps2/tt)/((np.exp(eps2/tt)-1)**2)
        return f1*(f2+f3)
    
class data_class():
    def __init__(self, name, filename, apfu):
        self.name=name
        self.filename=filename
        self.path='.'
        self.apfu=apfu
        self.x_orig=np.array([])
        self.y_orig=np.array([])
        self.x=np.array([])
        self.y=np.array([])
        self.minx=0.
        self.maxx=0.
        self.num=0
        self.guess=50.
        self.bounds=(10., 2500.)
        self.model=1
        self.fit1=[]
        self.fit2=[]
        self.fit_flag=[False, False]
        self.n_plot=100
        self.selection_flag=False
        
    def read(self, path='default'):
        
        if path == 'default':
           path=self.path
        
        filename=path+'/'+self.filename
        data=np.loadtxt(filename)
        self.x_orig=data[:,0]
        self.y_orig=data[:,1]
        
        self.minx=np.min(self.x_orig)
        self.maxx=np.max(self.x_orig)
        
        self.num=self.x_orig.size
        
        self.x=np.copy(self.x_orig)
        self.y=np.copy(self.y_orig)
        self.selection_flag=False
        
    def select(self, tmin, tmax=0):
        
        if tmax == 0:
           tmax=self.maxx
        
        select=(self.x_orig >= tmin) & (self.x_orig <= tmax)
        self.x=self.x_orig[select]
        self.y=self.y_orig[select]
        self.fit_flag=[False, False]
        
        self.minx=np.min(self.x)
        self.maxx=np.max(self.x)
        self.selection_flag=True
        self.selection_min=tmin
        self.selection_max=tmax
        
    def info(self):
        print("Data set name %s" % self.name)
        print("Data set file %s" % self.filename)
        print("apfu: %4i" % self.apfu)
        print("Number of T points: %4i" % self.num)
        
        if self.selection_flag:
           print("Original temperature range restricted to the [%5.1f, %5.1f K] interval" \
                 % (self.selection_min, self.selection_max))
            
        print("Minimum and maximum temperatures: %5.1f, %5.1f" % (self.minx, self.maxx))
        if not (self.fit_flag[0] | self.fit_flag[1]):
           print("Fitting model:  None")
        else:
           if self.fit_flag[0]:
              print("one temperature model; Einstein temperature: %5.1f (K)" % self.fit1[0])
           if self.fit_flag[1]:
              print("two temperatures model; Einstein temperatures: %5.1f, %5.1f (K)" % (self.fit2[0], self.fit2[1]))


ein=einstein_class()
my_plot=plot.plot_class('data_files')

def einstein_fit(name, model=1):

    ein.apfu=name.apfu
    guess=name.guess
    bounds=name.bounds
    
    if model==1:    
       guess=[guess]
       ein_fit, ein_cov=curve_fit(ein.einstein_fun, name.x, name.y, bounds=bounds,\
                      p0=guess, xtol=1e-15, ftol=1e-15)
    else:
       guess=[guess, guess]
       ein_fit, ein_cov=curve_fit(ein.einstein_2_fun, name.x, name.y, bounds=bounds,\
                      p0=guess, xtol=1e-15, ftol=1e-15)
        
    if model == 1:
       print("Einstein temperature:   %5.1f (K)" % ein_fit[0])
    else:        
       print("Einstein temperatures:  %5.1f, %5.1f (K)" % (ein_fit[0], ein_fit[1]))
    
    if model == 1: 
       name.model=1
       name.fit1=[ein_fit[0]]
       name.fit_flag[0]=True
    else:
       name.model=2
       name.fit2=[ein_fit[0], ein_fit[1]]
       name.fit_flag[1]=True
       
def plot_fit(name):
    
    t_plot=np.linspace(name.minx, name.maxx, name.n_plot)
    
    cv1_plot=np.array([ein.einstein_fun(it, name.fit1[0]) for it in t_plot])
    cv2_plot=np.array([ein.einstein_2_fun(it, name.fit2[0], name.fit2[1]) for it in t_plot])
    
    x=[name.x, t_plot, t_plot]
    y=[name.y, cv1_plot, cv2_plot]
    style=['k*', 'k--', 'k-']
    label=['Actual values', '1p fit', '2p fit']
    
    my_plot.multi(x,y,style, label, xlab=r'$T (K)$', ylab=r'$C_v (J/mol\ J)$')
    
def compare_fit(name, plot=True):
    
    if not name.fit_flag[0]:
       einstein_fit(name, model=1)
    if not name.fit_flag[1]:
       einstein_fit(name, model=2)
    
    print("")
    model1=np.array([ein.einstein_fun(it, name.fit1[0]) for it in name.x])
    model2=np.array([ein.einstein_2_fun(it, name.fit2[0], name.fit2[1]) for it in name.x])
    
    serie=[name.x, name.y, model1.round(2), model2.round(2)]
    df=pd.DataFrame(serie, index=['T  ', '   Cv Exp', ' model 1', ' model 2'])
    df=df.T
    print(df.to_string(index=False), '\n')  
    
    if plot:
       plot_fit(name)