# This script imports the class Logistic which is contained in the file
# Logistic_class.py, saved in the Logistic_lib folder
#
# Folder structure:
#
# logistic_4.py
# Logistic_lib/
#    __init__.py           # Actually no longer needed
#    Logistic_class.py
#


import numpy as np
import matplotlib.pyplot as plt

# From the library Logistic_lib, import the file (module) Logistic_class.py
# The Logistic_class module is given the Lg alias 

from Logistic_lib import Logistic_class as Lg

# The plot function below references the function get_stable_point_set,
# that is a function of the Logistic class defined in the Logistic_class.py
# file, located in the Logistic_lib folder

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
        isx=Lg.Logistic.get_stable_points_set(ik)
        isx_size=len(isx)
        ik_list=np.repeat(ik, isx_size)
        is_list=list(isx)
        plt.plot(ik_list, is_list, "k.", markersize=2)
    
    plt.xlim(kmin, kmax)
    plt.xlabel("K")
    plt.ylabel("X")
    plt.show()

