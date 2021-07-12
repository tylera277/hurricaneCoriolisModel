import numpy as np

def getCoriolisAcc(velocity, rotation):
    acc = 2 * np.cross(velocity, rotation)

    #print(acc)
    return acc
