import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 0.5, 0.01)
y_linear = x*100
y_hal = -0.5*np.log(1-2*x)*100
y_kos = 0.25*np.log((1+2*x)/(1-2*x))*100

ellie0 = [0.425, 42.5]
ellie = [0.425, 62.80764]
ellie1 = [0.425, 94.86]

plt.plot(y_linear, x, "b-")
plt.plot(y_hal, x, "r-")
plt.plot(y_kos, x, "g-")
plt.plot(ellie0[1], ellie0[0], "kx")
plt.plot(ellie[1], ellie[0], "kx")
plt.plot(ellie1[1], ellie[0], "kx")

plt.show()