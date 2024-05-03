import scipy.interpolate as scipy
import numpy as np
import matplotlib.pyplot as plt

x = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0]

#approxitiom of my data with b-spline
tck = scipy.splrep(x, y, s=0)
xnew = np.arange(-10, 10, 0.1)
ynew = scipy.splev(xnew, tck, der=0)

plt.plot(x, y, 'x', xnew, ynew, xnew, np.sin(xnew), x, y, 'b')
plt.legend(['Linear', 'Cubic Spline', 'True'])
plt.axis([-10, 10, -2, 10])

plt.show()