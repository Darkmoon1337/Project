import cv2
import os
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt

# 设置文件夹路径
folder1 = r'D:\dataset\sr\new\train\Parasitized'
folder2 = r'D:\dataset\OR\train\parasitized'

# 获取文件夹中的文件路径列表
file_paths1 = [os.path.join(folder1, f) for f in sorted(os.listdir(folder1))]
file_paths2 = [os.path.join(folder2, f) for f in sorted(os.listdir(folder2))]

# 初始化指针
ptr1, ptr2 = 0, 0

# 初始化列表用于存储 SSIM 和 PSNR 值
ssim_values = []
psnr_values = []

# 匹配文件并计算 SSIM 和 PSNR 值
while ptr1 < len(file_paths1) and ptr2 < len(file_paths2):
    file1 = file_paths1[ptr1]
    file2 = file_paths2[ptr2]

    # 比较文件名并移动指针
    filename1 = os.path.basename(file1).replace('_RCAN_BIX4-official', '')
    filename2 = os.path.basename(file2)
    if filename1 < filename2:
        ptr1 += 1
    elif filename1 > filename2:
        ptr2 += 1
    else:
        # 读取图像
        img1 = cv2.imread(file1)
        img2 = cv2.imread(file2)

        # 将图像调整到相同的尺寸
        height, width = min(img1.shape[:2]), min(img1.shape[:2])
        img1 = cv2.resize(img1, (width, height))
        img2 = cv2.resize(img2, (width, height))

        # 计算 SSIM 值
        win_size = min(img1.shape[:2])  # 根据图像尺寸动态设置窗口大小
        if win_size % 2 == 0:
            win_size -= 1  # 保证窗口大小为奇数
        ssim_value = ssim(img1, img2, win_size=win_size, multichannel=True, channel_axis=2, data_range=255)

        # 计算 PSNR 值
        psnr_value = cv2.PSNR(img1, img2)

        ssim_values.append(ssim_value)
        psnr_values.append(psnr_value)

        print(f"File {filename1} and {filename2}: SSIM = {ssim_value:.4f}, PSNR = {psnr_value:.2f}")

        # 移动指针
        ptr1 += 1
        ptr2 += 1

# 检查是否有匹配的文件对
if not ssim_values:
    print("No matching file pairs found.")
else:
    # 绘制 SSIM 与 PSNR 的散点图
    plt.figure(figsize=(8, 6))
    plt.scatter(psnr_values, ssim_values)
    plt.title('SSIM vs PSNR')
    plt.xlabel('PSNR')
    plt.ylabel('SSIM')
    plt.show()

    # 打印 SSIM 最大值、最小值和平均值
    ssim_max = max(ssim_values)
    ssim_min = min(ssim_values)
    ssim_avg = sum(ssim_values) / len(ssim_values)
    print(f"\nSSIM: Max = {ssim_max:.4f}, Min = {ssim_min:.4f}, Avg = {ssim_avg:.4f}")

    # 打印 PSNR 最大值、最小值和平均值
    psnr_max = max(psnr_values)
    psnr_min = min(psnr_values)
    psnr_avg = sum(psnr_values) / len(psnr_values)
    print(f"\nPSNR: Max = {psnr_max:.2f}, Min = {psnr_min:.2f}, Avg = {psnr_avg:.2f}")