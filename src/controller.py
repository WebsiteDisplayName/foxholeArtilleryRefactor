import math
import re
from tkinter import filedialog

import dearpygui.dearpygui as dpg
import keyboard

import artillery_calculator as aC
import calc_helper as cH
import ocr

# https://dearpygui.readthedocs.io/en/latest/documentation/item-creation.html
# https://dearpygui.readthedocs.io/en/latest/tutorials/item-usage.html?highlight=current%20widget set values
# https://dearpygui.readthedocs.io/en/latest/documentation/item-callbacks.html
# https://dearpygui.readthedocs.io/en/latest/documentation/tables.html
GUN_COUNTER = 0
FIRING_SOLUTION_DICT = {}

# wind azimuth is direction it is going towards, 0 = wind is blowing North


def update_firing_solution(sender, app_data, user_data):
    var_to_change = user_data[1]
    match var_to_change:
        case 1:  # gun name I changed this
            FIRING_SOLUTION_DICT[user_data[0]].gun_name = app_data
            dpg.configure_item(
                "gridGunDropdown",
                items=[
                    FIRING_SOLUTION_DICT[key].gun_name
                    for key, val in FIRING_SOLUTION_DICT.items()
                ],
            )
            dpg.configure_item(
                "spotterPosDropdown",
                items=[
                    FIRING_SOLUTION_DICT[key].gun_name
                    for key, val in FIRING_SOLUTION_DICT.items()
                ],
            )
            dpg.configure_item(
                "impliedWindDropdown",
                items=[
                    FIRING_SOLUTION_DICT[key].gun_name
                    for key, val in FIRING_SOLUTION_DICT.items()
                ],
            )
        case 2:  # dist_st
            FIRING_SOLUTION_DICT[user_data[0]].spotter_target_distance = app_data
        case 3:  # azi_st
            FIRING_SOLUTION_DICT[user_data[0]].spotter_target_azimuth = app_data % 360
        case 4:  # dist_sg
            FIRING_SOLUTION_DICT[user_data[0]].spotter_gun_distance = app_data
        case 5:  # azi_sg
            FIRING_SOLUTION_DICT[user_data[0]].spotter_gun_azimuth = app_data % 360
        case 6:  # weapon type
            for key, fs in FIRING_SOLUTION_DICT.items():
                fs.weapon_type = app_data
                set_values(key, "adjusted")
            return
        case 7:  # wind force
            for key, fs in FIRING_SOLUTION_DICT.items():
                if isinstance(app_data, str):
                    fs.wind_force = app_data
                else:
                    fs.wind_force = int(app_data)
                set_values(key, "adjusted")
            return
        case 8:  # wind azimuth
            for key, fs in FIRING_SOLUTION_DICT.items():
                fs.wind_azimuth = int(app_data) % 360
                set_values(key, "adjusted")
            return
    set_values(user_data[0], "adjusted")


def set_values(key, type):  # key is key from dictionary, type = [adjusted, target, gun]
    FIRING_SOLUTION_DICT[key].recalc_gun_target()
    if type == "gunname":
        dpg.set_value(f"{key}1", FIRING_SOLUTION_DICT[key].gun_name)
    elif type == "target":
        dpg.set_value(
            f"{key}2", round(FIRING_SOLUTION_DICT[key].spotter_target_distance, 2)
        )
        dpg.set_value(
            f"{key}3", round(FIRING_SOLUTION_DICT[key].spotter_target_azimuth, 2)
        )
    elif type == "gun":
        dpg.set_value(
            f"{key}4", round(FIRING_SOLUTION_DICT[key].spotter_gun_distance, 2)
        )
        dpg.set_value(
            f"{key}5", round(FIRING_SOLUTION_DICT[key].spotter_gun_azimuth, 2)
        )
    elif type == "adjusted":
        dpg.set_value(
            f"{key}6", round(FIRING_SOLUTION_DICT[key].adjusted_gun_target_distance, 2)
        )
        dpg.set_value(
            f"{key}7", round(FIRING_SOLUTION_DICT[key].adjusted_gun_target_azimuth, 2)
        )
        dpg.set_value(
            f"{key}8",
            round(FIRING_SOLUTION_DICT[key].oldadjusted_gun_target_distance, 2),
        )
        dpg.set_value(
            f"{key}9",
            round(FIRING_SOLUTION_DICT[key].oldadjusted_gun_target_azimuth, 2),
        )


