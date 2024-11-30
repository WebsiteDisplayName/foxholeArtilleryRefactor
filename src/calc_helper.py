# use classes because some data needs to persist until changed
import math
WEAPONTYPEWINDFORCES= {
    # weapon type
    # 1 = normal artillery (i.e. 120mm & 150mm)
    # 2 = storm cannon (i.e. 300mm)
    # 3 = mortars
    "120mm & 150mm": [0, 15, 30],
    "Storm cannon": [0, 125, 250],
    "Mortars": [0, 10, 20]

}


def findTSGAngle(spotter_target_azimuth, spotter_gun_azimuth):
    azimuthArray = [spotter_target_azimuth, spotter_gun_azimuth]
    aziMin = min(azimuthArray)
    aziMax = max(azimuthArray)

    if (aziMax - aziMin) >= 180:
        return 360 - (aziMax - aziMin)
    else:
        return (aziMax - aziMin)


def find_distance_gun_target(spotter_target_azimuth, spotter_target_distance, spotter_gun_azimuth, spotter_gun_distance):
    dST = spotter_target_distance
    dSG = spotter_gun_distance
    aTSG = findTSGAngle(spotter_target_azimuth, spotter_gun_azimuth)

    distGunToTarget = math.sqrt(
        dST**2 + dSG**2 - 2*dST*dSG*math.cos(math.radians(aTSG)))

    return distGunToTarget


def findTGSAngle(spotter_target_azimuth, spotter_target_distance, spotter_gun_azimuth, spotter_gun_distance):
    dGT = find_distance_gun_target(
        spotter_target_azimuth, spotter_target_distance, spotter_gun_azimuth, spotter_gun_distance)
    dST = spotter_target_distance
    dSG = spotter_gun_distance
    try:
        aTGS = math.degrees(math.acos((dGT**2 + dSG**2 - dST**2)/(2*dGT*dSG)))
        return aTGS
    except:
        return 0



def find_azimuth_gun_target(spotter_target_azimuth, spotter_target_distance, spotter_gun_azimuth, spotter_gun_distance):
    aTGS = findTGSAngle(spotter_target_azimuth, spotter_target_distance,
                        spotter_gun_azimuth, spotter_gun_distance)
    aTSG = findTSGAngle(spotter_target_azimuth, spotter_gun_azimuth)
    aSTG = 180 - (aTGS + aTSG)
    azi_sg = spotter_gun_azimuth
    azi_st = spotter_target_azimuth

    if aTGS == 0:  # return backazimuth of spotterToGun
        if spotter_gun_distance == 0:
            return spotter_target_azimuth
        elif spotter_target_distance == 0:
            return spotter_gun_azimuth + 180 if spotter_gun_azimuth <= 180 else spotter_gun_azimuth - 180
        elif spotter_target_azimuth != spotter_gun_azimuth:
            return spotter_target_azimuth
        else:
            if spotter_target_azimuth >= 180:
                return spotter_target_azimuth - 180
            else:
                return spotter_target_azimuth + 180
    elif (azi_sg >= 180) and (azi_st <= 180) and (azi_sg - 180 > azi_st):
        result = (azi_sg - 180) - aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result

    elif (azi_sg >= 180) and (azi_st <= 180) and (azi_sg - 180 < azi_st):
        result = (azi_sg - 180) + aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result

    elif (azi_sg < 180) and (azi_st >= 180) and (azi_sg + 180 > azi_st):
        result = (azi_sg + 180) - aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result
    elif (azi_sg < 180) and (azi_st >= 180) and (azi_sg + 180 < azi_st):
        result = (azi_sg + 180) + aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result

    elif (azi_sg >= 180) and (azi_st >= 180) and (azi_sg > azi_st):
        result = (azi_sg - 180) + aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result

    elif (azi_sg >= 180) and (azi_st >= 180) and (azi_sg < azi_st):
        result = (azi_sg - 180) - aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result

    elif (azi_sg < 180) and (azi_st < 180) and (azi_sg > azi_st):
        result = (azi_sg + 180) + aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result

    elif (azi_sg < 180) and (azi_st < 180) and (azi_sg <= azi_st):
        result = (azi_sg + 180) - aTGS
        if result < 0:
            return (result + 360)
        elif result >= 360:
            return (result - 360)
        else:
            return result




