## routines/BasicRoutines.py

import logging
import win32gui
import win32con
import win32api
import time
import win32con
import asyncio
from .utils.log_setup import setup_logging
from .utils.utilities import CriticalError

#log setup from /routines/utils/log_setup.py#
setup_logging()

## BASIC FUNCTIONS ##
def BasicRoutineGetInfoAllWowWindows():
    # Function to get information about all World of Warcraft (WoW) windows
    # Returns a dictionary with information about each identified window
    # Create an empty dictionary to store WoW window information
    wow_windows = {}
    # Loop from 1 to 99 to search for windows with titles starting with "is" + loop number
    for i in range(1, 100):
        window_title_prefix = "is" + str(i)  # Window title prefix
        hwnd = win32gui.FindWindow(None, None)  # Get the handle of the first found window
        # Loop to iterate through all found windows
        while hwnd:
            window_title = win32gui.GetWindowText(hwnd)  # Get the window title
            if window_title.startswith(window_title_prefix):  # Check if the title starts with the expected prefix
                window_rect = win32gui.GetWindowRect(hwnd)  # Get the window coordinates and size
                window_x = window_rect[0]  # Window X coordinate
                window_y = window_rect[1]  # Window Y coordinate
                window_width = window_rect[2] - window_x  # Window width
                window_height = window_rect[3] - window_y  # Window height
                window_info = {
                    "number": i,  # Window number
                    "title": window_title,  # Window title
                    "height": window_height,  # Window height
                    "width": window_width,  # Window width
                    "x": window_x,  # Window X coordinate
                    "y": window_y,  # Window Y coordinate
                    "hwnd": hwnd  # Window handle
                }
                wow_windows[i] = window_info  # Add the window information to the dictionary
                break
            hwnd = win32gui.FindWindowEx(None, hwnd, None, None)  # Get the handle of the next window
    return wow_windows  # Return the dictionary with WoW window information

import logging
import time
import pyautogui


async def BasicRoutineSendMouseClickAllWowWindows(whocallthisfunction, mouse_button, window_number, x, y, click_count):
    thisroutinename = "BasicRoutineSendMouseClickAllWowWindows"
    logging.debug("[BasicRoutineSendMouseClickAllWowWindows] Debug mode enabled")    
    if not isinstance(mouse_button, str) or mouse_button.lower() not in ["left", "right"]:
        logging.critical(f"[{whocallthisfunction}]->[{thisroutinename}] = Invalid mouse Button. Use 'left' or 'right'.")
        return False
    if not isinstance(window_number, int) or not (1 <= window_number <= 99):
        logging.critical(f"[{whocallthisfunction}]->[{thisroutinename}] = Invalid window number. Use a number between 1-99.")
        return False
    if not isinstance(x, int) or not isinstance(y, int):
        logging.critical(f"[{whocallthisfunction}]->[{thisroutinename}] = Invalid X and Y coordenates. Both must be integer numbers.")
        return False
    if not isinstance(click_count, int) or not (1 <= click_count <= 99):
        logging.critical(f"[{whocallthisfunction}]->[{thisroutinename}] = Invalid number of clicks. Use a number between [1-99].")
        return False
    wow_windows = BasicRoutineGetInfoAllWowWindows()
    if window_number not in wow_windows:
        logging.critical(f"[{whocallthisfunction}]->[{thisroutinename}] = The window {window_number} was not found.")
        return False
    button = "left" if mouse_button.lower() == "left" else "right"
    initial_mouse_pos = pyautogui.position()
    for _ in range(click_count):
        for window_num, window in wow_windows.items():
            window_x = window["x"] + int(x * window["width"] / wow_windows[window_number]["width"])
            window_y = window["y"] + int(y * window["height"] / wow_windows[window_number]["height"])
            pyautogui.click(window_x, window_y, button=button)
            time.sleep(0.3)
            logging.debug(f"[{whocallthisfunction}]->[BasicRoutineSendMouseClickAllWowWindows] Clicking with {mouse_button} mouse button in the windows {window_num} at position {window_x - window['x']},{window_y - window['y']}")
        # Return mouse to initial position after clicking in all windows
        time.sleep(0.5)
        logging.debug(f"[{whocallthisfunction}]->[BasicRoutineSendMouseClickAllWowWindows] Returning mouse to initial position")
        pyautogui.moveTo(initial_mouse_pos)
    return True

async def BasicRoutineSendKeyAllWowWindows(whocallthisfunction,window_number, key, key_press_count):
    thisroutinename = "BasicRoutineSendKeyAllWowWindows"
    logging.debug("[BasicRoutineSendKeyAllWowWindows] Debug mode enabled")
    if not isinstance(window_number, int) or not (1 <= window_number <= 99):
        logging.critical(f"[{whocallthisfunction}]->[{thisroutinename}] = Invalid window number. Use a number between 1-99.")
        return False
    if not isinstance(key, str) or (len(key) != 1 and key not in ['ESC', 'SPACE']):
        logging.critical(f"[{whocallthisfunction}]->[{thisroutinename}] = Invalid key to press. Must be one digit [a-z], [0-9], ESC or SPACE.") 
        return False
    if not isinstance(key_press_count, int) or not (1 <= key_press_count <= 99):
        logging.critical(f"[{whocallthisfunction}]->[{thisroutinename}] = Invalid Key pressing count. Must be [1-99]")
        return False
    wow_windows = BasicRoutineGetInfoAllWowWindows()
    if window_number not in wow_windows:
        logging.critical(f"[{whocallthisfunction}]->[{thisroutinename}] = The window {window_number} was not found.")
        return False
    target_window = wow_windows[window_number]
    if key == 'ESC':
        vk_code = win32con.VK_ESCAPE
    elif key == 'SPACE':
        vk_code = win32con.VK_SPACE
    else:
        vk_code = win32api.VkKeyScanEx(key, 0)
    def send_key_to_window(window_hwnd):
        win32gui.SendMessage(window_hwnd, win32con.WM_KEYDOWN, vk_code, 0)
        #time.sleep(0.1)
        win32gui.SendMessage(window_hwnd, win32con.WM_KEYUP, vk_code, 0)
        #time.sleep(0.1)
    loop_count = 0
    while loop_count < key_press_count:
        # Send key to the target window.
        send_key_to_window(target_window["hwnd"])
        logging.debug(f"[{whocallthisfunction}]->[BasicRoutineSendKeyAllWowWindows] Key '{key}' sended to window {window_number}.")
        # Send key to other windows too.
        for other_window_number, other_window in wow_windows.items():
            if other_window_number != window_number:
                send_key_to_window(other_window["hwnd"])
                logging.debug(f"[{whocallthisfunction}]->[BasicRoutineSendKeyAllWowWindows] Key '{key}' sended to window {other_window_number}.")
        #time.sleep(1)
        loop_count += 1
    logging.debug(f"[{whocallthisfunction}]->[BasicRoutineSendKeyAllWowWindows] Key '{key}' sended to all windows {key_press_count} times.")
    return True