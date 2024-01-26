import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit


class Fit():
    
    dpi=80
    
    def __init__(self):
        self.degree=3
        self.file=None
        self.x=None
        self.y=None
        self.size=None
        self.fit=None
        self.flag=False
        self.read_flag=False
        
    @classmethod    
    def set_dpi(cls, dpi):
        cls.dpi=dpi
        
    def set_degree(self, degree):
        self.degree=degree
        
    def read_data(self, file_name):
        data=np.loadtxt(file_name)
        self.file=file_name
        self.x=data[:,0]
        self.y=data[:,1]
        self.size=len(self.x)
        self.read_flag=True
        
    def polyfit(self):
        if not self.read_flag:
            print("No data file loaded")
            return 
        
        self.flag=True
        self.fit=np.polyfit(self.x, self.y, self.degree)
        
        print("Polynomial fit coeff's': ", self.fit)
        
    def plot(self, xmin='default', xmax='default', npoint=100):
        
        if not self.read_flag:
            print("No data file loaded")
            return
            
        if not self.flag:
            self.polyfit()
            self.flag=True
            
        if xmin=='default':
            xmin=np.min(self.x)
            
        if xmax=='default':
            xmax=np.max(self.x)   
            
        x_plot=np.linspace(xmin, xmax, npoint)
        y_poly=np.polyval(self.fit, x_plot)
        
        plt.figure(dpi=self.dpi)
        plt.plot(self.x,self.y,"k*", label="Actual values")
        plt.plot(x_plot, y_poly, "b-", label="Poly fit")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend(frameon=False)
        plt.show()
        
    
    def table(self):
        yc=np.polyval(self.fit, self.x)
        diff=self.y-yc
        serie=[self.x.round(2), self.y.round(2), yc.round(2), diff.round(2)]
        
        data_frame=pd.DataFrame(serie, index=['X ', 'Y ', 'Yc ', 'Delta'])
        data_frame=data_frame.T
        print("\n")
        print(data_frame.to_string(index=False), "\n")
        
    def info(self):
        print("\nData set file:         ", self.file)
        print("Number of data:       %3i" % self.size)
        if self.flag==True:
            print("Degree of fit:        %3i" % self.degree)
            cfit=[self.fit[ic].round(4) for ic in range(self.degree+1)]
            print("Polynomial fit coeff's ", cfit)
            
    

def start(my_data_file='exercise_data.dat', degree=3, dpi=100):
    
    my_data=Fit()
    my_data.set_dpi(dpi)
    my_data.set_degree(degree)
    my_data.read_data(my_data_file)
    my_data.plot()
    my_data.table()
    my_data.info()
  

