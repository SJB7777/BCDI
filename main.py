import numpy as np
import matplotlib.pyplot as plt
from roi_rectangle import RoiRectangle

from src.preprocess.select_roi import RoiSelector


def main() -> None:

    exp_id: str = '240608_FXS'
    run_n: int = 144
    file: str = f"Y:\\{exp_id}\\analysis_data\\processed_data\\run={run_n:03}\\scan=001\\run={run_n:04}_scan=0001.npz"
    print(f'Loading file: {file}')

    data = np.load(file)
    if 'poff' in data:
        images = data['poff']
    elif 'pon' in data:
        images = data['pon']

    roi: tuple[int, int, int, int] = RoiSelector().select_roi(np.log1p(images.sum(axis=0)))
    roi_rect: RoiRectangle = RoiRectangle.from_tuple(roi)
    print(roi_rect)

    roi_images = roi_rect.slice(images)
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.imshow(np.log1p(roi_images.sum(axis=0)))
    plt.show()


if __name__ == '__main__':
    main()