def add_guns():
    global GUN_COUNTER
    GUN_COUNTER += 1
    new_fs = aC.FiringSolution()
    FIRING_SOLUTION_DICT[GUN_COUNTER] = new_fs
    with dpg.table_row(parent="gun_table", tag=f"new_gun{GUN_COUNTER}"):
        dpg.add_input_text(
            tag=f"{GUN_COUNTER}1",
            default_value=f"Gun {GUN_COUNTER}",
            callback=update_firing_solution,
            user_data=[GUN_COUNTER, 1],
            width=80,
        )  # Name
        dpg.add_input_double(
            tag=f"{GUN_COUNTER}2",
            default_value=0.0,
            step=0,
            step_fast=0,
            callback=update_firing_solution,
            user_data=[GUN_COUNTER, 2],
            width=80,
            on_enter=True,
            format="%.1f",
        )  # dist_st
        dpg.add_input_double(
            tag=f"{GUN_COUNTER}3",
            default_value=0.0,
            step=0,
            step_fast=0,
            callback=update_firing_solution,
            user_data=[GUN_COUNTER, 3],
            width=80,
            on_enter=True,
            format="%.1f",
        )  # azi_st
        dpg.add_input_double(
            tag=f"{GUN_COUNTER}4",
            default_value=0.0,
            step=0,
            step_fast=0,
            callback=update_firing_solution,
            user_data=[GUN_COUNTER, 4],
            width=80,
            on_enter=True,
            format="%.1f",
        )  # dist_sg
        dpg.add_input_double(
            tag=f"{GUN_COUNTER}5",
            default_value=0.0,
            step=0,
            step_fast=0,
            callback=update_firing_solution,
            user_data=[GUN_COUNTER, 5],
            width=80,
            on_enter=True,
            format="%.1f",
        )  # azi_sg
        dpg.add_text(tag=f"{GUN_COUNTER}6", default_value=0.0)  # adjDistGT
        dpg.add_text(tag=f"{GUN_COUNTER}7", default_value=0.0)  # adjAziGT
        dpg.add_text(
            tag=f"{GUN_COUNTER}8", default_value=0.0
        )  # delta between old and new adjDistGT
        dpg.add_text(
            tag=f"{GUN_COUNTER}9", default_value=0.0
        )  # delta between old and new adjDistGT
    FIRING_SOLUTION_DICT[GUN_COUNTER].gun_name = f"Gun {GUN_COUNTER}"
    dpg.configure_item(
        "gridGunDropdown",
        items=[
            FIRING_SOLUTION_DICT[key].gun_name
            for key, val in FIRING_SOLUTION_DICT.items()
        ],
    )
    dpg.configure_item(
        "spotterPosDropdown",
        items=[
            FIRING_SOLUTION_DICT[key].gun_name
            for key, val in FIRING_SOLUTION_DICT.items()
        ],
    )
    dpg.configure_item(
        "impliedWindDropdown",
        items=[
            FIRING_SOLUTION_DICT[key].gun_name
            for key, val in FIRING_SOLUTION_DICT.items()
        ],
    )


