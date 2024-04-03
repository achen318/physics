# library
import matplotlib.pyplot as plt
import numpy as np

# Get the data
data = np.loadtxt("e_field.csv", delimiter=",")

# Create contour
plt.contour(data, levels=20, cmap="RdBu_r")
plt.show()
