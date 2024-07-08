import time
import random
import pyautogui


class MouseController:
    def __init__(self):
        # Initialize any necessary attributes
        random.seed("pingas")
        pass

    def click_random_in_box(self, x, y, width, height):
        """Click at a random point within the specified box."""
        random_x = random.randint(x, x + width)
        random_y = random.randint(y, y + height)
        pyautogui.click(random_x, random_y)

    def move_to_random_in_box(self, x, y, width, height):
        """Move the mouse to a random point within the specified box."""
        random_x = random.randint(x, x + width)
        random_y = random.randint(y, y + height)
        pyautogui.moveTo(random_x, random_y)

    def click_with_random_delay(
        self, x, y, width, height, min_delay=0.1, max_delay=0.5
    ):
        """Click at a random point within the box after a random delay."""
        self.move_to_random_in_box(x, y, width, height)
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        pyautogui.click()

    def click_no_random(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.click()

    def click_normal_random_delay(self, x, y, min_delay=0.1, max_delay=1):
        pyautogui.moveTo(x, y)
        timer = random.uniform(min_delay, max_delay)
        time.sleep(timer)
        pyautogui.click()
