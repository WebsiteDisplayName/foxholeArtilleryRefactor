import dearpygui.dearpygui as dpg
import artilleryCalculator as aC

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


def recalculateSGValues():
    refGunName = dpg.get_value("spotterPosDropdown")
    newRefDistSG = dpg.get_value("spotterGunDistChange")
    newRefAziSG = dpg.get_value("spotterGunAziChange")
    # calculate internal gun relationships with respect to the refGunName chosen with historical values then recalculate updated SG and update
    if len(firingSolutionDict) >= 2:
        refKey = -1
        for key, val in firingSolutionDict.items():  # find key of chosen refGunName
            if val.gunName == refGunName:
                refKey = key

        for key, val in firingSolutionDict.items():
