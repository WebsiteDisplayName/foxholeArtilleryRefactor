Usage
=====


Global values
-------------
1. These include ``Weapon Type``, ``Wind Force``, & ``Wind Azimuth``
2. Global values will affect all calculations


Gun rows
--------
1. Take out binoculars, record values in cells, then press ``Enter``
   a. *Spotter* represents the individual with binoculars
   b. *Gun* represents the friendly artillery piece used
   c. *Target* represents the target that is being fired at by *Gun*
   d. *distST* means the distance that is shown in binoculars when the *Spotter* looks at the *Target*
   e. The meanings of abbreviations can be found in the :doc:`glossary`
2. The values that should be input into the *Gun* are those in the ``adjDistGT`` and ``adjAziGT`` columns
   a. Relative adjustments are found in ``CHG adjDGT`` and ``CHG adjAGT`` columns



Advanced functions
------------------
Grid converter
^^^^^^^^^^^^^^
1. Functionality: calculates distance & azimuth between two grid coordinates and pushes those values to ``distST`` and ``aziST`` of a reference gun
2. Usage: when target and gun locations are visible on map, but cannot be seen with binoculars

ST Master
^^^^^^^^^
1. Functionality: adjusts ST values for every gun row in the table
2. Usage: when multiple gun batteries are dependent on a single *Spotter* and a different *Target* is chosen

SG Master
^^^^^^^^^
1. Functionality: changes all SG values for every gun row in the table based off of new *Spotter* and reference *Gun* relationship
2. Usage: *Spotter* changes position, but does not want to adjust all SG values

Wind Flag
^^^^^^^^^
1. Functionality: given the pole and flag tip location relative to a point, a vector that gives direction, i.e. azimuth, can be drawn from the pole to the flag
2. Usage: precisely calculate *Wind Azimuth* without havng to be aligned with the flag or fire rounds

Implied Wind Ref.
^^^^^^^^^^^^^^^^^
1. Functionality: calculates implied wind values given point of aim and impact, given a reference gun
2. Usage: quickly calculates wind values that carry over for future calculations

Horiz. Defl.
1. Functionality: calculates the affects of distance, change in azimuth, and meters of shift at that distance on each other
2. Usage: suppose target is 300 meters away and I want to shift point of impact 20 meters to the right, what change in azimuth is necessary?

Save/load firing tables
-----------------------
1. Select ``Open FS`` & choose relevant option
2. Files must be saved as *.txt* files