def findWindAdjustedGunToTargetAziDist(unadjusted_gun_target_azimuth, unadjusted_gun_target_distance, wind_azimuth, wind_force, weapon_type):
    # target takes the spotter role in the triangle calculation
    # adjustedTarget takes the role of target in the triangle calculation
    # accounts for wind force 1-3

    # oppositewind_azimuth is the back azimuth of wind_azimuth
    if wind_azimuth < 180:
        oppositewind_azimuth = wind_azimuth + 180
    elif wind_azimuth >= 180:
        oppositewind_azimuth = wind_azimuth - 180

    wind_forceMetersArray = WEAPONTYPEWINDFORCES[weapon_type]

    # spotter_gun_azimuth is unadjustedGunToTarget back azimuth
    if unadjusted_gun_target_azimuth < 180:
        targetToGunAzimuth = unadjusted_gun_target_azimuth + 180
    else:
        targetToGunAzimuth = unadjusted_gun_target_azimuth - 180
    
    try:
        extractedWF = float(wind_force[5:])
        adjusted_gun_target_azimuth = find_azimuth_gun_target(
            oppositewind_azimuth, extractedWF, targetToGunAzimuth, unadjusted_gun_target_distance)
        adjustedGunToTargetDist = find_distance_gun_target(
            oppositewind_azimuth, extractedWF, targetToGunAzimuth, unadjusted_gun_target_distance)

    except:
        wind_force = int(wind_force)
        adjusted_gun_target_azimuth = find_azimuth_gun_target(
            oppositewind_azimuth, wind_forceMetersArray[wind_force-1], targetToGunAzimuth, unadjusted_gun_target_distance)
        adjustedGunToTargetDist = find_distance_gun_target(
            oppositewind_azimuth, wind_forceMetersArray[wind_force-1], targetToGunAzimuth, unadjusted_gun_target_distance)
        if wind_forceMetersArray[wind_force-1] == 0:
            adjusted_gun_target_azimuth = unadjusted_gun_target_azimuth



    return [unadjusted_gun_target_azimuth, unadjusted_gun_target_distance, adjusted_gun_target_azimuth, adjustedGunToTargetDist]


def comprehensiveSpotterArtillery(spotter_target_azimuth, spotter_target_distance, spotter_gun_azimuth, spotter_gun_distance, wind_azimuth, wind_force, weapon_type):
    unadjusted_gun_target_azimuth = find_azimuth_gun_target(
        spotter_target_azimuth, spotter_target_distance, spotter_gun_azimuth, spotter_gun_distance)
    unadjusted_gun_target_distance = find_distance_gun_target(
        spotter_target_azimuth, spotter_target_distance, spotter_gun_azimuth, spotter_gun_distance)

    return findWindAdjustedGunToTargetAziDist(unadjusted_gun_target_azimuth, unadjusted_gun_target_distance, wind_azimuth, wind_force, weapon_type)

# ouputs [impliedwind_azimuth, impliedWindDriftMeters]


def findImpliedWindAziDist(gunToImpactAzi, gunToImpactDist, gunToTargetAzi, gunToTargetDist):
    impliedwind_azimuth = find_azimuth_gun_target(
        gunToImpactAzi, gunToImpactDist, gunToTargetAzi, gunToTargetDist)
    impliedWindDriftMeters = find_distance_gun_target(
        gunToImpactAzi, gunToImpactDist, gunToTargetAzi, gunToTargetDist)
    return [impliedwind_azimuth, impliedWindDriftMeters]


def findImpliedWindAdjustedGunToTargetAziDist(unadjusted_gun_target_azimuth, unadjusted_gun_target_distance, impliedwind_azimuth, impliedWindDriftMeters):
    # target takes the spotter role in the triangle calculation
    # adjustedTarget takes the role of target in the triangle calculation
    # accounts for wind force 1-3

    # oppositewind_azimuth is the back azimuth of impliedwind_azimuth
    if impliedwind_azimuth < 180:
        oppositewind_azimuth = impliedwind_azimuth + 180
    elif impliedwind_azimuth >= 180:
        oppositewind_azimuth = impliedwind_azimuth - 180

    # spotter_gun_azimuth is unadjustedGunToTarget back azimuth
    if unadjusted_gun_target_azimuth < 180:
        targetToGunAzimuth = unadjusted_gun_target_azimuth + 180
    else:
        targetToGunAzimuth = unadjusted_gun_target_azimuth - 180

    adjusted_gun_target_azimuth = find_azimuth_gun_target(
        oppositewind_azimuth, impliedWindDriftMeters, targetToGunAzimuth, unadjusted_gun_target_distance)
    adjustedGunToTargetDist = find_distance_gun_target(
        oppositewind_azimuth, impliedWindDriftMeters, targetToGunAzimuth, unadjusted_gun_target_distance)
    return [unadjusted_gun_target_azimuth, unadjusted_gun_target_distance, adjusted_gun_target_azimuth, adjustedGunToTargetDist]


if __name__ == "__main__":
    # tempVar = find_distance_gun_target(spotter_target_azimuth, spotter_target_distance, spotter_gun_azimuth, spotter_gun_distance)
    # tempVar2 = find_azimuth_gun_target(spotter_target_azimuth, spotter_target_distance, spotter_gun_azimuth, spotter_gun_distance)
    # tempVar2 = find_azimuth_gun_target(323.13, 5, 270, 3)
    # tempVar = find_distance_gun_target(153, 180, 0, 0)
    # tempVar2 = find_azimuth_gun_target(153, 180, 0, 0)
    tempVar = find_distance_gun_target(299, 157, 0, 0)
    tempVar2 = find_azimuth_gun_target(299, 157, 0, 0)
    print(tempVar)
    print(tempVar2)

    # create firingSolution class, write helper definitions outside of class, inside class write functions to change instance variables & calls helper functions
    # calcHelper is functions outside of class, create new .py file for class & instance variable etc, import calcHelper
    pass