def delete_guns():
    global GUN_COUNTER
    if GUN_COUNTER >= 1:
        dpg.delete_item(f"new_gun{GUN_COUNTER}")
        del FIRING_SOLUTION_DICT[GUN_COUNTER]
        GUN_COUNTER -= 1
    dpg.configure_item(
        "gridGunDropdown",
        items=[
            FIRING_SOLUTION_DICT[key].gun_name
            for key, val in FIRING_SOLUTION_DICT.items()
        ],
    )
    dpg.configure_item(
        "spotterPosDropdown",
        items=[
            FIRING_SOLUTION_DICT[key].gun_name
            for key, val in FIRING_SOLUTION_DICT.items()
        ],
    )
    dpg.configure_item(
        "impliedWindDropdown",
        items=[
            FIRING_SOLUTION_DICT[key].gun_name
            for key, val in FIRING_SOLUTION_DICT.items()
        ],
    )


def grid_coord_conv():
    # a1 top left, q15 bottom right
    # g9 125 meter side
    # g9k3: 41 meter side
    # g9k3k3: ~13.8 meter side
    # first calculate horizontal and vertical of both points in distance, then subtract
    # find length of two sides at 90, calc azimuth and distance of hypotenuse
    # tactic: a1 = top left of grid square, keypads add distance?
    ref_grid_gun_name = dpg.get_value("gridGunDropdown")
    gun_grid_coord = dpg.get_value("grid_coord1")
    target_grid_coord = dpg.get_value("grid_coord2")

    horiz_vals_gun = origin_dist_from_grid_coord(gun_grid_coord)
    horiz_vals_target = origin_dist_from_grid_coord(target_grid_coord)
    # azimuth is either 0 or 90, write up on paper
    dist_sg = horiz_vals_target[0] - horiz_vals_gun[0]
    dist_st = horiz_vals_target[1] - horiz_vals_gun[1]
    if dist_sg > 0:  # gets azimuth for calc
        azi_sg = 270
    else:
        azi_sg = 90
    dist_sg = abs(dist_sg)
    if dist_st > 0:
        azi_st = 0
    else:
        azi_st = 180
    dist_st = abs(dist_st)
    # spotter_target_azimuth, spotter_target_distance, spotter_gun_azimuth, spotter_gun_distance
    dist_gt = cH.find_distance_gun_target(azi_st, dist_st, azi_sg, dist_sg)
    azi_gt = cH.find_azimuth_gun_target(azi_st, dist_st, azi_sg, dist_sg)

    for key, val in FIRING_SOLUTION_DICT.items():
        if val.gun_name == ref_grid_gun_name:
            val.spotter_target_distance = dist_gt
            val.spotter_target_azimuth = azi_gt
            set_values(key, "target")
            set_values(key, "adjusted")


def origin_dist_from_grid_coord(grid_coord):
    # start in bottom left
    # g9k3: 41 meter side
    horiz_letters = list("abcdefghijklmnopq")
    vert_numbers = list(range(1, 16))

    horiz_letters_dict = dict(
        zip(horiz_letters, list(range(0, len(horiz_letters))))
    )  # 'a':0, 'b':1
    vert_numbers_dict = dict(
        zip(vert_numbers[::-1], list(range(0, len(vert_numbers))))
    )  # 15:0, 14:1, 1:14

    # https://www.reddit.com/r/foxholegame/comments/mopq7l/foxholes_map_is_64km2/
    region_horiz_length = 2184
    region_vert_length = 1890  # hard coded !
    grid_horiz_length = region_horiz_length / len(horiz_letters)
    grid_vert_length = region_vert_length / len(vert_numbers)

    # distance from botton left of grid map (A15)
    running_horizontal_distance = 0
    running_vertical_distance = 0
    # 789
    # 456
    # 123

    # !!!! redo handles g15k3k3, handles double digit vertical number
    # use regex on everything after first letter G(15K3K3)
    # aziDist = re.compile(r'[A-Za-z\. ]+(\d+)m[A-Za-z\. ]+(\d+)')
    # returnResult = aziDist.search(result).groups()

    try:
        x = re.search(r"(\w{1})(\d{1,})[Kk](\d)[Kk](\d)", grid_coord)
        horiz_letter = x.group(1).lower()
        vert_number = int(x.group(2))
        keypad = int(x.group(3))
        second_keypad = int(x.group(4))
        case = 1
    except Exception as e:
        x = re.search(r"(\w{1})(\d{1,})[Kk](\d)", grid_coord)
        horiz_letter = x.group(1).lower()
        vert_number = int(x.group(2))
        keypad = int(x.group(3))
        case = 2

    # handles grid square (G9)
    running_horizontal_distance += horiz_letters_dict[horiz_letter] * grid_horiz_length
    running_vertical_distance += vert_numbers_dict[vert_number] * grid_vert_length

    # handles keypad, convert to hor/vert distance
    # one part handles vertical and another conditional handles horiztonal
    if case == 1 or case == 2:
        running_horizontal_distance += (
            grid_horiz_length / 6
        )  # moves to middle of keypad 1
        running_vertical_distance += grid_vert_length / 6
        horiz_vert_vals = keypad_distance(
            grid_horiz_length / 3, grid_vert_length / 3, keypad
        )
        running_horizontal_distance += horiz_vert_vals[0]
        running_vertical_distance += horiz_vert_vals[1]
    # handles if additional keypad is added
    if case == 1:
        running_horizontal_distance -= grid_horiz_length / 6  # resets to bottom left
        running_vertical_distance -= grid_vert_length / 6
        running_horizontal_distance += (
            grid_horiz_length / 18
        )  # centers for smaller keypad
        running_vertical_distance += grid_vert_length / 18
        horiz_vert_vals = keypad_distance(
            grid_horiz_length / 9, grid_vert_length / 9, second_keypad
        )
        running_horizontal_distance += horiz_vert_vals[0]
        running_vertical_distance += horiz_vert_vals[1]
    return [running_horizontal_distance, running_vertical_distance]


