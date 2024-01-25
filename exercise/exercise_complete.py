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


def fit():
    fit_poly=np.polyfit(d.x,d.y,3)
    fit_curve=curve_fit(cubic, d.x, d.y)

    x_plot=np.linspace(-4, 4, 40)
    y_poly=np.polyval(fit_poly, x_plot)
    y_curve=cubic(x_plot, *fit_curve[0])
    
    print("Polynomial fit coeff: ", fit_poly)
    print("Curve_fit coeff:      ", fit_curve[0])

    plt.figure()
    plt.plot(d.x,d.y,"k*", label="Actual values")
    plt.plot(x_plot, y_poly, "b-", label="Poly fit")
    plt.plot(x_plot, y_curve, "r--", label="Curve_fit")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend(frameon=False)
    plt.show()


