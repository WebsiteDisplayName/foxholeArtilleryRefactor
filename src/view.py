import dearpygui.dearpygui as dpg
import ocr
import artilleryCalculator as aC
import calcHelper as cH
import dearpygui.dearpygui as dpg

dpg.create_context()

# https://dearpygui.readthedocs.io/en/latest/documentation/item-creation.html


global counter
counter = 0

firingSolutionDict = {}

# https://dearpygui.readthedocs.io/en/latest/documentation/tables.html


def add_guns():
    global counter
    counter += 1
    # new_button = dpg.add_button(
    #     label=f"Gun {counter}", before="gun_table", tag=f"new_gun{counter}")
    # with dpg.table_row(
    #         label=f"Gun {counter}", parent="gun_table", tag=f"new_gun{counter}"):
    #     dpg.add_button(label="fishsticks")
    # dpg.add_table_row(label=f"Gun {counter}",
    #                   before="gun_table", tag=f"new_gun{counter}")
    new_button = dpg.add_table_row(
        label=f"Gun {counter}", before="gun_table", tag=f"new_gun{counter}")


def delete_guns():
    global counter
    if counter >= 1:
        dpg.delete_item(f"new_gun{counter}")
        counter -= 1


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
