import dearpygui.dearpygui as dpg
import keyboard
from dearpygui_ext.themes import create_theme_imgui_dark

import artillery_calculator as aC
import calc_helper as cH
import controller as cT
import ocr

dpg.create_context()


with dpg.window(tag="Primary Window", label="main", pos=(200, 200)):
    with dpg.menu_bar(tag="mainMenuBar"):
        dpg.add_button(label="Add Guns", callback=cT.add_guns)
        dpg.add_button(
            label="Delete Guns", callback=cT.delete_guns, tag="delete_gun"
        )
        dpg.add_combo(
            tag="weaponDropdown",
            items=list(cH.WEAPONTYPEWINDFORCES.keys()),
            default_value=list(cH.WEAPONTYPEWINDFORCES.keys())[0],
            callback=cT.update_firing_solution,
            user_data=["global", 6],
            width=120,
        )

        dpg.add_text(default_value="Wind Force")
        dpg.add_combo(
            tag="wind_forceDropdown",
            items=[1, 2, 3],
            default_value=1,
            callback=cT.update_firing_solution,
            user_data=["global", 7],
            width=95,
        )
        dpg.add_text(default_value="Wind Azi")
        dpg.add_input_int(
            tag="globalwind_azimuth",
            default_value=0.0,
            step=0,
            step_fast=0,
            callback=cT.update_firing_solution,
            user_data=["global", 8],
            width=30,
        )
        dpg.add_combo(
            tag="file_optionsDropdown",
            items=["Open FS", "Save FS"],
            default_value="Open FS",
            callback=cT.file_options,
            width=100,
        )

    with dpg.table(tag="gun_table", header_row=True):
        dpg.add_table_column(label="Name")
        dpg.add_table_column(label="dist_st")
        dpg.add_table_column(label="azi_st")
        dpg.add_table_column(label="dist_sg")
        dpg.add_table_column(label="azi_sg")
        dpg.add_table_column(label="adjDistGT")
        dpg.add_table_column(label="adjAziGT")
        dpg.add_table_column(label="CHG adjDGT")
        dpg.add_table_column(label="CHG adjAGT")

    # https://www.reddit.com/r/DearPyGui/comments/iibfo8/how_to_dynamically_change_comboboxlistbox_items/
    # add_loading_indicator
    # configure_item

    # Grid Coord. Conv.
    with dpg.table(tag="grid_coordTable", header_row=True):
        dpg.add_table_column(label="Grid Conv.")
        dpg.add_table_column(label="")
        dpg.add_table_column(label="Ref. Gun Name")
        dpg.add_table_column(label="Gun Coord.")
        dpg.add_table_column(label="Target Coord.")
        dpg.add_table_column(label="Recalc. Grid ST")
        with dpg.table_row(tag="grid_coordRow"):
            dpg.add_text(default_value="")
            dpg.add_text(default_value="")
            dpg.add_combo(
                tag="gridGunDropdown",  # firing solution name ref
                parent="grid_coordRow",
                items=[],
            )
            dpg.add_input_text(
                tag="grid_coord1", default_value=""
            )  # dist_sg ref
            dpg.add_input_text(
                tag="grid_coord2", default_value=""
            )  # azi_sg ref
            dpg.add_button(
                tag="grid_coordButton",  # clicking prompts are you sure you want to recalculate sg?
                label="WARNING",
                callback=cT.grid_coord_conv,
            )

    with dpg.table(tag="globalSpotterTargetTable", header_row=True):
        dpg.add_table_column(label="ST Master")
        dpg.add_table_column(label="")
        dpg.add_table_column(label="")
        dpg.add_table_column(label="dist_st")
        dpg.add_table_column(label="azi_st")
        dpg.add_table_column(label="Recalc. ST")
        with dpg.table_row(tag="globalSpotterTargetRow"):
            dpg.add_text(default_value="")
            dpg.add_text(default_value="")
            dpg.add_text(default_value="")
            dpg.add_input_double(
                tag="spotterTargetDistChange",  # dist_sg ref
                default_value=0.0,
                step=0,
                step_fast=0,
                format="%.1f",
            )
            dpg.add_input_double(
                tag="spotterTargetAziChange",  # azi_sg ref
                default_value=0.0,
                step=0,
                step_fast=0,
                format="%.1f",
            )
            dpg.add_button(
                tag="targetChangeButton",  # clicking prompts are you sure you want to recalculate sg?
                label="WARNING",
                callback=cT.recalculate_st_values,
            )

    with dpg.table(tag="spotterChangeTable", header_row=True):
        dpg.add_table_column(label="SG Master")
        dpg.add_table_column(label="")
        dpg.add_table_column(label="Ref. Gun Name")
        dpg.add_table_column(label="dist_sg")
        dpg.add_table_column(label="azi_sg")
        dpg.add_table_column(label="Recalc. SG")
        with dpg.table_row(tag="spotterRow"):
            dpg.add_text(default_value="")
            dpg.add_text(default_value="")
            dpg.add_combo(
                tag="spotterPosDropdown",  # firing solution name ref
                parent="spotterRow",
                items=[],
            )
            dpg.add_input_double(
                tag="spotterGunDistChange",  # dist_sg ref
                default_value=0.0,
                step=0,
                step_fast=0,
                format="%.1f",
            )
            dpg.add_input_double(
                tag="spotterGunAziChange",  # azi_sg ref
                default_value=0.0,
                step=0,
                step_fast=0,
                format="%.1f",
            )
            dpg.add_button(
                tag="spotterChangeButton",  # clicking prompts are you sure you want to recalculate sg?
                label="WARNING",
                callback=cT.recalculate_sg_values,
            )

    with dpg.table(tag="windChangeTable", header_row=True):
        dpg.add_table_column(label="Wind Flag")
        dpg.add_table_column(label="dist_sf")
        dpg.add_table_column(label="azi_sf")
        dpg.add_table_column(label="dist_sp")
        dpg.add_table_column(label="azi_sp")
        dpg.add_table_column(label="Recalc. Wind Azi")
        with dpg.table_row(tag="windRow"):
            dpg.add_text(default_value="")
            dpg.add_input_double(
                tag="distSpotterToFlag",  # dist_st ref spotter to end of flag
                default_value=0.0,
                step=0,
                step_fast=0,
                format="%.1f",
            )
            dpg.add_input_double(
                tag="aziSpotterToFlag",  # azi_st ref
                default_value=0.0,
                step=0,
                step_fast=0,
                format="%.1f",
            )
            dpg.add_input_double(
                tag="distSpotterToPole",  # dist_sg ref spotter to pole
                default_value=0.0,
                step=0,
                step_fast=0,
                format="%.1f",
            )
            dpg.add_input_double(
                tag="aziSpotterToPole",  # azi_sg ref
                default_value=0.0,
                step=0,
                step_fast=0,
                format="%.1f",
            )
            dpg.add_button(
                tag="windChangeButton",  # push to global
                label="WARNING",
                callback=cT.global_wind_calc,
            )

    with dpg.table(tag="impliedWindChangeTable", header_row=True):
        dpg.add_table_column(label="Implied Wind Ref.")
        dpg.add_table_column(label="dist_si")
        dpg.add_table_column(label="azi_si")
        dpg.add_table_column(label="imp_wf")
        dpg.add_table_column(label="imp_wa")
        dpg.add_table_column(label="Push to Global")
        with dpg.table_row(tag="impliedWindRow"):
            dpg.add_combo(
                tag="impliedWindDropdown",  # firing solution name ref
                parent="impliedWindRow",
                items=[],
            )
            dpg.add_input_double(
                tag="distSpotterToImpact",  # dist_si
                default_value=0.0,
                step=0,
                step_fast=0,
                callback=cT.implied_wind_calc,
                format="%.1f",
            )
            dpg.add_input_double(
                tag="aziSpotterToImpact",  # azi_si
                default_value=0.0,
                step=0,
                step_fast=0,
                callback=cT.implied_wind_calc,
                format="%.1f",
            )
            dpg.add_input_text(tag="implied_wind_force", default_value=0.0)
            dpg.add_input_text(tag="impliedwind_azimuth", default_value=0.0)
            dpg.add_button(
                tag="impliedWindChangeButton",  # push to global
                label="WARNING",
                callback=cT.push_implied_wind_to_global,
            )

    with dpg.table(tag="horizDeflectionTable", header_row=True):
        dpg.add_table_column(label="Horiz. Defl.")
        dpg.add_table_column(label="Hold Constant")
        dpg.add_table_column(label="dist_gi")
        dpg.add_table_column(label="Azi. CHG")
        dpg.add_table_column(label="Offset Meters")
        dpg.add_table_column(label="")
        with dpg.table_row(tag="horizDeflectionRow"):
            dpg.add_text(default_value="")
            dpg.add_combo(
                tag="hold_constantDropdown",  # firing solution name ref
                parent="horizDeflectionRow",
                items=["dist_gi", "Azi.", "Offset Meters"],
                default_value="Azi.",
                width=120,
            )
            dpg.add_input_double(
                tag="distGunToImpactDeflection",  # dist_gi ref
                default_value=0.0,
                step=0,
                step_fast=0,
                callback=cT.horiz_defl_calc,
                user_data=["dist_gi"],
                format="%.1f",
            )
            dpg.add_input_double(
                tag="azimuth_deflection",  # Azi. ref
                default_value=1,
                step=0,
                step_fast=0,
                callback=cT.horiz_defl_calc,
                user_data=["Azi."],
                format="%.1f",
            )
            dpg.add_input_double(
                tag="offset_meters_deflection",  # Offset meters ref
                default_value=0.0,
                step=0,
                step_fast=0,
                callback=cT.horiz_defl_calc,
                user_data=["Offset Meters"],
                format="%.1f",
            )
            dpg.add_text(default_value="")

# themes https://github.com/hoffstadt/DearPyGui_Ext
# https://github.com/hoffstadt/DearPyGui/discussions/1636
# https://github.com/hoffstadt/DearPyGui_Ext/blob/master/dearpygui_ext/themes.py
# change color of viewport (top border of window) window title bar
# dark_theme = create_theme_imgui_dark()
# dpg.bind_theme(dark_theme)


dpg.create_viewport(title="Artillery Calculator", width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
# insert hotkeys https://stackoverflow.com/questions/65057228/python-keyboard-module-wait-for-user
# https://github.com/hoffstadt/DearPyGui/discussions/1582 switch to specific tab
# cT.set_hotkeys()
dpg.start_dearpygui()
dpg.destroy_context()
