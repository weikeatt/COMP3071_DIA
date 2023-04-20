import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

x = [0, 500, 1000, 1500, 2000, 2500, 3000]
y = [-11132, -242, -204, -164, -159, -136, -136]
z = [0.994433999999222, 0.6248354999475603, 0.5230369999333311, 0.4465134999345112, 0.38261149993976823, 0.3261064999444167, 0.2736189999487347]

ax = plt.axes(projection = "3d")
ax.plot3D(x, y, z)
ax.set_xlabel("Episode Number")
ax.set_ylabel("Best Rewards")
ax.set_zlabel("Epsilon Value")
plt.show()
