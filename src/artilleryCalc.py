# use classes because some data needs to persist until changed
import pandas as pd
import math


def findTSGAngle(spotterToTargetAzimuth, spotterToGunAzimuth):
    azimuthArray = [spotterToTargetAzimuth, spotterToGunAzimuth]
    aziMin = min(azimuthArray)
    aziMax = max(azimuthArray)

    if (aziMax - aziMin) >= 180:
        return 360 - (aziMax - aziMin)
    else:
        return (aziMax - aziMin)


def findDistanceGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance):
    dST = spotterToTargetDistance
    dSG = spotterToGunDistance
    aTSG = findTSGAngle(spotterToTargetAzimuth, spotterToGunAzimuth)

    distGunToTarget = math.sqrt(
        dST**2 + dSG**2 - 2*dST*dSG*math.cos(math.radians(aTSG)))

    return distGunToTarget


def findTGSAngle(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance):
    dGT = findDistanceGunToTarget(
        spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance)
    dST = spotterToTargetDistance
    dSG = spotterToGunDistance

    aTGS = math.degrees(math.acos((dGT**2 + dSG**2 - dST**2)/(2*dGT*dSG)))
    return aTGS


def findAzimuthGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance):
    aTGS = findTGSAngle(spotterToTargetAzimuth, spotterToTargetDistance,
                        spotterToGunAzimuth, spotterToGunDistance)
    aTSG = findTSGAngle(spotterToTargetAzimuth, spotterToGunAzimuth)
    aSTG = 180 - (aTGS + aTSG)
    aziSG = spotterToGunAzimuth
    aziST = spotterToTargetAzimuth

    if (aziSG >= 180) and (aziST < 180) and (aziSG - 180 > aziST):
        result = (aziSG - 180) - aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result

    elif (aziSG >= 180) and (aziST < 180) and (aziSG - 180 < aziST):
        result = (aziSG - 180) + aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result

    elif (aziSG < 180) and (aziST >= 180) and (aziSG + 180 > aziST):
        result = (aziSG + 180) - aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result

    elif (aziSG < 180) and (aziST >= 180) and (aziSG + 180 < aziST):
        result = (aziSG + 180) + aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result

    elif (aziSG >= 180) and (aziST >= 180) and (aziSG > aziST):
        result = (aziSG - 180) + aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result

    elif (aziSG >= 180) and (aziST >= 180) and (aziSG < aziST):
        result = (aziSG - 180) - aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result

    elif (aziSG < 180) and (aziST < 180) and (aziSG > aziST):
        result = (aziSG + 180) + aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result

    elif (aziSG < 180) and (aziST < 180) and (aziSG < aziST):
        result = (aziSG + 180) - aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result


if __name__ == "__main__":
    pass
