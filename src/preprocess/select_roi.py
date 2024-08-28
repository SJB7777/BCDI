import os

from typing import Optional

import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np
import numpy.typing as npt
from roi_rectangle import RoiRectangle


class RoiSelector:
    def __init__(self):
        self.drawing = False
        self.ix, self.iy = -1, -1
        self.fx, self.fy = -1, -1
        self.rect = None
        self.ax = None

    def on_mouse_press(self, event):

        if event.inaxes is not None:
            if event.button == 1:
                self.drawing = True
                self.ix, self.iy = int(event.xdata), int(event.ydata)
                self.fx, self.fy = self.ix, self.iy
                if self.rect is not None:
                    self.rect.remove()
                self.rect = patches.Rectangle((self.ix, self.iy), 1, 1, linewidth=1, edgecolor='r', facecolor='none')
                self.ax.add_patch(self.rect)
                plt.draw()

    def on_mouse_release(self, event):

        if event.inaxes is not None and self.drawing:
            self.drawing = False
            self.fx, self.fy = int(event.xdata), int(event.ydata)
            if self.rect is not None:
                self.rect.set_width(self.fx - self.ix)
                self.rect.set_height(self.fy - self.iy)
                plt.draw()

    def on_mouse_move(self, event):

        if event.inaxes is not None and self.drawing:
            self.fx, self.fy = int(event.xdata), int(event.ydata)
            if self.rect is not None:
                self.rect.set_width(self.fx - self.ix)
                self.rect.set_height(self.fy - self.iy)
                plt.draw()

    def select_roi(self, image: npt.NDArray) -> Optional[tuple[int, int, int, int]]:
        if image.ndim != 2:
            raise TypeError(f"Invalid shape {image.shape} for image data")
        fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.imshow(image)

        fig.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        fig.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

        plt.show()

        if self.ix == -1 or self.iy == -1 or self.fx == -1 or self.fy == -1:
            return None
        x1, y1 = min(self.ix, self.fx), min(self.iy, self.fy)
        x2, y2 = max(self.ix, self.fx), max(self.iy, self.fy)
        return (x1, y1, x2, y2)


if __name__ == "__main__":

    ran_image = np.random.randn(500, 1000)
    roi_rect = RoiSelector().select_roi(ran_image)
    print(roi_rect)
