import dearpygui.dearpygui as dpg
import ocr
import artilleryCalculator as aC
import calcHelper as cH
import dearpygui.dearpygui as dpg
import controller as cT

dpg.create_context()


with dpg.window(tag="Primary Window", label="main", pos=(200, 200)):
    with dpg.menu_bar():
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

#  I changed this: gun to change dropdown, new SG dist, new SG azi, button to trigger recalc callback for all firing solution SG values
    # with dpg.menu_bar(tag="spotterPosChangeMenuBar"):
    #     dpg.add_button(label="Add Guns")
        # dpg.add_combo(tag="spotterPosDropdown", items=[
        #               cT.firingSolutionDict[key].gunName for key, val in cT.firingSolutionDict.items()])

dpg.create_viewport(title='Artillery Calculator', width=600, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
