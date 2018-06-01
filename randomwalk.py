import numpy as np
import matplotlib.pyplot as plt 

rands = np.random.randint(0,1,1000)
walk = np.where(rands > 0,1,-1)
walks = walk.cumsum()
plt.plot(walks)
plt.title('Random Walk')
plt.xlabel('Step')
plt.ylabel('position')

