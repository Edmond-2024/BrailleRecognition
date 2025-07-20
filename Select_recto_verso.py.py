import os
import shutil

def organize_files(root_dir):
    # 首先，为每一类图片和标注创建两个一级子文件夹 Recto 和 Verso
    for mode in ['Recto', 'Verso']:
        # 1、分别创建 images 和 annotations 两个二级子文件夹
        os.makedirs(os.path.join(mode,'images'),exist_ok = True)
        os.makedirs(os.path.join(mode,'annotations'), exist_ok = True)

    # 2、遍历所有文件（包括子文件夹里的）
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            # 3、如果不是 .jpg 或 .txt 文件就跳过
            if not (file.endswith('.jpg') or file.endswith('.txt')):
                continue

            # 4、把文件名变成小写，避免大小写影响判断
            lower_file = file.lower()

            # 5、判断是 Recto 还是 Verso 类型的文件,target_base为定义的一级子文件夹名
            if 'recto' in lower_file:
                target_base = 'Recto'
            elif 'verso' in lower_file:
                target_base = 'Verso'
            else:
                continue  # 如果不包含 recto 或 verso 就跳过

            # 6、决定是放在 images 文件夹还是 annotations 文件夹，target_sub为定义的二级子文件夹名
            if file.lower().endswith('.jpg'):
                target_sub = 'images'
            elif file.lower().endswith('.txt'):
                target_sub = 'annotations'
            else:
                continue  # 如果不包含 recto 或 verso 就跳过

            # 7、源文件路径，准确到文件名
            src_path = os.path.join(subdir,file)
            # 8、目标路径
            dst_path = os.path.join(target_base,target_sub,file)

            # 9、复制文件到目标位置
            shutil.copyfile(src_path,dst_path)
            print(f'Copied {src_path} -> {dst_path}')  # 显示复制的过程
# 删除空的标注文件和它对应的图像文件
    for mode in ['Recto', 'Verso']:
        ann_dir = os.path.join(mode, 'annotations')  # 标注路径
        img_dir = os.path.join(mode, 'images')       # 图像路径

        for txt_file in os.listdir(ann_dir):
            if not txt_file.endswith('.txt'):
                continue  # 只处理 .txt 文件

            txt_path = os.path.join(ann_dir, txt_file)

            # 读取标注文件内容
            with open(txt_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()  # 去除空格和换行

            if not content:
                # 如果内容为空就删除标注文件
                os.remove(txt_path)
                print(f"Deleted empty annotation: {txt_path}")

                # 再删除对应的图像文件
                jpg_name = txt_file.replace('.txt', '.jpg')
                jpg_path = os.path.join(img_dir, jpg_name)
                if os.path.exists(jpg_path):
                    os.remove(jpg_path)
                    print(f"Deleted corresponding image: {jpg_path}")


# 15、执行程序，把 "DSBI-master/data" 目录里的文件整理分类
organize_files("DSBI-master/data")
