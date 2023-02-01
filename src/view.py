import dearpygui.dearpygui as dpg
import ocr
import artilleryCalculator as aC
import calcHelper as cH
import dearpygui.dearpygui as dpg

dpg.create_context()

# https://dearpygui.readthedocs.io/en/latest/documentation/item-creation.html


# https://dearpygui.readthedocs.io/en/latest/documentation/tables.html
global gunCounter
gunCounter = 0
firingSolutionDict = {}


def add_guns():
    global gunCounter
    gunCounter += 1
    newFS = aC.firingSolution()
    firingSolutionDict[gunCounter] = newFS
    with dpg.table_row(parent="gun_table", tag=f"new_gun{gunCounter}"):
        dpg.add_text(label=f"##{gunCounter}1",
                     default_value=f"Gun {gunCounter}")  # Name
        dpg.add_input_int(label=f"##{gunCounter}2",
                          default_value=newFS.spotterToTargetDistance, step=0, step_fast=0)  # distST
        dpg.add_input_int(label=f"##{gunCounter}3",
                          default_value=newFS.spotterToTargetAzimuth, step=0, step_fast=0)  # aziST
        dpg.add_input_int(label=f"##{gunCounter}4",
                          default_value=newFS.spotterToGunDistance, step=0, step_fast=0)  # distSG
        dpg.add_input_int(label=f"##{gunCounter}5",
                          default_value=newFS.spotterToGunAzimuth, step=0, step_fast=0)  # aziSG
        dpg.add_input_int(label=f"##{gunCounter}6",
                          default_value=newFS.adjustedGunToTargetDist, step=0, step_fast=0)  # adjDistGT
        dpg.add_input_int(label=f"##{gunCounter}7",
                          default_value=newFS.adjustedGunToTargetAzimuth, step=0, step_fast=0)  # adjAziGT


def delete_guns():
    global gunCounter
    if gunCounter >= 1:
        dpg.delete_item(f"new_gun{gunCounter}")
        del firingSolutionDict[gunCounter]
        gunCounter -= 1


with dpg.window(tag="Primary Window", label="main", pos=(200, 200)):
    with dpg.menu_bar():
        dpg.add_button(label="Add Guns", callback=add_guns)
        dpg.add_button(label="Delete Guns",
                       callback=delete_guns, tag="delete_gun")

    with dpg.table(tag="gun_table", header_row=True):
        dpg.add_table_column(label="Name")
        dpg.add_table_column(label="distST")
        dpg.add_table_column(label="aziST")
        dpg.add_table_column(label="distSG")
        dpg.add_table_column(label="aziSG")
        dpg.add_table_column(label="adjDistGT")
        dpg.add_table_column(label="adjAziGT")

dpg.create_viewport(title='Artillery Calculator', width=600, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
