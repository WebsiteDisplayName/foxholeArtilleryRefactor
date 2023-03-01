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
    :Grid Conv.: Converts grid coordinates to Distance and Azimuth, i.e. "G9K3K7" or "G9K3"
    :ST Master: function that globally changes *Spotter* to *Target* values
    :SG Master: function that globally changes *Spotter* to *Target* values based on new spotter position to reference Gun
    :Wind Flag: function that calculates and globally pushes *Wind Azimuth* based on fly & hoist end, i.e. tip of flag vs. pole
    




