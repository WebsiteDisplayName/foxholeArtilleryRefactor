import dearpygui.dearpygui as dpg
import ocr
import artilleryCalculator as aC
import calcHelper as cH
import dearpygui.dearpygui as dpg
import controller as cT
from dearpygui_ext.themes import create_theme_imgui_dark
import keyboard
dpg.create_context()


with dpg.window(tag="Primary Window", label="main", pos=(200, 200)):
    with dpg.menu_bar(tag="mainMenuBar"):
        dpg.add_button(label="Add Guns", callback=cT.add_guns)
        dpg.add_button(label="Delete Guns",
                       callback=cT.delete_guns, tag="delete_gun")
        dpg.add_combo(tag="weaponDropdown", items=["120mm & 150mm", "Storm cannon",
                      "Mortars"], default_value="120mm & 150mm", callback=cT.updateFiringSolution, user_data=["global", 6], width=120)

        dpg.add_text(default_value="Wind Force")
        dpg.add_combo(tag="windForceDropdown", items=[1, 2, 3], default_value=1,
                      callback=cT.updateFiringSolution, user_data=["global", 7], width=30)
        dpg.add_text(default_value="Wind Azi")
        dpg.add_input_int(tag="windAziDropdown",
                          default_value=0, step=0, step_fast=0, callback=cT.updateFiringSolution, user_data=["global", 8], width=30)

    with dpg.table(tag="gun_table", header_row=True):
        dpg.add_table_column(label="Name")
        dpg.add_table_column(label="distST")
        dpg.add_table_column(label="aziST")
        dpg.add_table_column(label="distSG")
        dpg.add_table_column(label="aziSG")
        dpg.add_table_column(label="adjDistGT")
        dpg.add_table_column(label="adjAziGT")

# https://www.reddit.com/r/DearPyGui/comments/iibfo8/how_to_dynamically_change_comboboxlistbox_items/
# add_loading_indicator
# configure_item
    with dpg.table(tag="spotterChangeTable", header_row=True):
        dpg.add_table_column(label="Ref. Gun Name")
        dpg.add_table_column(label="distSG")
        dpg.add_table_column(label="aziSG")
        dpg.add_table_column(label="Recalc. SG")
        with dpg.table_row(tag=f"spotterRow"):
            dpg.add_combo(tag="spotterPosDropdown",  # firing solution name ref
                          parent="spotterRow", items=[], width=80)
            dpg.add_input_int(tag=f"spotterGunDistChange",  # distSG ref
                              default_value=0, step=0, step_fast=0, width=80)
            dpg.add_input_int(tag=f"spotterGunAziChange",  # aziSG ref
                              default_value=0, step=0, step_fast=0, width=80)
            dpg.add_button(tag=f"spotterChangeButton",  # clicking prompts are you sure you want to recalculate sg?
                           label="WARNING", width=80, callback=cT.recalculateSGValues)

# themes https://github.com/hoffstadt/DearPyGui_Ext
# https://github.com/hoffstadt/DearPyGui/discussions/1636
# https://github.com/hoffstadt/DearPyGui_Ext/blob/master/dearpygui_ext/themes.py
# change color of viewport (top border of window) window title bar
    # dark_theme = create_theme_imgui_dark()
    # dpg.bind_theme(dark_theme)


dpg.create_viewport(title='Artillery Calculator', width=600, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
cT.setHotkeys() # insert hotkeys https://stackoverflow.com/questions/65057228/python-keyboard-module-wait-for-user
dpg.start_dearpygui()
dpg.destroy_context()