def keypad_distance(horiz_keypad_length, vert_keypad_length, keypad):
    running_vertical_distance = 0
    running_horizontal_distance = 0
    if keypad in [4, 5, 6]:
        running_vertical_distance += vert_keypad_length
    elif keypad in [7, 8, 9]:
        running_vertical_distance += vert_keypad_length * 2

    if keypad in [2, 5, 8]:
        running_horizontal_distance += horiz_keypad_length
    elif keypad in [3, 6, 9]:
        running_horizontal_distance += horiz_keypad_length * 2

    return [running_horizontal_distance, running_vertical_distance]

    # return horizontal and vertical distance from grid coord


def recalculate_st_values():
    new_global_dist_st = dpg.get_value("spotterTargetDistChange")
    new_global_azi_st = dpg.get_value("spotterTargetAziChange") % 360
    for idx in range(1, GUN_COUNTER + 1):
        dpg.set_value(f"{idx}2", new_global_dist_st)
        dpg.set_value(f"{idx}3", new_global_azi_st)
        FIRING_SOLUTION_DICT[idx].spotter_target_distance = new_global_dist_st
        FIRING_SOLUTION_DICT[idx].spotter_target_azimuth = new_global_azi_st
        set_values(idx, "adjusted")


def recalculate_sg_values():
    ref_gun_name = dpg.get_value("spotterPosDropdown")
    new_ref_dist_sg = dpg.get_value("spotterGunDistChange")
    new_ref_azi_sg = dpg.get_value("spotterGunAziChange") % 360
    new_ref_azi_sg_back = (
        new_ref_azi_sg - 180 if new_ref_azi_sg >= 180 else new_ref_azi_sg + 180
    )
    # back azimuth
    # calculate internal gun relationships with respect to the ref_gun_name chosen with historical values then recalculate updated SG and update
    if len(FIRING_SOLUTION_DICT) >= 2:
        ref_key = -1
        for key, val in FIRING_SOLUTION_DICT.items():  # find key of chosen ref_gun_name
            if val.gun_name == ref_gun_name:
                ref_key = key
        if ref_key == -1:
            return
        # calculating everything relative to the chosen ref_gun_name, azimuth is traveling from ref to curr
        old_ref_sg_dist = FIRING_SOLUTION_DICT[ref_key].spotter_gun_distance
        old_ref_sg_azi = FIRING_SOLUTION_DICT[ref_key].spotter_gun_azimuth
        for key, val in FIRING_SOLUTION_DICT.items():
            if val.gun_name == ref_gun_name:
                continue
            # spotter_target_azimuth, spotter_target_distance, spotter_gun_azimuth, spotter_gun_distance
            curr_sg_dist = FIRING_SOLUTION_DICT[key].spotter_gun_distance
            curr_sg_azi = FIRING_SOLUTION_DICT[key].spotter_gun_azimuth
            ref_to_curr_azi = cH.find_azimuth_gun_target(
                curr_sg_azi, curr_sg_dist, old_ref_sg_azi, old_ref_sg_dist
            )
            ref_to_curr_dist = cH.find_distance_gun_target(
                curr_sg_azi, curr_sg_dist, old_ref_sg_azi, old_ref_sg_dist
            )
            new_curr_sg_azi = cH.find_azimuth_gun_target(
                ref_to_curr_azi, ref_to_curr_dist, new_ref_azi_sg_back, new_ref_dist_sg
            )
            new_curr_sg_dist = cH.find_distance_gun_target(
                ref_to_curr_azi, ref_to_curr_dist, new_ref_azi_sg_back, new_ref_dist_sg
            )
            dpg.set_value(f"{key}4", new_curr_sg_dist)
            dpg.set_value(f"{key}5", new_curr_sg_azi)
            FIRING_SOLUTION_DICT[key].spotter_gun_distance = new_curr_sg_dist
            FIRING_SOLUTION_DICT[key].spotter_gun_azimuth = new_curr_sg_azi
            set_values(key, "adjusted")
        # update ref
        dpg.set_value(f"{ref_key}4", new_ref_dist_sg)
        dpg.set_value(f"{ref_key}5", new_ref_azi_sg)
        FIRING_SOLUTION_DICT[ref_key].spotter_gun_distance = new_ref_dist_sg
        FIRING_SOLUTION_DICT[ref_key].spotter_gun_azimuth = new_ref_azi_sg
        set_values(ref_key, "adjusted")


