import os  # 导入操作系统模块，用于文件和路径操作
from tkinter import image_names

from PIL import Image, ImageDraw  # 从PIL库导入图像处理模块
from tqdm import tqdm  # 用于显示进度条
from data_box_select import parse_dsbi_annotation  # 自定义函数，用于解析标注文件

def generate_semantic_masks(img_dir, txt_dir, output_mask_dir, padding=6):
    """
    功能：根据图片和对应的标注文件，生成语义分割用的灰度掩码图
    参数：
        img_dir：图片所在文件夹路径
        txt_dir：标注文件所在文件夹路径
        output_mask_dir：输出掩码图的保存路径
        padding：对标注框进行一定像素的扩张，默认为6
    """
    # 1、如果输出掩码图的文件夹不存在，就创建它
    os.makedirs(output_mask_dir,exist_ok = True)

    # 2、读取所有.jpg图片文件名
    img_files = [f for f in os.listdir(img_dir) if f.endswith ('.jpg')]

    skipped_images = []  # 用于记录被跳过的图像文件名

    # tqdm用于显示进度条（可视化进度）
    for img_name in tqdm(img_files, desc="Generating masks"):
        # 3、获取对应的标注文件名，然后将.jpg替换为.txt
        txt_name = os.path.splitext(img_name)[0] + '.txt'


        # 4、构造完整路径
        img_path = os.path.join(img_dir,img_name)
        txt_path = os.path.join(txt_dir,txt_name)

        # 如果没有对应的.txt标注文件，就跳过
        if not os.path.exists(txt_path):
            continue

        # 5、打开图像并获取其宽高
        img = Image.open(img_path)
        width,height=img.size

        # 6、调用自定义函数parse_dsbi_annotation，解析txt_path路径下图片对应的标注信息
        boxes, labels = parse_dsbi_annotation(txt_path)

        valid_found = False  # 是否找到了有效标注的标记（默认为否）

        # 7、创建一个新的灰度图像，大小与原图一致，初始全黑（值为0）
        mask = Image.new('L',(width,height),0)

        # 8、创建一个绘图对象，可以在mask图上画矩形
        draw = ImageDraw.Draw(mask)

        # for循环遍历每一个标注框和对应的类别标签,如果类别编号不是合法范围（例如 1~63），跳过该标注
        for box, label in zip(boxes, labels):
            if not (1 <= label <= 63):
                continue

            # 将标注框中的坐标转换为整数
            xmin, ymin, xmax, ymax = map(int, box)

            # 对边界框做扩张处理，同时确保不越界
            xmin = max(0, xmin - padding)
            ymin = max(0, ymin - padding)
            xmax = min(width, xmax + padding)
            ymax = min(height, ymax + padding)

            # 如果扩张后仍然是有效矩形（非负宽高）
            if xmax > xmin and ymax > ymin:
                # 9、在掩码图中绘制这个框，灰度值设为label
                draw.rectangle([xmin,ymin,xmax,ymax],fill=label)
                # 10、找到了有效标注
                valid_found = True  # 找到了有效标注

        # 如果找到了有效的标注，就保存这张mask图
        if valid_found:

            # 11、将图片名从.jpg换成.png作为掩码图的文件名
            mask_name = os.path.splitext(img_name)[0] + '.png'

            # 12、构造完整路径
            mask_path = os.path.join(output_mask_dir,mask_name)

            # 保存掩码图
            mask.save(mask_path)
        else:
            # 如果没有有效标注，则记录这张图片为“跳过”
            skipped_images.append(img_name)

        # 所有mask图处理完后，输出提示信息
    print(f" 所有ground truth已保存至 {output_mask_dir}")

    # 输出哪些图像因无有效标注而被跳过
    if skipped_images:
        print(f" 以下图像无有效标注，被跳过（无合法类别 bbox）:")
        for name in skipped_images:
            print(f" - {name}")

# 15、调用函数，处理Recto和Verso两组数据
generate_semantic_masks('./Recto/images','./Recto/anotations','./Recto/masks')
generate_semantic_masks("./Verso/images", "./Verso/annotations", "./Verso/masks")