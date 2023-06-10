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
          self.x_last=[]
          self.sx=None
          
      def logistic_function(self):
          
          x=self.x0
          
          for _ in range(self.niter):
              ix=self.k*x*(1-x)
              x=ix   
              ix=round(ix, self.digits)
                            
              yield ix             
             
      def count(self):
          
          x_list_generator=self.logistic_function()
          
          for _ in range(self.niter-self.last):
              next(x_list_generator)
              
          self.x_last=[]    
          for ix in range(self.last):
              xl=next(x_list_generator)
              self.x_last.append(xl)
              
          sx=set(self.x_last)
          self.sx=sx
          
      def get_stable_points_set(self, k):
          self.set_k(k)
          self.count()
          
          return self.sx    
          
      def set_k(self,k):
          self.k=k 
          
      def get_k(self):
          return self.k
          
      def set_param(self, xini=0.1, niter=5000, last=100, digits=5):
          self.x0=xini
          self.niter=niter
          self.last=last
          self.digits=digits
          
      def get_niter(self):
          return self.niter
          
      def plot(self, k=2.5, niter=30, bins=20, hist=False):
          
          k_orig=self.get_k()
          niter_orig=self.get_niter()
          
          self.set_param(niter=niter)
          self.set_k(k)
          
          x_list_generator=self.logistic_function()
          x_list=list(x_list_generator)
          
          self.set_param(niter=niter_orig)
          self.k=k_orig
          
          it_list=list(range(niter))
          plt.figure(dpi=100)
          if not hist:
             plt.plot(it_list, x_list)
             plt.xlim(0)
             plt.ylim(0,1)
             plt.xlabel("Generation")
             plt.ylabel("X_i")
          else:
             plt.hist(x_list, bins) 
             plt.xlabel("X_i")
             plt.ylabel("Counts")
          plt.show()
          
lgs=Logistic()


def plot(kmin, kmax, npoints=100):
    """
    Plots the logistic graph. Typical value of k to get a bifurcation
    is around 3. 
    
    Try: 
    >>  plot(2.8, 3.6)
    """
    
    k_list=np.linspace(kmin, kmax, npoints)
    
    plt.figure(dpi=100)
    
    for ik in k_list:
        isx=lgs.get_stable_points_set(ik)
        isx_size=len(isx)
        ik_list=np.repeat(ik, isx_size)
        is_list=list(isx)
        plt.plot(ik_list, is_list, "k.", markersize=2)
    
    plt.xlim(kmin, kmax)
    plt.xlabel("K")
    plt.ylabel("X")
    plt.show()
    