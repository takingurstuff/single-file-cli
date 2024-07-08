import os
from screenshot import Screenshot
from clicker import MouseController
from detection import TemplateMatcher


def screenshots():
    capture = Screenshot()
    matcher = TemplateMatcher()
    mouse = MouseController()

    templatedir = "/Volumes/T0/sfc/pylibs/templates"
    tmpdldir = "/Volumes/T0/sftmpdl"
    templates = os.listdir(templatedir)
    templatePaths = [os.path.join(templatedir, i) for i in templates]

    pageImage = capture.auto_screenshot_with_save(os.path.join(tmpdldir, "Screenshot"))

    results = matcher.get_match_coordinates(pageImage, templatePaths)

    for i, (x, y, w, h) in enumerate(results, 1):
        print(f"Match {i}: Top-left corner at (x={x}, y={y}), width={w}, height={h}")

        # Perform a mouse action for each match
        mouse.click_normal_random_delay(x, y)
