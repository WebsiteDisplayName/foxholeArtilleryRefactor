import dearpygui.dearpygui as dpg
import artilleryCalculator as aC
import calcHelper as cH
import keyboard
import ocr
from tkinter import filedialog
from tkinter import *
import math
import re

# https://dearpygui.readthedocs.io/en/latest/documentation/item-creation.html
# https://dearpygui.readthedocs.io/en/latest/tutorials/item-usage.html?highlight=current%20widget set values
# https://dearpygui.readthedocs.io/en/latest/documentation/item-callbacks.html
# https://dearpygui.readthedocs.io/en/latest/documentation/tables.html
global gunCounter
gunCounter = 0
firingSolutionDict = {}

# wind azimuth is direction it is going towards, 0 = wind is blowing North


def updateFiringSolution(sender, app_data, user_data):
    varToChange = user_data[1]
    if varToChange == 1:  # gun name I changed this
        firingSolutionDict[user_data[0]].gunName = app_data
        dpg.configure_item("gridGunDropdown", items=[
            firingSolutionDict[key].gunName for key, val in firingSolutionDict.items()])
        dpg.configure_item("spotterPosDropdown", items=[
            firingSolutionDict[key].gunName for key, val in firingSolutionDict.items()])
        dpg.configure_item("impliedWindDropdown", items=[
            firingSolutionDict[key].gunName for key, val in firingSolutionDict.items()])

    elif varToChange == 2:  # distST
        firingSolutionDict[user_data[0]].spotterToTargetDistance = app_data
    elif varToChange == 3:  # aziST
        firingSolutionDict[user_data[0]
                           ].spotterToTargetAzimuth = app_data % 360
    elif varToChange == 4:  # distSG
        firingSolutionDict[user_data[0]].spotterToGunDistance = app_data
    elif varToChange == 5:  # aziSG
        firingSolutionDict[user_data[0]].spotterToGunAzimuth = app_data % 360
    elif varToChange == 6:  # weapon type
        weaponList = ["120mm & 150mm", "Storm cannon", "Mortars"]
        weaponNum = weaponList.index(app_data) + 1
        for key, fs in firingSolutionDict.items():
            fs.weaponType = int(weaponNum)
            setValues(key, "adjusted")
        return
    elif varToChange == 7:  # wind force
        for key, fs in firingSolutionDict.items():
            if type(app_data) == str:
                fs.windForce = app_data
            else:
                fs.windForce = int(app_data)
            setValues(key, "adjusted")
        return
    elif varToChange == 8:  # wind azimuth
        for key, fs in firingSolutionDict.items():
            fs.windAzimuth = int(app_data) % 360
            setValues(key, "adjusted")
        return
    setValues(user_data[0], "adjusted")


def setValues(key,type): #key is key from dictionary, type = [adjusted, target, gun]
    firingSolutionDict[key].recalcGunToTarget()
    if type == "target":
        dpg.set_value(
            f"{key}2", round(firingSolutionDict[key].spotterToTargetDistance,2))
        dpg.set_value(
            f"{key}3", round(firingSolutionDict[key].spotterToTargetAzimuth,2))
    elif type == "gun":
        dpg.set_value(
            f"{key}4", round(firingSolutionDict[key].spotterToGunDistance,2))
        dpg.set_value(
            f"{key}5", round(firingSolutionDict[key].spotterToGunAzimuth,2))
    elif type == "adjusted":
        dpg.set_value(
            f"{key}6", round(firingSolutionDict[key].adjustedGunToTargetDistance,2))
        dpg.set_value(
            f"{key}7", round(firingSolutionDict[key].adjustedGunToTargetAzimuth,2))
        dpg.set_value(
            f"{key}8", round(firingSolutionDict[key].oldAdjustedGunToTargetDistance,2))
        dpg.set_value(
            f"{key}9", round(firingSolutionDict[key].oldAdjustedGunToTargetAzimuth,2))