def global_wind_calc():
    dist_sf = dpg.get_value("distSpotterToFlag")
    azi_sf = dpg.get_value("aziSpotterToFlag") % 360
    dist_sp = dpg.get_value("distSpotterToPole")
    azi_sp = dpg.get_value("aziSpotterToPole") % 360
    new_wind_azimuth = cH.find_azimuth_gun_target(azi_sf, dist_sf, azi_sp, dist_sp)
    dpg.set_value("globalwind_azimuth", new_wind_azimuth)
    for key in range(1, GUN_COUNTER + 1):
        FIRING_SOLUTION_DICT[key].wind_azimuth = new_wind_azimuth
        set_values(key, "adjusted")


def implied_wind_calc():
    ref_implied_gun_name = dpg.get_value("impliedWindDropdown")
    dist_si = dpg.get_value("distSpotterToImpact")
    azi_si = dpg.get_value("aziSpotterToImpact") % 360
    for key, val in FIRING_SOLUTION_DICT.items():
        if val.gun_name == ref_implied_gun_name:
            ref_key = key
            break
    # find_distance_gun_target(spotter_target_azimuth, spotter_target_distance, spotter_gun_azimuth, spotter_gun_distance)
    orig_dist_sg = FIRING_SOLUTION_DICT[ref_key].spotter_gun_distance
    orig_azi_sg = FIRING_SOLUTION_DICT[ref_key].spotter_gun_azimuth
    orig_dist_gt = FIRING_SOLUTION_DICT[ref_key].adjusted_gun_target_distance  # changed
    orig_azi_gt = FIRING_SOLUTION_DICT[ref_key].adjusted_gun_target_azimuth

    dist_gi = cH.find_distance_gun_target(azi_si, dist_si, orig_azi_sg, orig_dist_sg)
    azi_gi = cH.find_azimuth_gun_target(azi_si, dist_si, orig_azi_sg, orig_dist_sg)

    # implied wind force, implied wind azimuth
    imp_wf = cH.find_distance_gun_target(azi_gi, dist_gi, orig_azi_gt, orig_dist_gt)
    imp_wa = cH.find_azimuth_gun_target(azi_gi, dist_gi, orig_azi_gt, orig_dist_gt)

    dpg.set_value("implied_wind_force", f"{imp_wf:.2f}")
    dpg.set_value("impliedwind_azimuth", f"{imp_wa:.2f}")
    # have impval in row call callback, global push pushes whatever is in the cell to global & recalc


