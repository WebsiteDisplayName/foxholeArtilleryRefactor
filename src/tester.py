
import keyboard
import controller as cT


if __name__ == "__main__":
    keyboard.add_hotkey(
        "shift+1", cT.updateFSByScreenCap(), args=[1, "target"])
    keyboard.add_hotkey("ctrl+1", cT.updateFSByScreenCap(), args=[1, "gun"])