def add_guns():
    global gunCounter
    gunCounter += 1
    newFS = aC.firingSolution()
    firingSolutionDict[gunCounter] = newFS
    with dpg.table_row(parent="gun_table", tag=f"new_gun{gunCounter}"):
        dpg.add_input_text(tag=f"{gunCounter}1",
                           default_value=f"Gun {gunCounter}", callback=updateFiringSolution, user_data=[gunCounter, 1], width=80)  # Name
        dpg.add_input_double(tag=f"{gunCounter}2",
                          default_value=0, step=0, step_fast=0, callback=updateFiringSolution, user_data=[gunCounter, 2], width=80, on_enter=True, format="%.1f")  # distST
        dpg.add_input_double(tag=f"{gunCounter}3",
                          default_value=0, step=0, step_fast=0, callback=updateFiringSolution, user_data=[gunCounter, 3], width=80, on_enter=True, format="%.1f")  # aziST
        dpg.add_input_double(tag=f"{gunCounter}4",
                          default_value=0, step=0, step_fast=0, callback=updateFiringSolution, user_data=[gunCounter, 4], width=80, on_enter=True, format="%.1f")  # distSG
        dpg.add_input_double(tag=f"{gunCounter}5",
                          default_value=0, step=0, step_fast=0, callback=updateFiringSolution, user_data=[gunCounter, 5], width=80, on_enter=True, format="%.1f")  # aziSG
        dpg.add_text(tag=f"{gunCounter}6", default_value=0)  # adjDistGT
        dpg.add_text(tag=f"{gunCounter}7", default_value=0)  # adjAziGT
        dpg.add_text(tag=f"{gunCounter}8", default_value=0) # delta between old and new adjDistGT
        dpg.add_text(tag=f"{gunCounter}9", default_value=0) # delta between old and new adjDistGT
    # I changed this
    firingSolutionDict[gunCounter].gunName = f"Gun {gunCounter}"
    dpg.configure_item("gridGunDropdown", items=[
        firingSolutionDict[key].gunName for key, val in firingSolutionDict.items()])
    dpg.configure_item("spotterPosDropdown", items=[
        firingSolutionDict[key].gunName for key, val in firingSolutionDict.items()])
    dpg.configure_item("impliedWindDropdown", items=[
        firingSolutionDict[key].gunName for key, val in firingSolutionDict.items()])


def delete_guns():
    global gunCounter
    if gunCounter >= 1:
        dpg.delete_item(f"new_gun{gunCounter}")
        del firingSolutionDict[gunCounter]
        gunCounter -= 1
    dpg.configure_item("gridGunDropdown", items=[
        firingSolutionDict[key].gunName for key, val in firingSolutionDict.items()])
    dpg.configure_item("spotterPosDropdown", items=[
        firingSolutionDict[key].gunName for key, val in firingSolutionDict.items()])
    dpg.configure_item("impliedWindDropdown", items=[
        firingSolutionDict[key].gunName for key, val in firingSolutionDict.items()])

def gridCoordConv():
    # a1 top left, q15 bottom right
    # g9 125 meter side
    # g9k3: 41 meter side
    # g9k3k3: ~13.8 meter side
    # first calculate horizontal and vertical of both points in distance, then subtract
    # find length of two sides at 90, calc azimuth and distance of hypotenuse
    # tactic: a1 = top left of grid square, keypads add distance?
    refGridGunName =dpg.get_value("gridGunDropdown")
    gunGridCoord = dpg.get_value("gridCoord1")
    targetGridCoord = dpg.get_value("gridCoord2")

    hvValsGun = originDistFromGridCoord(gunGridCoord)
    hvValsTarget = originDistFromGridCoord(targetGridCoord)
    # azimuth is either 0 or 90, write up on paper
    distSG = hvValsTarget[0] - hvValsGun[0] 
    distST = hvValsTarget[1] - hvValsGun[1]
    if distSG > 0: #gets azimuth for calc
        aziSG = 270
    else:
        aziSG = 90
    distSG = abs(distSG)
    if distST > 0:
        aziST = 0
    else:
        aziST = 180
    distST = abs(distST)
    # spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance
    distGT = cH.findDistanceGunToTarget(aziST,distST,aziSG,distSG)
    aziGT = cH.findAzimuthGunToTarget(aziST,distST,aziSG,distSG)

    for key, val in firingSolutionDict.items():
        if val.gunName == refGridGunName:   
            val.spotterToTargetDistance = distGT
            val.spotterToTargetAzimuth = aziGT
            setValues(key,"target")
            setValues(key,"adjusted")


