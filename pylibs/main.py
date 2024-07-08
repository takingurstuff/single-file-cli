import os
import time
import random
from screenshot import Screenshot
from clicker import MouseController
from detection import TemplateMatcher

if __name__ == "__main__":
    matcher = TemplateMatcher()
    mouse_controller = MouseController()
    screenshot = Screenshot(trigger_key="f1")

    template_dir = "./pylibs/templates"
    template_paths = os.listdir(template_dir)
    if "note to anyone who might visit this area" in template_paths:
        template_paths.remove("note to anyone who might visit this area")
    full_template_paths = [os.path.join(template_dir, i) for i in template_paths]
    if len(template_paths) == 0:
        print("no templates to use")
        raise FileNotFoundError("empty templates directory")
    image = screenshot.screenshot_no_save()

    # Initialize variables
    results = []

    # For getting coordinates and dimensions (production use)
    results = matcher.get_match_coordinates(image, full_template_paths)
    print("Matches found:", results)

    # For debugging with visual output
    # debug_results, _ = matcher.debug_matches(image, template_path)
    # if debug_results:
    #    results = debug_results

    # Final print loop and mouse interaction
    if results:
        print(f"\nFound {len(results)} matches:")
        for i, (x, y, w, h) in enumerate(results, 1):
            print(
                f"Match {i}: Top-left corner at (x={x}, y={y}), width={w}, height={h}"
            )

            # Perform a mouse action for each match
            mouse_controller.click_normal_random_delay(x, y)
            print(f"Clicked on match {i}")

            # Add a delay between actions (optional)
            time.sleep(random.uniform(0.5, 1.5))
    else:
        print("\nNo matches found.")
