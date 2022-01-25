from PIL import Image
import numpy as np

import matplotlib.pyplot as plt

if __name__ == "__main__":
    filename = "img.jpg"
    img = Image.open(filename)
    img = np.array(img.convert("L"))

    # threshold 1
    img[img < 91] = 50

    # threshold 2
    img[img > 153] = 255

    # threshold 3 (leftover)
    img[np.logical_and(img >= 91, img <= 153)] = 150

    plt.figure()
    plt.imshow(img, cmap="gray")
    plt.show()

    pil_img = Image.fromarray(img)
    pil_img.save("out.png")
