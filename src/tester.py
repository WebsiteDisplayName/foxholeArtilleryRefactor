import controller as cT
import math


if __name__ == "__main__":
    azimuthDeflection = 30
    offsetMetersDeflection = 6
    distGI = 6

    # adjacentAngleRadians = math.radians(90-azimuthDeflection/2)
    # sideLength = (offsetMetersDeflection/2)/math.cos(adjacentAngleRadians) #inputs radians
    # print(sideLength)

    newAzimuthDeflection = math.degrees(math.acos((2*distGI**2 - offsetMetersDeflection**2)/(2*distGI**2)))
    
    # newVal = math.sin(math.radians(azimuthDeflection))*distGI

    # print(newVal)
    print(newAzimuthDeflection)