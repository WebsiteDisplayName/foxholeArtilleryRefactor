import calc_helper as cH


class FiringSolution:
    # set wind & weapon type values to global?, when they change, change all FiringSolution object instance variables too?
    # class variables are default variables, change through function

    def __init__(self):
        self.spotter_target_distance = 0
        self.spotter_target_azimuth = 0
        self.spotter_gun_distance = 0
        self.spotter_gun_azimuth = 0
        self.adjusted_gun_target_distance = 0
        self.adjusted_gun_target_azimuth = 0

        self.unadjusted_gun_target_azimuth = 0
        self.unadjusted_gun_target_distance = 0

        self.oldadjusted_gun_target_azimuth = 0
        self.oldadjusted_gun_target_distance = 0
        self.wind_azimuth = 0
        self.wind_force = 1
        self.weapon_type = list(cH.WEAPONTYPEWINDFORCES.keys())[0]

    def recalc_gun_target(self):
        get_attr = cH.comprehensiveSpotterArtillery(
            self.spotter_target_azimuth,
            self.spotter_target_distance,
            self.spotter_gun_azimuth,
            self.spotter_gun_distance,
            self.wind_azimuth,
            self.wind_force,
            self.weapon_type,
        )
        self.unadjusted_gun_target_azimuth = get_attr[0]
        self.unadjusted_gun_target_distance = get_attr[1]
        self.oldadjusted_gun_target_azimuth = (
            get_attr[2] - self.adjusted_gun_target_azimuth
        )
        self.oldadjusted_gun_target_distance = (
            get_attr[3] - self.adjusted_gun_target_distance
        )
        self.adjusted_gun_target_azimuth = get_attr[2]
        self.adjusted_gun_target_distance = get_attr[3]


if __name__ == "__main__":
    f1 = FiringSolution()
    f1.spotterSwitch()
    f2 = FiringSolution()
    print(f1.spotter)
    print(f2.spotter)
