import dearpygui.dearpygui as dpg
import ocr
import artilleryCalculator as aC
import calcHelper as cH


import dearpygui.dearpygui as dpg

dpg.create_context()

global counter
counter = 0


def add_buttons():
    global new_button1
    global counter
    counter += 1
    new_button1 = dpg.add_button(
        label="New Button", before="delete_button", tag=f"new_button{counter}")


def delete_buttons():
    global counter
    dpg.delete_item(f"new_button{counter}")
    counter -= 1


with dpg.window(label="Tutorial", pos=(200, 200)):
    dpg.add_button(label="Add Buttons", callback=add_buttons)
    dpg.add_button(label="Delete Buttons",
                   callback=delete_buttons, tag="delete_button")


dpg.create_viewport(title='Custom Title', width=600, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
