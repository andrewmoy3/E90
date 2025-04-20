import matplotlib.pyplot as plt


import numpy as np


arr = np.arange(1000)
print(arr)

plt.scatter(arr, arr, c='black', marker='o')
plt.show()