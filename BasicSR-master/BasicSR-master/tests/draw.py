import matplotlib.pyplot as plt
import re

# 定义用于匹配迭代次数和像素损失的正则表达式
iter_pattern = r"iter: +(\d+,\d+)"
l_pix_pattern = r"l_pix: (\d\.\d+e-\d+)"

# 解析日志文件
def parse_log_file(file_path):
    iters = []
    l_pix_values = []

    with open(file_path, 'r') as file:
        for line in file:
            iter_match = re.search(iter_pattern, line)
            l_pix_match = re.search(l_pix_pattern, line)

            if iter_match and l_pix_match:
                iter_value = int(iter_match.group(1).replace(',', ''))
                l_pix_value = float(l_pix_match.group(1))

                iters.append(iter_value)
                l_pix_values.append(l_pix_value)

    return iters, l_pix_values

# 日志文件路径
file_path = r"E:\BasicSR-master\BasicSR-master\experiments\201_RCANx2_scratch_DIV2K_rand0\train_201_RCANx2_scratch_DIV2K_rand0_20240313_103645.log"

# 获取数据
iters, l_pix_values = parse_log_file(file_path)

# 找到最低点的iter及其数值
min_l_pix = min(l_pix_values)
min_iter = iters[l_pix_values.index(min_l_pix)]

# 绘图
plt.figure(figsize=(15, 7))
plt.plot(iters, l_pix_values, marker='o', color='b', linestyle='-')
plt.xlabel('Iteration')
plt.ylabel('Pixel Loss (l_pix)')
plt.title('Pixel Loss vs Iterations')

# 标记最低点
plt.scatter(min_iter, min_l_pix, color='red')
plt.text(min_iter, min_l_pix, f'({min_iter}, {min_l_pix:.5f})', color='red', verticalalignment='bottom')

plt.grid(True)
plt.show()

# 输出最低点信息
print(f"Lowest Pixel Loss: {min_l_pix:.5f} at Iteration {min_iter}")