def originDistFromGridCoord(gridCoord):
    # start in bottom left
    # g9k3: 41 meter side
    horizLetters = list('abcdefghijklmnopq')
    vertNumbers = list(range(1,16))

    horizLettersDict = dict(zip(horizLetters,list(range(0,len(horizLetters))))) # 'a':0, 'b':1
    vertNumbersDict = dict(zip(vertNumbers[::-1], list(range(0,len(vertNumbers))))) # 15:0, 14:1, 1:14

    # https://www.reddit.com/r/foxholegame/comments/mopq7l/foxholes_map_is_64km2/
    regionHorizLength = 2184
    regionVertLength = 1890 #hard coded !
    gridHorizLength = regionHorizLength / len(horizLetters)
    gridVertLength = regionVertLength / len(vertNumbers)

    # distance from botton left of grid map (A15)
    runningHorizontalDistance = 0
    runningVerticalDistance = 0
    #789
    #456
    #123


    # !!!! redo handles g15k3k3, handles double digit vertical number
    # use regex on everything after first letter G(15K3K3)
    # aziDist = re.compile(r'[A-Za-z\. ]+(\d+)m[A-Za-z\. ]+(\d+)')
    # returnResult = aziDist.search(result).groups()

    try:
        x = re.search(r"(\w{1})(\d{1,})[Kk](\d)[Kk](\d)", gridCoord)
        horizLetter = x.group(1).lower()
        vertNumber = int(x.group(2))
        keypad = int(x.group(3))
        secondKeypad = int(x.group(4))
        case = 1
    except:
        x = re.search(r"(\w{1})(\d{1,})[Kk](\d)", gridCoord)
        horizLetter = x.group(1).lower()
        vertNumber = int(x.group(2))
        keypad = int(x.group(3))
        case = 2




    # handles grid square (G9)
    runningHorizontalDistance += horizLettersDict[horizLetter]*gridHorizLength  
    runningVerticalDistance += vertNumbersDict[vertNumber]*gridVertLength

    # handles keypad, convert to hor/vert distance
    # one part handles vertical and another conditional handles horiztonal
    if case == 1 or case == 2:
        runningHorizontalDistance += gridHorizLength/6 # moves to middle of keypad 1
        runningVerticalDistance += gridVertLength/6
        horVertVals = keypadDistance(gridHorizLength/3, gridVertLength/3, keypad)
        runningHorizontalDistance += horVertVals[0]
        runningVerticalDistance += horVertVals[1]
    # handles if additional keypad is added
    if case == 1:
        runningHorizontalDistance -= gridHorizLength/6 # resets to bottom left
        runningVerticalDistance -= gridVertLength/6
        runningHorizontalDistance += gridHorizLength/18 # centers for smaller keypad
        runningVerticalDistance += gridVertLength/18
        horVertVals = keypadDistance(gridHorizLength/9, gridVertLength/9, secondKeypad)
        runningHorizontalDistance += horVertVals[0]
        runningVerticalDistance += horVertVals[1]
    return [runningHorizontalDistance, runningVerticalDistance]


def keypadDistance(horizKeypadLength, vertKeypadLength, keypad):
    runningVerticalDistance = 0
    runningHorizontalDistance = 0
    if keypad in [4,5,6]:
        runningVerticalDistance += vertKeypadLength
    elif keypad in [7,8,9]:
        runningVerticalDistance += vertKeypadLength*2

    if keypad in [2,5,8]:
        runningHorizontalDistance += horizKeypadLength
    elif keypad in [3,6,9]:
        runningHorizontalDistance += horizKeypadLength*2

    return [runningHorizontalDistance, runningVerticalDistance]

    # return horizontal and vertical distance from grid coord

