import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.optimize import curve_fit

data=np.loadtxt('exercise_data.dat')
x=data[:,0]
y=data[:,1]


def cubic(x, a, b, c):
    return a*x**3 + b*x + c


def fit():
    fit_poly=np.polyfit(x,y,3)
    fit_curve=curve_fit(cubic, x, y)

    x_plot=np.linspace(-4, 4, 40)
    y_poly=np.polyval(fit_poly, x_plot)
    y_curve=cubic(x_plot, *fit_curve[0])
    
    print("Polynomial fit coeff: ", fit_poly)
    print("Curve_fit coeff:      ", fit_curve[0])

    plt.figure()
    plt.plot(x,y,"k*", label="Actual values")
    plt.plot(x_plot, y_poly, "b-", label="Poly fit")
    plt.plot(x_plot, y_curve, "r--", label="Curve_fit")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend(frameon=False)
    plt.show()


