import controller as cT
import math
import re


if __name__ == "__main__":
    # gridCoord = "G15K9K5"
    gridCoord = "G15K9"
    # horizLetter = gridCoord[0].lower()
    # vertNumber = int(gridCoord[1])
    # keypad = int(gridCoord[3]) 

    #789
    #456
    #123


    # !!!! redo handles g15k3k3, handles double digit vertical number
    # use regex on everything after first letter G(15K3K3)
    # aziDist = re.compile(r'[A-Za-z\. ]+(\d+)m[A-Za-z\. ]+(\d+)')
    # returnResult = aziDist.search(result).groups()
    try:
        x = re.search(r"(\w{1})(\d{1,})[Kk](\d)[Kk](\d)", gridCoord)
        print(x.group(1))
        print(x.group(2))
        print(x.group(3))
        print(x.group(4))
    except:
        x = re.search(r"(\w{1})(\d{1,})[Kk](\d)", gridCoord)
        print(x.group(1))
        print(x.group(2))
        print(x.group(3))
