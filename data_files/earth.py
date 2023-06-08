import numpy as np

data=np.loadtxt('earthq_sicilia.dat', delimiter='|', dtype='str')
magn=data[:,10]