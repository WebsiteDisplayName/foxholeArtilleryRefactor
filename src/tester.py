import math
import re

import controller as cT

if __name__ == "__main__":
    # grid_coord = "G15K9K5"
    grid_coord = "G15K9"
    # horiz_letter = grid_coord[0].lower()
    # vert_number = int(grid_coord[1])
    # keypad = int(grid_coord[3])

    # 789
    # 456
    # 123

    # !!!! redo handles g15k3k3, handles double digit vertical number
    # use regex on everything after first letter G(15K3K3)
    # aziDist = re.compile(r'[A-Za-z\. ]+(\d+)m[A-Za-z\. ]+(\d+)')
    # returnResult = aziDist.search(result).groups()
    try:
        x = re.search(r"(\w{1})(\d{1,})[Kk](\d)[Kk](\d)", grid_coord)
        print(x.group(1))
        print(x.group(2))
        print(x.group(3))
        print(x.group(4))
    except:
        x = re.search(r"(\w{1})(\d{1,})[Kk](\d)", grid_coord)
        print(x.group(1))
        print(x.group(2))
        print(x.group(3))
