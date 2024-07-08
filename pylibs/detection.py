import cv2
import numpy as np
import matplotlib.pyplot as plt


class TemplateMatcher:
    def __init__(self):
        pass

    def preprocess_image(self, image):
        if isinstance(image, str):
            image = cv2.imread(image)
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        edges = cv2.Canny(gray, 50, 150)
        return edges

    def match_template(self, image, template, threshold=0.62524):
        image_edges = self.preprocess_image(image)
        template_edges = self.preprocess_image(template)

        heights, widths = [0.5, 0.75, 1, 1.25, 1.5], [0.5, 0.75, 1, 1.25, 1.5]
        matches = []

        for h in heights:
            for w in widths:
                resized = cv2.resize(
                    template_edges, None, fx=w, fy=h, interpolation=cv2.INTER_AREA
                )
                res = cv2.matchTemplate(image_edges, resized, cv2.TM_CCOEFF_NORMED)
                loc = np.where(res >= threshold)
                for pt in zip(*loc[::-1]):
                    matches.append(
                        (
                            int(pt[0] + (template.shape[1] * w) / 2),  # center x
                            int(pt[1] + (template.shape[0] * h) / 2),  # center y
                            int(template.shape[1] * w),
                            int(template.shape[0] * h),
                        )
                    )

        return self.remove_duplicates(matches)

    def remove_duplicates(self, matches, distance_threshold=10):
        if not matches:
            return []

        def distance(p1, p2):
            return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

        unique_matches = []
        for match in matches:
            if not any(
                distance(match, unique_match) < distance_threshold
                for unique_match in unique_matches
            ):
                unique_matches.append(match)

        return unique_matches

    def find_matches(self, image, templates):
        if not isinstance(templates, list):
            templates = [templates]  # Convert single template to list

        results = []
        for template in templates:
            matches = self.match_template(image, template)
            results.extend(matches)
        return self.remove_duplicates(results)

    def get_match_coordinates(self, image, templates):
        if isinstance(image, str):
            image = cv2.imread(image)

        if isinstance(templates, str):
            templates = [cv2.imread(templates)]
        elif isinstance(templates, np.ndarray):
            templates = [templates]
        elif isinstance(templates, list):
            templates = [
                cv2.imread(path) if isinstance(path, str) else path
                for path in templates
            ]

        results = self.find_matches(image, templates)

        return results  # Now returning full results (center_x, center_y, w, h)

    def debug_matches(self, image, templates):
        if isinstance(image, str):
            image = cv2.imread(image)

        if isinstance(templates, str):
            templates = [cv2.imread(templates)]
        elif isinstance(templates, np.ndarray):
            templates = [templates]
        elif isinstance(templates, list):
            templates = [
                cv2.imread(path) if isinstance(path, str) else path
                for path in templates
            ]

        results = self.find_matches(image, templates)
        self._plot_results(image, results)

        coordinates = [(x, y) for (x, y, _, _) in results]

        return results, coordinates

    def _plot_results(self, image, results):
        fig, ax = plt.subplots(1, figsize=(12, 8))
        ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        for x, y, w, h in results:
            circle = plt.Circle((x, y), min(w, h) / 4, color="r", fill=False)
            ax.add_artist(circle)
            rect = plt.Rectangle(
                (x - w / 2, y - h / 2), w, h, fill=False, edgecolor="g"
            )
            ax.add_patch(rect)

        plt.title(f"Found {len(results)} matches")
        plt.axis("off")
        plt.show()
