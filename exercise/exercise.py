import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.optimize import curve_fit


class Data():

    def __init__(self, x):
        self.x=x
        self.err=[random.gauss(0., sigma=0.1) for ie in range(len(x))]
        self.y = self.compute_y()+self.err
                      
    def compute_y(self):
        y=self.x**3 - 0.8*self.x**2 +2*self.x + 4
        return y 
        

x=np.array([-4, -3, -2., -1., 0., 1., 2., 3.])
d=Data(x)


def cubic(x, a, b, c):
    return a*x**3 + b*x + c




