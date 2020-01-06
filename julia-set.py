import cmath
import numpy
from matplotlib import pyplot as plt 

n_iter = 20
step = 0.01

def f(z,c):
    return z**2 + c

def Julia(c):
    xlist = [] 
    ylist = []     
    for x in numpy.arange(-1.6,1.6,step):
        for y in numpy.arange(-1.6,1.6,step):
            z = complex(x,y)
            for idx in range(0,n_iter):
                if abs(z) > 2:
                    xlist.append(x)
                    ylist.append(y)
                    break
                else:
                    z = f(z,c)
    plt.scatter(xlist, ylist, s=1.5) 
    plt.show()
    
c = complex(0.18, 0.5)
Julia(c)