def recalculateSTValues():
    newGlobalDistST = dpg.get_value("spotterTargetDistChange")
    newGlobalAziST = dpg.get_value("spotterTargetAziChange") % 360
    for idx in range(1,gunCounter+1):
        dpg.set_value(f"{idx}2", newGlobalDistST)
        dpg.set_value(f"{idx}3", newGlobalAziST)
        firingSolutionDict[idx].spotterToTargetDistance = newGlobalDistST
        firingSolutionDict[idx].spotterToTargetAzimuth = newGlobalAziST
        setValues(idx, "adjusted")
        
def recalculateSGValues():
    refGunName = dpg.get_value("spotterPosDropdown")
    newRefDistSG = dpg.get_value("spotterGunDistChange")
    newRefAziSG = dpg.get_value("spotterGunAziChange") % 360
    newRefAziSGBack = newRefAziSG - 180 if newRefAziSG >= 180 else newRefAziSG + 180
    # back azimuth
    # calculate internal gun relationships with respect to the refGunName chosen with historical values then recalculate updated SG and update
    if len(firingSolutionDict) >= 2:
        refKey = -1
        for key, val in firingSolutionDict.items():  # find key of chosen refGunName
            if val.gunName == refGunName:
                refKey = key
        if refKey == -1:
            return
        # calculating everything relative to the chosen refGunName, azimuth is traveling from ref to curr
        oldRefSGDist = firingSolutionDict[refKey].spotterToGunDistance
        oldRefSGAzi = firingSolutionDict[refKey].spotterToGunAzimuth
        for key, val in firingSolutionDict.items():
            if val.gunName == refGunName:
                continue
            # spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance
            currSGDist = firingSolutionDict[key].spotterToGunDistance
            currSGAzi = firingSolutionDict[key].spotterToGunAzimuth
            refToCurrAzi = cH.findAzimuthGunToTarget(
                currSGAzi, currSGDist, oldRefSGAzi, oldRefSGDist)
            refToCurrDist = cH.findDistanceGunToTarget(
                currSGAzi, currSGDist, oldRefSGAzi, oldRefSGDist)
            newCurrSGAzi = cH.findAzimuthGunToTarget(
                refToCurrAzi, refToCurrDist, newRefAziSGBack, newRefDistSG)
            newCurrSGDist = cH.findDistanceGunToTarget(
                refToCurrAzi, refToCurrDist, newRefAziSGBack, newRefDistSG)
            dpg.set_value(
                f"{key}4", newCurrSGDist)
            dpg.set_value(
                f"{key}5", newCurrSGAzi)
            firingSolutionDict[key].spotterToGunDistance = newCurrSGDist
            firingSolutionDict[key].spotterToGunAzimuth = newCurrSGAzi
            setValues(key, "adjusted")
    # update ref
        dpg.set_value(
            f"{refKey}4", newRefDistSG)
        dpg.set_value(
            f"{refKey}5", newRefAziSG)
        firingSolutionDict[refKey].spotterToGunDistance = newRefDistSG
        firingSolutionDict[refKey].spotterToGunAzimuth = newRefAziSG
        setValues(refKey, "adjusted")

def globalWindCalc():
    distSF = dpg.get_value("distSpotterToFlag")
    aziSF = dpg.get_value("aziSpotterToFlag") % 360
    distSP = dpg.get_value("distSpotterToPole")
    aziSP = dpg.get_value("aziSpotterToPole") % 360
    newWindAzimuth = cH.findAzimuthGunToTarget(aziSF,distSF,aziSP,distSP)
    dpg.set_value("globalWindAzimuth",newWindAzimuth)
    for key in range(1,gunCounter+1):
        firingSolutionDict[key].windAzimuth = newWindAzimuth
        setValues(key, "adjusted")

