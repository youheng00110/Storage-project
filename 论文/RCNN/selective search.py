import os
import argparse

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import selectivesearch
from skimage import io as skio, color, util


def run_selective_search(
	image_path: str,
	scale: int = 500,
	sigma: float = 0.9,
	min_size: int = 10,
	top_n: int = 100,
):
	"""在一张图片上运行 Selective Search 并可视化候选框。

	参数
	------
	image_path : 图片路径
	scale      : 控制超像素分割的尺度（越大区域越大，框越少）
	sigma      : 高斯滤波参数
	min_size   : 最小区域大小（像素）
	top_n      : 可视化前 top_n 个候选框
	"""

	if not os.path.exists(image_path):
		raise FileNotFoundError(f"Image not found: {image_path}")

	image = skio.imread(image_path)
	# 确保是三通道 RGB 图像（selectivesearch 要求 shape[2] == 3）
	if image.ndim == 2:
		# 灰度图：复制三份作为伪 RGB
		image = color.gray2rgb(image)
	elif image.ndim == 3 and image.shape[2] == 4:
		# RGBA 图：丢掉 alpha 通道，只取前 3 个通道
		image = image[:, :, :3]
	elif image.ndim == 3 and image.shape[2] != 3:
		raise ValueError(f"Unsupported channel number: {image.shape}")

	# 将图像转换为整数类型（uint8），避免 skimage 的 LBP 警告
	if image.dtype != np.uint8:
		image = util.img_as_ubyte(image)

	print("[INFO] 正在对图像进行 Selective Search 处理，请稍候...")
	print(f"[INFO] 图像路径: {image_path}, 参数: scale={scale}, sigma={sigma}, min_size={min_size}")

	# 运行 selective search
	img_lbl, regions = selectivesearch.selective_search(
		image, scale=scale, sigma=sigma, min_size=min_size
	)

	# 过滤候选框：去重、过滤太小区域或奇异比例
	candidates = set()
	for r in regions:
		# rect: (x, y, w, h)
		rect = r["rect"]
		size = r["size"]

		# 去重
		if rect in candidates:
			continue

		# 过滤很小的区域
		if size < 2000:
			continue

		x, y, w, h = rect
		# 过滤退化框
		if w == 0 or h == 0:
			continue

		# 过滤极端长宽比的框
		if w / h > 3 or h / w > 3:
			continue

		candidates.add(rect)

	print(f"Total regions from selective search: {len(regions)}")
	print(f"Candidates after filtering: {len(candidates)}")
	print("[INFO] Selective Search 处理完成，开始可视化候选框...")

	# 可视化前 top_n 个候选框
	fig, ax = plt.subplots(1, figsize=(8, 8))
	ax.imshow(image)
	ax.set_axis_off()

	for i, (x, y, w, h) in enumerate(list(candidates)[:top_n]):
		rect = mpatches.Rectangle(
			(x, y), w, h, fill=False, edgecolor="red", linewidth=1
		)
		ax.add_patch(rect)

	plt.tight_layout()
	plt.show()


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Run Selective Search on an image")
	parser.add_argument(
		"-i",
		"--image",
		type=str,
		required=False,
		help="路径到输入图片 (e.g. D:/images/dog.jpg)，留空则运行时输入",
	)
	parser.add_argument("--scale", type=int, default=500, help="Selective Search scale")
	parser.add_argument("--sigma", type=float, default=0.9, help="Gaussian sigma")
	parser.add_argument("--min-size", type=int, default=10, help="Minimum region size")
	parser.add_argument("--top", type=int, default=100, help="Number of boxes to show")
	return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	# 如果命令行没有给出图片路径，则在运行时通过输入获取
	image_path = args.image or input("请输入图片路径（例如 D:/images/dog.jpg）：")
	run_selective_search(
		image_path=image_path,
		scale=args.scale,
		sigma=args.sigma,
		min_size=args.min_size,
		top_n=args.top,
	)

