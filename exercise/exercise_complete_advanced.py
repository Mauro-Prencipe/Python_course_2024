import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.optimize import curve_fit


class Fit():
    
    dpi=200
    
    def __init__(self):
        self.degree=3
        self.file=None
        self.x=None
        self.y=None
        self.fit=None
        self.flag=False
        self.read_flag=False
        
    def read_data(self, file_name):
        data=np.loadtxt(file_name)
        self.x=data[:,0]
        self.y=data[:,1]
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
        
        plt.figure(self.dpi)
        plt.plot(self.x,self.y,"k*", label="Actual values")
        plt.plot(x_plot, y_poly, "b-", label="Poly fit")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend(frameon=False)
        plt.show()
        
    

if __name__ == '__main__' :
    my_data=Fit()
    my_data.read_data('exercise_data.dat')
    my_data.plot()

  