def push_implied_wind_to_global():
    implied_wind_force = float(dpg.get_value("implied_wind_force"))
    implied_wind_force_azimuth = float(dpg.get_value("impliedwind_azimuth")) % 360
    dpg.set_value("globalwind_azimuth", implied_wind_force_azimuth)

    implied_wind_force_strength = f"IWF: {implied_wind_force:.2f}"
    dpg.configure_item(
        "wind_forceDropdown", items=[1, 2, 3, implied_wind_force_strength]
    )
    dpg.set_value("wind_forceDropdown", implied_wind_force_strength)

    for key in range(1, GUN_COUNTER + 1):
        FIRING_SOLUTION_DICT[key].wind_force = implied_wind_force_strength
        FIRING_SOLUTION_DICT[key].wind_azimuth = implied_wind_force_azimuth
        set_values(key, "adjusted")


def horiz_defl_calc(sender, app_data, user_data):
    dist_gi = float(dpg.get_value("distGunToImpactDeflection"))
    azimuth_deflection = float(dpg.get_value("azimuth_deflection"))
    offset_meters_deflection = float(dpg.get_value("offset_meters_deflection"))
    hold_constant = str(dpg.get_value("hold_constantDropdown"))
    changed_input = user_data[0]
    option_list = ["dist_gi", "Azi.", "Offset Meters"]
    for val in option_list:
        if hold_constant == changed_input:
            return
        elif val not in [hold_constant, changed_input]:
            output_var = val

    if output_var == option_list[0]:  # dist_gi
        # find length of side isosceles triangle
        # (baseSide/2)/cosine(90-betaAngle/2)
        adjacent_angle_radians = math.radians(90 - azimuth_deflection / 2)
        new_dist_gi = (offset_meters_deflection / 2) / math.cos(
            adjacent_angle_radians
        )  # inputs radians
        dpg.set_value("distGunToImpactDeflection", new_dist_gi)
    elif output_var == option_list[1]:  # Azi
        new_azimuth_deflection = math.degrees(
            math.acos((2 * dist_gi**2 - offset_meters_deflection**2) / (2 * dist_gi**2))
        )
        dpg.set_value("azimuth_deflection", new_azimuth_deflection)
    elif output_var == option_list[2]:  # Offset Meters
        new_offset_meters_deflection = (
            math.sin(math.radians(azimuth_deflection)) * dist_gi
        )
        dpg.set_value("offset_meters_deflection", new_offset_meters_deflection)


def set_hotkeys():
    with open("keybinds.txt") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()  # parse string
            val_list = line.split(",")
            val_list[1] = int(val_list[1])
            keyboard.add_hotkey(
                val_list[0],
                lambda vals=val_list[1:]: updateFSByScreenCap(vals[0], vals[1]),
            )
            # 0 = keybind, 1 = which rows are affected, 2 = columns/type
            # black magic: https://stackoverflow.com/questions/21791482/split-list-into-different-variables


