import calcHelper as cH

# calcHelper.findAzimuthGunToTarget


class firingSolution:
    # set wind & weapon type values to global?, when they change, change all firingSolution object instance variables too?
    # class variables are default variables, change through function
    spotter = False

    spotterToTargetAzimuth = 0
    spotterToTargetDistance = 0
    spotterToGunAzimuth = 0
    spotterToGunDistance = 0

    unadjustedGunToTargetAzimuth = 0
    unadjustedGunToTargetDistance = 0
    adjustedGunToTargetAzimuth = 0
    adjustedGunToTargetDist = 0

    windAzimuth = 0
    windForce = 1
    weaponType = 1  # 120mm & 150mm

    def recalcGunToTarget(self):
        gttArr = cH.comprehensiveSpotterArtillery(self.spotterToTargetAzimuth, self.spotterToTargetDistance,
                                                  self.spotterToGunAzimuth, self.spotterToGunDistance, self.windAzimuth, self.windForce, self.weaponType)
        self.unadjustedGunToTargetAzimuth = gttArr[0]
        self.unadjustedGunToTargetDistance = gttArr[1]
        self.adjustedGunToTargetAzimuth = gttArr[2]
        self.adjustedGunToTargetDist = gttArr[3]

    def spotterSwitch(self):
        if self.spotter == False:
            self.spotter = True
        else:
            self.spotter = False
            self.spotterToGunAzimuth = 0
            self.spotterToGunDistance = 0

    def updateWind(self, windAzimuth, windForce):  # wf = 1-3
        self.windAzimuth = windAzimuth
        self.windForce = windForce

    def updateWeapon(self, weaponType):  # wt = 1-3
        self.weaponType = weaponType

    # use with ocr.extractAziDistText
    def updateSpotterToTarget(self, arr):
        self.spotterToTargetAzimuth = arr[0]
        self.spotterToTargetDistance = arr[1]

    # use with ocr.extractAziDistText
    def updateSpotterToGun(self, arr):
        self.spotterToGunAzimuth = arr[0]
        self.spotterToGunDistance = arr[1]


if __name__ == "__main__":
    f1 = firingSolution()
    f1.spotterSwitch()
    f2 = firingSolution()
    print(f1.spotter)
    print(f2.spotter)
