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

    def spotterSwitch(self):
        if self.spotter == False:
            self.spotter = True
        else:
            self.spotter = False

    pass


if __name__ == "__main__":
    f1 = firingSolution()
    f1.spotterSwitch()
    f2 = firingSolution()
    print(f1.spotter)
    print(f2.spotter)