def updateFSByScreenCap(key, type):
    if key in FIRING_SOLUTION_DICT:
        if type == "target":
            capDist, capAzi = ocr.screepCapExtract("target")
            FIRING_SOLUTION_DICT[key].spotter_target_distance = capDist
            FIRING_SOLUTION_DICT[key].spotter_target_azimuth = capAzi
            set_values(key, "target")
        elif type == "gun":
            capDist, capAzi = ocr.screepCapExtract("gun")
            FIRING_SOLUTION_DICT[key].spotter_gun_distance = capDist
            FIRING_SOLUTION_DICT[key].spotter_gun_azimuth = capAzi
            set_values(key, "gun")
        elif type == "global":
            if key == 1:  # spotter to target global change
                capDist, capAzi = ocr.screepCapExtract("global1")
                dpg.set_value("spotterTargetDistChange", capDist)
                dpg.set_value("spotterTargetAziChange", capAzi)
                recalculate_st_values()
            elif key == 2:  # SG master
                capDist, capAzi = ocr.screepCapExtract("global2")
                dpg.set_value("spotterGunDistChange", capDist)
                dpg.set_value("spotterGunAziChange", capAzi)
                recalculate_sg_values()
            elif key == 3:  # global wind flag ctrl + V
                capDist, capAzi = ocr.screepCapExtract("global3")
                dpg.set_value("distSpotterToFlag", capDist)
                dpg.set_value("aziSpotterToFlag", capAzi)
                global_wind_calc()
            elif key == 4:  # global wind pole shift + V
                capDist, capAzi = ocr.screepCapExtract("global4")
                dpg.set_value("distSpotterToPole", capDist)
                dpg.set_value("aziSpotterToPole", capAzi)
                global_wind_calc()

        set_values(key, "adjusted")


def file_options(sender, app_data):
    if app_data == "Open FS":
        file_path = filedialog.askopenfilename(
            initialdir="../firingSolutionTables",
            title="Select file",
            filetypes=(("txt files", "*.txt"), ("all files", "*.*")),
        )
        if file_path == "":
            return
        for _ in range(GUN_COUNTER):
            delete_guns()
        with open(file_path) as f:
            lines = f.readlines()
            for line in lines:
                add_guns()
                line = line.strip()  # parse string
                val_list = line.split(",")
                val_list = [val_list[0]] + list(map(float, val_list[1:]))

                FIRING_SOLUTION_DICT[GUN_COUNTER].gun_name = val_list[0]
                FIRING_SOLUTION_DICT[GUN_COUNTER].spotter_target_distance = val_list[1]
                FIRING_SOLUTION_DICT[GUN_COUNTER].spotter_target_azimuth = val_list[2]
                FIRING_SOLUTION_DICT[GUN_COUNTER].spotter_gun_distance = val_list[3]
                FIRING_SOLUTION_DICT[GUN_COUNTER].spotter_gun_azimuth = val_list[4]
                FIRING_SOLUTION_DICT[GUN_COUNTER].adjusted_gun_target_distance = (
                    val_list[5]
                )
                FIRING_SOLUTION_DICT[GUN_COUNTER].adjusted_gun_target_azimuth = (
                    val_list[6]
                )
                set_values(GUN_COUNTER, "gunname")
                set_values(GUN_COUNTER, "target")
                set_values(GUN_COUNTER, "gun")
                set_values(GUN_COUNTER, "adjusted")

    # https://stackoverflow.com/questions/11295917/how-to-select-a-directory-and-store-the-location-using-tkinter-in-python
    elif app_data == "Save FS":  # open folder, save text as what gui?
        file_path = filedialog.asksaveasfilename(
            initialdir="../firingSolutionTables",
            title="File name to save as",
            filetypes=(("txt files", "*.txt"), ("all files", "*.*")),
        )
        with open(file_path + ".txt", "w") as f:
            for row in range(1, GUN_COUNTER + 1):
                for column in range(1, 8):  # 7 columns
                    f.write(str(dpg.get_value(f"{row}{column}")))
                    if column == 7:
                        f.write("\n")
                        continue
                    f.write(",")


# open and store firingSolutions in .txt and add keybinds to set_hotkeys


if __name__ == "__main__":

    keyboard.add_hotkey("shift+1", updateFSByScreenCap(), args=(1, "target"))
    keyboard.add_hotkey("ctrl+1", updateFSByScreenCap(), args=(1, "gun"))
