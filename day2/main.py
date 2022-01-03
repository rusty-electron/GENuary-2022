import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# for blue noise
# credit: https://github.com/MomentsInGraphics/BlueNoise
import BlueNoise

# for error diffusion dithering, I found a library
# named hitherdither: https://github.com/hbldh/hitherdither and decided to use it
import hitherdither

FILENAME = "source_scaled.jpg"

def perform_simple_quant(img, threshold):
    return (img > threshold).astype(np.int)

def perform_random_quant(img):
    h, w = img.shape
    noise = np.random.rand(h, w)
    return (img > noise).astype(np.int)

BAYER_0 = np.array([[0, 2], [3, 1]])

def construct_bayer_n(n_val):
    if n_val == 0:
        return BAYER_0
    else:
        top = np.hstack((4 * construct_bayer_n(n_val - 1) + 0,
                4 * construct_bayer_n(n_val - 1) + 2))
        bottom = np.hstack((4 * construct_bayer_n(n_val - 1) + 3,
                4 * construct_bayer_n(n_val - 1) + 1))
        return np.vstack((top, bottom))

def bayer_dithering(img, mat):
    h_im, w_im = img.shape
    h_mat, w_mat = mat.shape
    assert h_mat == w_mat, "the bayer matrix must be a square matrix"
    bayer_num = np.log2(h_mat) - 1
    tiled_mat = np.tile(mat, (h_im//h_mat + 1, w_im//w_mat + 1)) * (1/(2**(2*bayer_num + 2)))
    return perform_simple_quant(img, tiled_mat[:h_im, :w_im])

def add_random_noise(img, val = 0.5):
    h, w = img.shape
    noise = np.random.rand(h, w) - val
    return img + noise

if __name__ == "__main__":
    # read img
    org_img = Image.open(FILENAME)

    # convert to grayscale
    gray_img_uint = org_img.convert('L')
    gray_img = np.array(gray_img_uint) / 255

    # exhibit 0: random uniform noise -> simple quantization
    # res = perform_simple_quant(add_random_noise(gray_img), 0.5)

    # exhibit 1:
    # res = perform_random_quant(gray_img)

    # exhibit 2: bayer dithering
    # bayer_matrix = construct_bayer_n(3)
    # res = bayer_dithering(gray_img, bayer_matrix)

    # exhibit 3: blue noise
    # h_im, w_im = gray_img.shape
    # BN_SIZE = 64
    # texture = BlueNoise.GetVoidAndClusterBlueNoise((BN_SIZE, BN_SIZE), 1.9)
    # texture = texture / np.max(texture)

    # tiled_texture = np.tile(texture, (h_im//BN_SIZE + 1, w_im//BN_SIZE + 1))
    # res = perform_simple_quant(gray_img, tiled_texture[:h_im, :w_im])

    # exhibit 4: error diffusion dithering
    # possible methods
    # "floyd-steinberg" - default
    # "atkinson"
    # "jarvis-judice-ninke"
    # "stucki"
    # "burkes"
    # "sierra3"
    # "sierra2"
    # "sierra-2-4a"

    method = 'atkinson'
    bw_pallete = hitherdither.palette.Palette([0x000000, 0xFFFFFF])
    img_pil = org_img.convert('RGB')
    res = hitherdither.diffusion.error_diffusion_dithering(img_pil, bw_pallete, method)

    plt.figure(figsize=(8, 8))
    plt.imshow(res, cmap="gray")
    plt.imsave('out.png', res, dpi=300, cmap="gray")
    # plt.show()
