import calcHelper as cH

# calcHelper.findAzimuthGunToTarget

class firingSolution:
    # set wind & weapon type values to global?, when they change, change all firingSolution object instance variables too?
    # class variables are default variables, change through function

    def __init__(self):
        self.spotterToTargetDistance = 0
        self.spotterToTargetAzimuth = 0
        self.spotterToGunDistance = 0
        self.spotterToGunAzimuth = 0
        self.adjustedGunToTargetDistance = 0
        self.adjustedGunToTargetAzimuth = 0

        self.unadjustedGunToTargetAzimuth = 0
        self.unadjustedGunToTargetDistance = 0

        self.oldAdjustedGunToTargetAzimuth = 0
        self.oldAdjustedGunToTargetDistance = 0
        self.windAzimuth = 0
        self.windForce = 1
        self.weaponType = list(cH.WEAPONTYPEWINDFORCES.keys())[0]

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