def impliedWindCalc():
    refImpliedGunName = dpg.get_value("impliedWindDropdown")
    distSI = dpg.get_value("distSpotterToImpact")
    aziSI = dpg.get_value("aziSpotterToImpact") % 360
    for key, val in firingSolutionDict.items():
        if val.gunName == refImpliedGunName:
            refKey = key
            break
    # findDistanceGunToTarget(spotterToTargetAzimuth, spotterToTargetDistance, spotterToGunAzimuth, spotterToGunDistance)
    origDistSG = firingSolutionDict[refKey].spotterToGunDistance
    origAziSG = firingSolutionDict[refKey].spotterToGunAzimuth
    origDistGT = firingSolutionDict[refKey].adjustedGunToTargetDistance # changed
    origAziGT = firingSolutionDict[refKey].adjustedGunToTargetAzimuth

    distGI = cH.findDistanceGunToTarget(aziSI, distSI, origAziSG, origDistSG)
    aziGI = cH.findAzimuthGunToTarget(aziSI, distSI, origAziSG, origDistSG)

    # implied wind force, implied wind azimuth
    impWF = cH.findDistanceGunToTarget(aziGI, distGI, origAziGT, origDistGT)
    impWA = cH.findAzimuthGunToTarget(aziGI, distGI, origAziGT, origDistGT)

    dpg.set_value("impliedWindForce",f"{impWF:.2f}")
    dpg.set_value("impliedWindAzimuth",f"{impWA:.2f}")
    # have impval in row call callback, global push pushes whatever is in the cell to global & recalc

def pushImpliedWindToGlobal():
    impliedWindForce = float(dpg.get_value("impliedWindForce"))
    impliedWindForceAzimuth = float(dpg.get_value("impliedWindAzimuth")) % 360
    dpg.set_value("globalWindAzimuth",impliedWindForceAzimuth)

    impliedWindForceStr = f"IWF: {impliedWindForce:.2f}"
    dpg.configure_item("windForceDropdown", items=[1,2,3, impliedWindForceStr])
    dpg.set_value("windForceDropdown",impliedWindForceStr)

    for key in range(1,gunCounter+1):
        firingSolutionDict[key].windForce = impliedWindForceStr
        firingSolutionDict[key].windAzimuth = impliedWindForceAzimuth
        setValues(key, "adjusted")


def horizDeflCalc(sender, app_data, user_data):
    distGI = float(dpg.get_value("distGunToImpactDeflection"))
    azimuthDeflection = float(dpg.get_value("azimuthDeflection"))
    offsetMetersDeflection = float(dpg.get_value("offsetMetersDeflection"))
    holdConstant = str(dpg.get_value("holdConstantDropdown"))
    # 1,2,3 = distGI, azi, metersOffset
    changedInput = user_data[0]
    optionList = ["distGI","Azi.","Offset Meters"]
    for val in optionList:
        if holdConstant == changedInput:
            return
        elif val not in [holdConstant, changedInput]:
            outputVar = val
    
    if outputVar == optionList[0]: #distGI
        # find length of side isosceles triangle
        # (baseSide/2)/cosine(90-betaAngle/2)
        adjacentAngleRadians = math.radians(90-azimuthDeflection/2)
        newDistGI = (offsetMetersDeflection/2)/math.cos(adjacentAngleRadians) #inputs radians
        dpg.set_value("distGunToImpactDeflection",newDistGI)
    elif outputVar == optionList[1]: #Azi
        newAzimuthDeflection = math.degrees(math.acos((2*distGI**2 - offsetMetersDeflection**2)/(2*distGI**2)))
        dpg.set_value("azimuthDeflection",newAzimuthDeflection)
    elif outputVar == optionList[2]: #Offset Meters
        newOffsetMetersDeflection = math.sin(math.radians(azimuthDeflection))*distGI
        dpg.set_value("offsetMetersDeflection",newOffsetMetersDeflection)

def setHotkeys():
        with open("keybinds.txt") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip() # parse string
                valList = line.split(',')
                valList[1] = int(valList[1])
                keyboard.add_hotkey(valList[0], lambda vals=valList[1:]: updateFSByScreenCap(vals[0],vals[1]))
                # 0 = keybind, 1 = which rows are affected, 2 = columns/type
                # black magic: https://stackoverflow.com/questions/21791482/split-list-into-different-variables

