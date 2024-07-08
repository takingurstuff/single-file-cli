import cv2
import threading
import numpy as np
from pynput import keyboard
import pyscreenshot as ImageGrab


class Screenshot:
    def __init__(self, trigger_key="end"):
        self.key_pressed = threading.Event()
        self.trigger_key = self.parse_key(trigger_key)
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def parse_key(self, key_string):
        if hasattr(keyboard.Key, key_string):
            return getattr(keyboard.Key, key_string)
        else:
            return keyboard.KeyCode.from_char(key_string)

    def on_press(self, key):
        if key == self.trigger_key:
            self.key_pressed.set()

    def wait_for_keypress(self):
        print(f"Press '{self.trigger_key}' to capture the screenshot...")
        self.key_pressed.wait()
        self.key_pressed.clear()

    def screenshot_no_save(self):
        self.wait_for_keypress()
        print("Capturing screenshot...")
        screenshot = ImageGrab.grab()

        # Convert PIL Image to numpy array
        screenshot_np = np.array(screenshot)

        # Convert RGB to BGR (OpenCV uses BGR)
        screenshot_cv2 = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        print("Screenshot captured!")
        return screenshot_cv2

    def screenshot_saved(self, savefilename):
        self.wait_for_keypress()
        print("Capturing screenshot...")
        screenshot = ImageGrab.grab()
        # Convert PIL Image to numpy array
        screenshot_np = np.array(screenshot)

        # Convert RGB to BGR (OpenCV uses BGR)
        screenshot_cv2 = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

        screenshot.save(savefilename)
        print(f"Screenshot saved as {savefilename}")
        return screenshot_cv2

    def auto_screenshot_no_save():
        screenshot = ImageGrab.grab()

        screenshot_intermediate = np.array(screenshot)

        final_screenshot = cv2.cvtColor(screenshot_intermediate, cv2.COLOR_RGB2BGR)

        return final_screenshot

    def auto_screenshot_with_save(filepath):
        screenshot = ImageGrab.grab()

        screenshot_intermediate = np.array(screenshot)

        final_screenshot = cv2.cvtColor(screenshot_intermediate, cv2.COLOR_RGB2BGR)

        screenshot.save(filepath)

        return final_screenshot

    def __del__(self):
        self.listener.stop()
