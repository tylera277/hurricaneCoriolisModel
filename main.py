# +this is a good tool to use to plot the hurricane data onto,
# with it being a pretty looking graphic and simple plotting.
# + Now I need to either automate the plot of the entire
# path of the hurricane or

import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from sideFunctions import getCoriolisAcc

# for globe:
plt.figure(figsize=(8, 8))
m = Basemap(projection='ortho', resolution=None, lat_0=20, lon_0=-50)
m.bluemarble(scale=0.5)

# +I'll clean the section below this once I get my plotter of object
# working, no point to do it right now
x, y = m(-18.4, 12.9)
plt.plot(x, y, color='red', marker='+', markersize=5)
x1, y1 = m(-34.6, 17.4)
plt.plot(x1, y1, color='red', marker='+', markersize=5)
x2, y2 = m(-60.0, 25.0)
plt.plot(x2, y2, color='red', marker='+', markersize=5)
x3, y3 = m(-76,33.6)
plt.plot(x3, y3, color='red', marker='+', markersize=5)

# path which is a line across the earth at a constant latitude
for i in range(-18, -100, -2):

    x10, y10 = m(i, 13.0)
    plt.plot(x10, y10, color='m', marker='+', markersize=5)

for j in range(0, 24, 1):
    pass


# radius of earth in km
rEarth = 6.371 * 10 ** 3
# angular velocity of earth in rad/hour
wEarth = 0.2617
# +initial position's latitude and longitude of the object \
# I want to simulate moving on earth's surface.
# + I am choosing around where the hurricane originated

initial_position = [-18.4, 12.9]

# + steps which convert initial coordinates. to positions
x = rEarth * math.cos(math.radians(initial_position[1])) * math.sin(math.radians(initial_position[0]))
y = rEarth * math.sin(math.radians(initial_position[1])) * math.sin(math.radians(initial_position[0]))
z = rEarth * math.cos(math.radians(initial_position[0]))
# print('x,y:',x,y)
position = [x, y, z]
print(position)
initialVelocity = [0, -20.0, -10.0]
velocity = initialVelocity
rotation = [0, 0, wEarth]

# + parameters of the simulation
t = 0
tEnd = 500
dt = 0.1

phiHigh = 0.0
thetaHigh = 0.0

# Initializing some arrays to use later, mainly used to store values
i = 0
angles = np.zeros((int(tEnd/dt), 2))
change = np.zeros((int(tEnd/dt), 2))
savePosition = np.zeros((int(tEnd/dt), 3))
saveVelocity = np.zeros((int(tEnd/dt), 3))
saveAcceleration = np.zeros((int(tEnd/dt), 3))

while t < tEnd:
    acceleration = getCoriolisAcc(velocity, rotation)
    # print(acceleration)

    velocity += np.multiply(np.multiply(acceleration, dt), 1.0 / 2.0)
    position += np.multiply(velocity, dt)

    acceleration = getCoriolisAcc(velocity, rotation)
    velocity += np.multiply(np.multiply(acceleration, dt), 1.0 / 2.0)

    # + saving values for plotting later
    savePosition[i] = position
    saveVelocity[i] = velocity
    saveAcceleration[i] = acceleration

    theta = math.degrees(math.acos((position[2]) / rEarth))

    phi = math.degrees(math.atan(position[1] / position[0]))
    # for plotting on globe
    angles[i][0] = phi
    angles[i][1] = theta

    t += dt
    i += 1

# +calculates the change between angle values and stores it into a new array, one for
# theta and one for phi
for k in range(1, int(tEnd/dt)):
    change[k][0] = angles[k][0] - angles[k-1][0]
    change[k][1] = angles[k][1] - angles[k-1][1]


for j in range(5, int(tEnd/dt)-1, 1):

    # + conditions which make a more accurate plot I believe
    if saveAcceleration[j][1] > saveAcceleration[j-1][1]:
        if angles[j][0] < angles[j-1][0]:
            x10, y10 = m(-angles[j][1], angles[j][0])
            plt.plot(x10, y10, color='y', marker='+', markersize=1)



plt.show()