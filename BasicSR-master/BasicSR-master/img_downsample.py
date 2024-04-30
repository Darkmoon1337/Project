import cv2
import os

def make_even(number):
    return number if number % 2 == 0 else number + 1

def ensure_minimum_size(h, w, min_size=48):
    # 确保即使在缩放后，低分辨率图像尺寸也满足最小尺寸要求
    h = max(min_size, h)
    w = max(min_size, w)
    # 使尺寸成为偶数
    return make_even(h), make_even(w)

img_root = r"E:\SRClass\archive\cell_images\Uninfected"
hq_root = r"E:\SRClass\archive\cell_images2\\Uninfected_HR"
lq_root = r"E:\SRClass\archive\cell_images2\\Uninfected_LRx2"

os.makedirs(hq_root, exist_ok=True)
os.makedirs(lq_root, exist_ok=True)

img_list = os.listdir(img_root)

for img_name in img_list:
    print(img_name)
    img = cv2.imread(os.path.join(img_root, img_name))
    if img is None:  # 确保图片被正确读取
        continue

    h, w, _ = img.shape
    # 调整原始图像尺寸以确保即使在缩放后，低分辨率图像也满足最小尺寸要求
    hr_h, hr_w = ensure_minimum_size(h * 2, w * 2)
    lr_h, lr_w = int(hr_h / 2), int(hr_w / 2)

    print(h, w, hr_h, hr_w)

    img_hq = cv2.resize(img, (hr_w, hr_h))  # 调整到高分辨率大小
    img_lq = cv2.resize(img_hq, (lr_w, lr_h))  # 从高分辨率调整到低分辨率

    cv2.imwrite(os.path.join(hq_root, img_name), img_hq)
    cv2.imwrite(os.path.join(lq_root, img_name), img_lq)
