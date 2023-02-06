import calcHelper as cH

# calcHelper.findAzimuthGunToTarget


class firingSolution:
    # set wind & weapon type values to global?, when they change, change all firingSolution object instance variables too?
    # class variables are default variables, change through function

    spotterToTargetDistance = 0
    spotterToTargetAzimuth = 0
    spotterToGunDistance = 0
    spotterToGunAzimuth = 0
    adjustedGunToTargetDistance = 0
    adjustedGunToTargetAzimuth = 0

    unadjustedGunToTargetAzimuth = 0
    unadjustedGunToTargetDistance = 0

    oldAdjustedGunToTargetAzimuth = 0
    oldAdjustedGunToTargetDistance = 0
    windAzimuth = 0
    windForce = 1
    weaponType = 1  # 120mm & 150mm

    def recalcGunToTarget(self):
        gttArr = cH.comprehensiveSpotterArtillery(self.spotterToTargetAzimuth, self.spotterToTargetDistance,
                                                  self.spotterToGunAzimuth, self.spotterToGunDistance, self.windAzimuth, self.windForce, self.weaponType)
        self.unadjustedGunToTargetAzimuth = gttArr[0]
        self.unadjustedGunToTargetDistance = gttArr[1]
        self.oldAdjustedGunToTargetAzimuth = gttArr[2] - self.adjustedGunToTargetAzimuth
        self.oldAdjustedGunToTargetDistance = gttArr[3] - self.adjustedGunToTargetDistance
        self.adjustedGunToTargetAzimuth = gttArr[2]
        self.adjustedGunToTargetDistance = gttArr[3]


if __name__ == "__main__":
    f1 = firingSolution()
    f1.spotterSwitch()
    f2 = firingSolution()
    print(f1.spotter)
    print(f2.spotter)
