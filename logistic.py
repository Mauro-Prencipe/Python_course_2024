# Logistic equation

import numpy as np
import matplotlib.pyplot as plt

class Logistic():
      def __init__(self):
          self.x0=0.1
          self.k=2.5
          self.niter=5000
          self.last=100
          self.digits=5
          self.x_list=[]
          self.x_last=[]
          self.sx=None
          
      def logistic_function(self):
          
          x=self.x0
          x_list=[]
          for it in range(self.niter):
              ix=self.k*x*(1-x)

              if ix <= 0.0001:
                 ix=0.0001
                  
              ix=round(ix, self.digits)
              x_list.append(ix)
              x=ix
          
          self.x_list=x_list
             
      def count(self):
          
          x_list=self.logistic_function()
          start_x=len(self.x_list)-self.last
          x_last=self.x_list[start_x:]
          self.x_last=x_last
          sx=set(x_last)
          self.sx=sx
          
      def set_k(self,k):
          self.k=k   
          
      def set_param(self, xini=0.1, niter=5000, last=100, digits=5):
          self.x0=xini
          self.niter=niter
          self.last=last
          self.digits=digits
          

lgs=Logistic()

def get_ss(k):
    lgs.set_k(k)
    lgs.count()
    
    return lgs.sx

def plot(kmin, kmax, npoints=100):
    
    k_list=np.linspace(kmin, kmax, npoints)
    
    plt.figure(dpi=100)
    
    for ik in k_list:
        isx=get_ss(ik)
        isx_size=len(isx)
        ik_list=np.repeat(ik, isx_size)
        is_list=list(isx)
        plt.plot(ik_list, is_list, "k.", markersize=2)
    
    plt.xlim(kmin, kmax)
    plt.xlabel("K")
    plt.ylabel("X")
    plt.show()
    