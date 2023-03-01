Glossary
========

Global terms
------------
    :Wind Force: Strength of wind from 1 to 5 indicated by in-game flags
    :Wind Azi: Direction the wind is blowing, i.e. wind blowing North to South is 180 degrees
    :Open FS: Open Firing Solution, able to save and load stored artillery calculations

Standard functionality
----------------------
    :distST: Distance from *Spotter* to *Target*
    :aziST: Azimuth from *Spotter* to *Target*
    :distSG: Distance from *Spotter* to *Gun*
    :aziSG: Azimuth from *Spotter* to *Gun*
    :adjDistGT: Wind-adjusted Distance *Gun* to *Target*
    :adjAziGT: Wind-adjusted Azimuth *Gun* to *Target*
    :CHG adjDGT: Net change from current and previous adjDistGT values
    :CHG adjAGT: Net change from current and previous adjAziGT values


Advanced functions
------------------
    :Grid Conv.: Converts grid coordinates, i.e. "G9K3K7" or "G9K3", and pushes to *Spotter* to *Target*
    :ST Master: function that globally changes *Spotter* to *Target* values
    :SG Master: function that globally changes *Spotter* to *Target* values based on new spotter position to reference Gun
    :Wind Flag: function that calculates and globally pushes *Wind Azimuth* based on fly & hoist end, i.e. tip of flag vs. pole
        :distSF: Distance from *Spotter* to *Flag* (fly end/flag tip)
        :aziSF: Azimuth from *Spotter* to *Flag* (fly end/flag tip)
        :distSP: Distance from *Spotter* to *Pole* (hoist end)
        :aziSP: Azimuth from *Spotter* to *Pole* (hoist end)
    :Implied Wind Ref.: function that calculates implied wind values based off of point of aim & impact, or pushes hard coded values to global, based off of reference gun
        :distSI: Distance from *Spotter* to *Impact*
        :aziSI: Azimuth from *Spotter* to *Impact*
        :impWF: Implied wind force in meters, cell value can be calculated or manually input
        :impWA: Implied wind azimuth, cell value can be calculated or manually input
    :Horiz. Defl.: Horizontal deflection, function that calculates how far distance shifts aim, given a set change in azimuth
        :distGI: Distance from *Gun* to *Impact*
        :Azi. CHG: Change in azimuth between two points of aim
        :Offset meters: Offset distance on aim caused by shift in azimuth/angle, and proportional to distance

        





