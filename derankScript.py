import time
import ctypes
import pyautogui

#https://sourceforge.net/projects/mpos/

# DirectKeys setup
SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Function to simulate keyboard press
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Function to simulate keyboard release
def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Custom function to perform the needed key presses
def custom_press(key):
    # Key down
    PressKey(key)
    # Wait a bit
    time.sleep(0.05)
    # Key up
    ReleaseKey(key)

def main_loop():
    # 1. Wait 5 seconds to start the program
    time.sleep(5)

    while True:
        # 2 & 3: Click on the screen at provided locations.
        pyautogui.click(x, x)  # First click location
        pyautogui.click(x, x)  # Second click location, starts searching for a game

        # 4. Repeatedly check for RGB and location.
        while True:
            if pyautogui.pixelMatchesColor(x, x, (x, x, x)):  # Replace x with actual values
                break
            time.sleep(0.5)  # Check every half-second

        # 5 & 8. Press W and D keys every second, while searching for the forfeit button.
        while not pyautogui.pixelMatchesColor(x, x, (x, x, x)):  # Forfeit button location & RGB
            custom_press(0x11)  # W key
            custom_press(0x20)  # D key
            time.sleep(1)  # Delay specified to press every second

        # 7. If the forfeit button is found, press escape key and then click.
        custom_press(0x1B)  # Escape key
        pyautogui.click(x, x)

        # 9. Wait, click and then wait as specified.
        time.sleep(20)
        pyautogui.click(x, x)
        time.sleep(10)

if __name__ == "__main__":
    main_loop()
