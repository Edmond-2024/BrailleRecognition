import os  # 用于路径操作
import shutil  # 用于复制文件
import random  # 用于打乱顺序
from tqdm import tqdm  # 用于显示进度条

def split_img_mask_dataset_new_structure(base_dir, seed=42):
    # 固定随机种子，确保每次划分结果一样
    random.seed(seed)

    # 1、图像和mask标签的路径（如 base_dir/images 和 base_dir/masks）
    image_dir = os.path.join(base_dir,'images')
    mask_dir = os.path.join(base_dir,'masks')

    # 2、获取所有jpg图像文件名
    img_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
    # 3、排序使得每次打乱前文件顺序一致
    img_files.sort()
    # 4、随机打乱图像顺序
    random.shuffle(img_files)

    # 计算总数，划分每一组的数量（7:2:1）
    n = len(img_files)
    # 5、训练集数量
    n_train = int(n*0.7)
    # 6、验证集数量
    n_val = int(n*0.2)
    # 7、剩下的作为测试集
    n_test = n-n_val-n_train
    # 8、分配图像文件名到每一组（train，val，test）(使用字典+数组）
    splits = {'train': img_files[:n_train],
              'val': img_files[n_train:n_val+n_train],
              'test': img_files[n_val+n_train:]}

    # 9、for循环遍历字典中每一组

    for split, files in splits.items():
        # 10、分别创建对应的图像和mask文件夹下train，val，test子文件夹
        split_img_dir = os.path.join(image_dir, split)
        split_mask_dir = os.path.join(mask_dir, split)
        os.makedirs(os.path.join(image_dir, split), exist_ok=True)
        os.makedirs(split_mask_dir, exist_ok=True)

        # 11、复制每张图像和其对应的mask到对应的组中，比如属于训练集的存到image/train中
        # (思考：1、如果某张图像没有对应的mask怎么办 2、我怎样使用进度条在终端中可视化复制进度）
        for img_file in tqdm(files, desc=f"Copying {split} set for {base_dir}"):
            mask_file = os.path.splitext(img_file)[0] + ".png"
            shutil.copyfile(os.path.join(image_dir, img_file) , os.path.join(split_img_dir,img_file))

            mask_src_path = os.path.join(mask_dir, mask_file)
            mask_dst_path = os.path.join(split_mask_dir, mask_file)

            if os.path.exists(mask_src_path):
                shutil.copyfile(mask_src_path, mask_dst_path)
            else:
                print(f" 缺失ground truth文件: {mask_src_path}")

        # 打印划分完成提示
        print(f" {base_dir} 图像+ground truth数据划分完成，train:{n_train}, val:{n_val}, test:{n_test}")








    # 12、打印划分完成提示,最好包含数据集信息（比如处理的是凹凸，完成数量等等）


# 13、对两个子数据集（凹面、凸面）分别划分
split_img_mask_dataset_new_structure('./Verso')
