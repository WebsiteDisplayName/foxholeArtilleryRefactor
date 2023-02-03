import dearpygui.dearpygui as dpg
import artilleryCalculator as aC
import calcHelper as cH
import keyboard
import ocr
from tkinter import filedialog
from tkinter import *

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
        dpg.configure_item("spotterPosDropdown", items=[
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
            fs.recalcGunToTarget()
            dpg.set_value(
                f"{key}6", f"{firingSolutionDict[key].adjustedGunToTargetDistance:.2f}")
            dpg.set_value(
                f"{key}7", f"{firingSolutionDict[key].adjustedGunToTargetAzimuth:.2f}")
        return
    elif varToChange == 7:  # wind force
        for key, fs in firingSolutionDict.items():
            fs.windForce = int(app_data)
            fs.recalcGunToTarget()
            dpg.set_value(
                f"{key}6", f"{firingSolutionDict[key].adjustedGunToTargetDistance:.2f}")
            dpg.set_value(
                f"{key}7", f"{firingSolutionDict[key].adjustedGunToTargetAzimuth:.2f}")
        return
    elif varToChange == 8:  # wind azimuth
        for key, fs in firingSolutionDict.items():
            fs.windAzimuth = int(app_data) % 360
            fs.recalcGunToTarget()
            dpg.set_value(
                f"{key}6", f"{firingSolutionDict[key].adjustedGunToTargetDistance:.2f}")
            dpg.set_value(
                f"{key}7", f"{firingSolutionDict[key].adjustedGunToTargetAzimuth:.2f}")
        return
    firingSolutionDict[user_data[0]].recalcGunToTarget()
    dpg.set_value(
        f"{user_data[0]}6", f"{firingSolutionDict[user_data[0]].adjustedGunToTargetDistance:.2f}")
    dpg.set_value(
        f"{user_data[0]}7", f"{firingSolutionDict[user_data[0]].adjustedGunToTargetAzimuth:.2f}")


def add_guns():
    global gunCounter
    gunCounter += 1
    newFS = aC.firingSolution()
    firingSolutionDict[gunCounter] = newFS
    with dpg.table_row(parent="gun_table", tag=f"new_gun{gunCounter}"):
        dpg.add_input_text(tag=f"{gunCounter}1",
                           default_value=f"Gun {gunCounter}", callback=updateFiringSolution, user_data=[gunCounter, 1], width=80)  # Name
        dpg.add_input_int(tag=f"{gunCounter}2",
                          default_value=0, step=0, step_fast=0, callback=updateFiringSolution, user_data=[gunCounter, 2], width=80)  # distST
        dpg.add_input_int(tag=f"{gunCounter}3",
                          default_value=0, step=0, step_fast=0, callback=updateFiringSolution, user_data=[gunCounter, 3], width=80)  # aziST
        dpg.add_input_int(tag=f"{gunCounter}4",
                          default_value=0, step=0, step_fast=0, callback=updateFiringSolution, user_data=[gunCounter, 4], width=80)  # distSG
        dpg.add_input_int(tag=f"{gunCounter}5",
                          default_value=0, step=0, step_fast=0, callback=updateFiringSolution, user_data=[gunCounter, 5], width=80)  # aziSG
        dpg.add_text(tag=f"{gunCounter}6", default_value=0)  # adjDistGT
        dpg.add_text(tag=f"{gunCounter}7", default_value=0)  # adjAziGT
    # I changed this
    firingSolutionDict[gunCounter].gunName = f"Gun {gunCounter}"
    dpg.configure_item("spotterPosDropdown", items=[
        firingSolutionDict[key].gunName for key, val in firingSolutionDict.items()])


def delete_guns():
    global gunCounter
    if gunCounter >= 1:
        dpg.delete_item(f"new_gun{gunCounter}")
        del firingSolutionDict[gunCounter]
        gunCounter -= 1
    dpg.configure_item("spotterPosDropdown", items=[
        firingSolutionDict[key].gunName for key, val in firingSolutionDict.items()])

def recalculateSTValues():
    newGlobalDistST = dpg.get_value("spotterTargetDistChange")
    newGlobalAziST = dpg.get_value("spotterTargetAziChange") % 360
    for idx in range(1,gunCounter+1):
        dpg.set_value(f"{idx}2", newGlobalDistST)
        dpg.set_value(f"{idx}3", newGlobalAziST)
        firingSolutionDict[idx].spotterToTargetDistance = newGlobalDistST
        firingSolutionDict[idx].spotterToTargetAzimuth = newGlobalAziST
        firingSolutionDict[idx].recalcGunToTarget()
        dpg.set_value(
            f"{idx}6", round(firingSolutionDict[idx].adjustedGunToTargetDistance,2))
        dpg.set_value(
            f"{idx}7", round(firingSolutionDict[idx].adjustedGunToTargetAzimuth,2))

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
            firingSolutionDict[key].recalcGunToTarget()
            dpg.set_value(
                f"{key}6", round(firingSolutionDict[key].adjustedGunToTargetDistance,2))
            dpg.set_value(
                f"{key}7", round(firingSolutionDict[key].adjustedGunToTargetAzimuth,2))
    # update ref
        dpg.set_value(
            f"{refKey}4", newRefDistSG)
        dpg.set_value(
            f"{refKey}5", newRefAziSG)
        firingSolutionDict[refKey].spotterToGunDistance = newRefDistSG
        firingSolutionDict[refKey].spotterToGunAzimuth = newRefAziSG
        firingSolutionDict[refKey].recalcGunToTarget()
        dpg.set_value(
            f"{refKey}6", round(firingSolutionDict[refKey].adjustedGunToTargetDistance,2))
        dpg.set_value(
            f"{refKey}7", round(firingSolutionDict[refKey].adjustedGunToTargetAzimuth,2))

# type is "target" or "gun"
    # shift is target, ctrl is gun (every screencap gets dist & azi)
# def fish():
#     keyboard.add_hotkey(f"shift+{1}", lambda: print(1, "target"))
#     keyboard.add_hotkey(f"ctrl+{1}", lambda: print(1, "gun"))
def setHotkeys():
        keyboard.add_hotkey(f"shift+1", lambda: updateFSByScreenCap(1,"target")) #spotterToTarget: dist and azi
        keyboard.add_hotkey(f"ctrl+1", lambda: updateFSByScreenCap(1,"gun")) #spotterToGun: dist and azi
        keyboard.add_hotkey(f"shift+2", lambda: updateFSByScreenCap(2,"target"))
        keyboard.add_hotkey(f"ctrl+2", lambda: updateFSByScreenCap(2,"gun"))
        keyboard.add_hotkey(f"shift+3", lambda: updateFSByScreenCap(3,"target"))
        keyboard.add_hotkey(f"ctrl+3", lambda: updateFSByScreenCap(3,"gun"))
        keyboard.add_hotkey(f"shift+4", lambda: updateFSByScreenCap(4,"target"))
        keyboard.add_hotkey(f"ctrl+4", lambda: updateFSByScreenCap(4,"gun"))
        keyboard.add_hotkey(f"shift+5", lambda: updateFSByScreenCap(5,"target"))
        keyboard.add_hotkey(f"ctrl+5", lambda: updateFSByScreenCap(5,"gun"))


def updateFSByScreenCap(key, type):
    if key in firingSolutionDict:
        if type == "target":
            capDist, capAzi = ocr.screepCapExtract("target")
            firingSolutionDict[key].spotterToTargetDistance = capDist
            firingSolutionDict[key].spotterToTargetAzimuth = capAzi
            dpg.set_value(
                f"{key}2", float(f"{firingSolutionDict[key].spotterToTargetDistance:.2f}"))
            dpg.set_value(
                f"{key}3", float(f"{firingSolutionDict[key].spotterToTargetAzimuth:.2f}"))
        else:
            capDist, capAzi = ocr.screepCapExtract("gun")
            firingSolutionDict[key].spotterToGunDistance = capDist
            firingSolutionDict[key].spotterToGunAzimuth = capAzi
            dpg.set_value(
                f"{key}4", float(f"{firingSolutionDict[key].spotterToGunDistance:.2f}"))
            dpg.set_value(
                f"{key}5", float(f"{firingSolutionDict[key].spotterToGunAzimuth:.2f}"))

        firingSolutionDict[key].recalcGunToTarget()
        dpg.set_value(
            f"{key}6", float(f"{firingSolutionDict[key].adjustedGunToTargetDistance:.2f}"))
        dpg.set_value(
            f"{key}7", float(f"{firingSolutionDict[key].adjustedGunToTargetAzimuth:.2f}"))
    else:
        return

def fileOptions(sender, app_data):
    if app_data == "Open FS":
        filePath =  filedialog.askopenfilename(initialdir = "../firingSolutionTables",title = "Select file",filetypes = (("txt files", "*.txt"),("all files","*.*")))
        for idx in range(gunCounter):
            delete_guns()
        with open(filePath) as f:
            lines = f.readlines()
            for line in lines:
                add_guns()
                line = line.strip() # parse string
                valList = line.split(',')
                valList = [valList[0]] + list(map(float, valList[1:]))
                            # dpg.set_value(
                # f"{key}6", f"{firingSolutionDict[key].adjustedGunToTargetDistance:.2f}")
                dpg.set_value(f"{gunCounter}1",valList[0])
                dpg.set_value(f"{gunCounter}2",valList[1])
                dpg.set_value(f"{gunCounter}3",valList[2])
                dpg.set_value(f"{gunCounter}4",valList[3])
                dpg.set_value(f"{gunCounter}5",valList[4])
                dpg.set_value(f"{gunCounter}6",valList[5])
                dpg.set_value(f"{gunCounter}7",valList[6])

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
