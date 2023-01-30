import calcHelper as cH

# calcHelper.findAzimuthGunToTarget


class firingSolution:
    # class variables are default variables, change through function
    # set wind & weapon type values to global?, when they change, change all firingSolution object instance variables too?
    spotter = False
    spotterToTargetAzimuth = 0
    spotterToTargetDistance = 0
    spotterToGunAzimuth = 0
    spotterToGunDistance = 0
    windAzimuth = 0
    windForce = 1
    weaponType = 1  # 120mm & 150mm

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

    pass


if __name__ == "__main__":
    f1 = firingSolution()
    f1.spotterSwitch()
    f2 = firingSolution()
    print(f1.spotter)
    print(f2.spotter)
