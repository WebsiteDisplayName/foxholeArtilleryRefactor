# use classes because some data needs to persist until changed
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
    try:
        aTGS = math.degrees(math.acos((dGT**2 + dSG**2 - dST**2)/(2*dGT*dSG)))
        return aTGS
    except:
        return 0


def findAzimuthGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance):
    aTGS = findTGSAngle(spotterToTargetAzimuth, spotterToTargetDistance,
                        spotterToGunAzimuth, spotterToGunDistance)
    aTSG = findTSGAngle(spotterToTargetAzimuth, spotterToGunAzimuth)
    aSTG = 180 - (aTGS + aTSG)
    aziSG = spotterToGunAzimuth
    aziST = spotterToTargetAzimuth

    if aTGS == 0:  # return backazimuth of spotterToGun
        if spotterToGunDistance == 0:
            return spotterToTargetAzimuth
        elif spotterToTargetDistance == 0:
            return spotterToGunAzimuth + 180 if spotterToGunAzimuth <= 180 else spotterToGunAzimuth - 180
        elif spotterToTargetAzimuth != spotterToGunAzimuth:
            return spotterToTargetAzimuth
        else:
            if spotterToTargetAzimuth >= 180:
                return spotterToTargetAzimuth - 180
            else:
                return spotterToTargetAzimuth + 180
    elif (aziSG >= 180) and (aziST <= 180) and (aziSG - 180 > aziST):
        result = (aziSG - 180) - aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result

    elif (aziSG >= 180) and (aziST <= 180) and (aziSG - 180 < aziST):
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

    elif (aziSG < 180) and (aziST < 180) and (aziSG <= aziST):
        result = (aziSG + 180) - aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result


# weapon type
    # 1 = normal artillery (i.e. 120mm & 150mm)
    # 2 = storm cannon (i.e. 300mm)
    # 3 = mortars


def findWindAdjustedGunToTargetAziDist(unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, windAzimuth, windForce, weaponType):
    # target takes the spotter role in the triangle calculation
    # adjustedTarget takes the role of target in the triangle calculation
    # accounts for wind force 1-3

    # oppositeWindAzimuth is the back azimuth of windAzimuth
    if windAzimuth < 180:
        oppositeWindAzimuth = windAzimuth + 180
    elif windAzimuth >= 180:
        oppositeWindAzimuth = windAzimuth - 180

    # ******* add more weapon types and windForce to meter conversions whenever possible *******
    if weaponType == 1:  # 120mm & 150mm
        windForceMetersArray = [0, 15, 30]
    elif weaponType == 2:  # storm cannon
        windForceMetersArray = [0, 125, 250]
    elif weaponType == 3:  # mortars
        windForceMetersArray = [0, 10, 20]

    # spotterToGunAzimuth is unadjustedGunToTarget back azimuth
    if unadjustedGunToTargetAzimuth < 180:
        targetToGunAzimuth = unadjustedGunToTargetAzimuth + 180
    else:
        targetToGunAzimuth = unadjustedGunToTargetAzimuth - 180
    
    try:
        extractedWF = float(windForce[5:])
        adjustedGunToTargetAzimuth = findAzimuthGunToTarget(
            oppositeWindAzimuth, extractedWF, targetToGunAzimuth, unadjustedGunToTargetDistance)
        adjustedGunToTargetDist = findDistanceGunToTarget(
            oppositeWindAzimuth, extractedWF, targetToGunAzimuth, unadjustedGunToTargetDistance)

    except:
        windForce = int(windForce)
        adjustedGunToTargetAzimuth = findAzimuthGunToTarget(
            oppositeWindAzimuth, windForceMetersArray[windForce-1], targetToGunAzimuth, unadjustedGunToTargetDistance)
        adjustedGunToTargetDist = findDistanceGunToTarget(
            oppositeWindAzimuth, windForceMetersArray[windForce-1], targetToGunAzimuth, unadjustedGunToTargetDistance)
        if windForceMetersArray[windForce-1] == 0:
            adjustedGunToTargetAzimuth = unadjustedGunToTargetAzimuth
        print(adjustedGunToTargetDist, adjustedGunToTargetAzimuth)



    return [unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, adjustedGunToTargetAzimuth, adjustedGunToTargetDist]


def comprehensiveSpotterArtillery(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance, windAzimuth, windForce, weaponType):
    unadjustedGunToTargetAzimuth = findAzimuthGunToTarget(
        spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance)
    unadjustedGunToTargetDistance = findDistanceGunToTarget(
        spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance)

    return findWindAdjustedGunToTargetAziDist(unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, windAzimuth, windForce, weaponType)

# ouputs [impliedWindAzimuth, impliedWindDriftMeters]


def findImpliedWindAziDist(gunToImpactAzi, gunToImpactDist, gunToTargetAzi, gunToTargetDist):
    impliedWindAzimuth = findAzimuthGunToTarget(
        gunToImpactAzi, gunToImpactDist, gunToTargetAzi, gunToTargetDist)
    impliedWindDriftMeters = findDistanceGunToTarget(
        gunToImpactAzi, gunToImpactDist, gunToTargetAzi, gunToTargetDist)
    return [impliedWindAzimuth, impliedWindDriftMeters]


def findImpliedWindAdjustedGunToTargetAziDist(unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, impliedWindAzimuth, impliedWindDriftMeters):
    # target takes the spotter role in the triangle calculation
    # adjustedTarget takes the role of target in the triangle calculation
    # accounts for wind force 1-3

    # oppositeWindAzimuth is the back azimuth of impliedWindAzimuth
    if impliedWindAzimuth < 180:
        oppositeWindAzimuth = impliedWindAzimuth + 180
    elif impliedWindAzimuth >= 180:
        oppositeWindAzimuth = impliedWindAzimuth - 180

    # spotterToGunAzimuth is unadjustedGunToTarget back azimuth
    if unadjustedGunToTargetAzimuth < 180:
        targetToGunAzimuth = unadjustedGunToTargetAzimuth + 180
    else:
        targetToGunAzimuth = unadjustedGunToTargetAzimuth - 180

    adjustedGunToTargetAzimuth = findAzimuthGunToTarget(
        oppositeWindAzimuth, impliedWindDriftMeters, targetToGunAzimuth, unadjustedGunToTargetDistance)
    adjustedGunToTargetDist = findDistanceGunToTarget(
        oppositeWindAzimuth, impliedWindDriftMeters, targetToGunAzimuth, unadjustedGunToTargetDistance)
    return [unadjustedGunToTargetAzimuth, unadjustedGunToTargetDistance, adjustedGunToTargetAzimuth, adjustedGunToTargetDist]


if __name__ == "__main__":
    # tempVar = findDistanceGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance)
    # tempVar2 = findAzimuthGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance)
    # tempVar2 = findAzimuthGunToTarget(323.13, 5, 270, 3)
    # tempVar = findDistanceGunToTarget(153, 180, 0, 0)
    # tempVar2 = findAzimuthGunToTarget(153, 180, 0, 0)
    tempVar = findDistanceGunToTarget(299, 157, 0, 0)
    tempVar2 = findAzimuthGunToTarget(299, 157, 0, 0)
    print(tempVar)
    print(tempVar2)

    # create firingSolution class, write helper definitions outside of class, inside class write functions to change instance variables & calls helper functions
    # calcHelper is functions outside of class, create new .py file for class & instance variable etc, import calcHelper
    pass