def updateFSByScreenCap(key, type):
    if key in firingSolutionDict:
        if type == "target":
            capDist, capAzi = ocr.screepCapExtract("target")
            firingSolutionDict[key].spotterToTargetDistance = capDist
            firingSolutionDict[key].spotterToTargetAzimuth = capAzi
            setValues(key, "target")
        elif type == "gun":
            capDist, capAzi = ocr.screepCapExtract("gun")
            firingSolutionDict[key].spotterToGunDistance = capDist
            firingSolutionDict[key].spotterToGunAzimuth = capAzi
            setValues(key, "gun")
        elif type == "global":
            if key == 1: #spotter to target global change
                capDist, capAzi = ocr.screepCapExtract("global1")
                dpg.set_value("spotterTargetDistChange",capDist)
                dpg.set_value("spotterTargetAziChange",capAzi)
                recalculateSTValues()
            elif key == 2: #SG master
                capDist, capAzi = ocr.screepCapExtract("global2")
                dpg.set_value("spotterGunDistChange",capDist)
                dpg.set_value("spotterGunAziChange",capAzi)
                recalculateSGValues()
            elif key == 3: #global wind flag ctrl + V
                capDist, capAzi = ocr.screepCapExtract("global3")
                dpg.set_value("distSpotterToFlag",capDist)
                dpg.set_value("aziSpotterToFlag",capAzi)
                globalWindCalc()
            elif key == 4: #global wind pole shift + V
                capDist, capAzi = ocr.screepCapExtract("global4")
                dpg.set_value("distSpotterToPole",capDist)
                dpg.set_value("aziSpotterToPole",capAzi)
                globalWindCalc()

        setValues(key, "adjusted")



def fileOptions(sender, app_data):
    if app_data == "Open FS":
        filePath =  filedialog.askopenfilename(initialdir = "../firingSolutionTables",title = "Select file",filetypes = (("txt files", "*.txt"),("all files","*.*")))
        if filePath == "":
            return
        for idx in range(gunCounter):
            delete_guns()
        with open(filePath) as f:
            lines = f.readlines()
            for line in lines:
                add_guns()
                line = line.strip() # parse string
                valList = line.split(',')
                valList = [valList[0]] + list(map(float, valList[1:]))

                firingSolutionDict[gunCounter].gunName = valList[0] 
                firingSolutionDict[gunCounter].spotterToTargetDistance = valList[1] 
                firingSolutionDict[gunCounter].spotterToTargetAzimuth = valList[2]
                firingSolutionDict[gunCounter].spotterToGunDistance = valList[3]
                firingSolutionDict[gunCounter].spotterToGunAzimuth = valList[4]
                firingSolutionDict[gunCounter].adjustedGunToTargetDistance = valList[5]
                firingSolutionDict[gunCounter].adjustedGunToTargetAzimuth = valList[6]
                setValues(gunCounter, "target")
                setValues(gunCounter, "gun")
                setValues(gunCounter, "adjusted")

    # https://stackoverflow.com/questions/11295917/how-to-select-a-directory-and-store-the-location-using-tkinter-in-python
    elif app_data == "Save FS": #open folder, save text as what gui?
        filePath =  filedialog.asksaveasfilename(initialdir = "../firingSolutionTables",
            title="File name to save as",filetypes = (("txt files", "*.txt"),("all files", "*.*")))
        with open(filePath+'.txt', 'w') as f:
            for row in range(1,gunCounter+1):
                for column in range(1,8): #7 columns
                    f.write(str(dpg.get_value(f"{row}{column}")))
                    if column == 7:
                        f.write('\n')
                        continue
                    f.write(',')

# open and store firingSolutions in .txt and add keybinds to setHotkeys



if __name__ == "__main__":

    keyboard.add_hotkey("shift+1", updateFSByScreenCap(), args=(1, "target"))
    keyboard.add_hotkey("ctrl+1", updateFSByScreenCap(), args=(1, "gun"))
    pass
