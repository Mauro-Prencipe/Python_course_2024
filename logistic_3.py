# Static methods definition: use of the decorator @staticmethod
# to define functions within a class that can be called without
# the need to create any instance of the class itself.

# The Logistic class is defined for such purpose. It groups all
# the functions needed to deal with the logist problem.
# In this case there is no a __init__ constructor, and
# all the relevant variables(that is, relevant for the 
# calculation) are class attribute (instead of instance 
# attributes).
# All the functions of the class are declared as 
# static methods by using the appropriate decorator. Such
# functions have not a self argument and directly manipulate
# the class attributes


# Logistic equation

import numpy as np
import matplotlib.pyplot as plt

class Logistic:
      x0=0.1
      k=2.5
      niter=5000
      last=100
      digits=5
      x_last=[]
      sx=None
    
      @staticmethod  
      def logistic_function():
          
          x=Logistic.x0
          
          for _ in range(Logistic.niter):
              ix=Logistic.k*x*(1-x)
              x=ix   
              ix=round(ix, Logistic.digits)
                            
              yield ix             
      
      @staticmethod
      def count():
          
          x_list_generator=Logistic.logistic_function()
          
          for _ in range(Logistic.niter-Logistic.last):
              next(x_list_generator)
              
          Logistic.x_last=[]    
          for _ in range(Logistic.last):
              xl=next(x_list_generator)
              Logistic.x_last.append(xl)
              
          sx=set(Logistic.x_last)
          Logistic.sx=sx
      
      @staticmethod
      def get_stable_points_set(k):
          Logistic.set_k(k)
          Logistic.count()
          
          return Logistic.sx    
       
      @staticmethod
      def set_k(k):
          Logistic.k=k 
       
      @staticmethod
      def get_k():
          return Logistic.k
       
      @staticmethod
      def set_param(xini=0.1, niter=5000, last=100, digits=5):
          Logistic.x0=xini
          Logistic.niter=niter
          Logistic.last=last
          Logistic.digits=digits
       
      @staticmethod    
      def get_niter():
          return Logistic.niter
       
      @staticmethod
      def plot(k=2.5, niter=30, bins=20, hist=False):
          
          k_orig=Logistic.get_k()
          niter_orig=Logistic.get_niter()
          
          Logistic.set_param(niter=niter)
          Logistic.set_k(k)
          
          x_list_generator=Logistic.logistic_function()
          x_list=list(x_list_generator)
          
          Logistic.set_param(niter=niter_orig)
          Logistic.k=k_orig
          
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
          

# The function plot makes use of the Logistic.get_stable_point_set
# directly; that is, there is non need to create an instance
# of the Logistic class, and then call the method associated 
# with that instance.

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
        isx=Logistic.get_stable_points_set(ik)
        isx_size=len(isx)
        ik_list=np.repeat(ik, isx_size)
        is_list=list(isx)
        plt.plot(ik_list, is_list, "k.", markersize=2)
    
    plt.xlim(kmin, kmax)
    plt.xlabel("K")
    plt.ylabel("X")
    plt.show()
    