import os
import shutil

def split_voc(source_dir,voc_root):
    image_dir = os.path.join(source_dir,'images')
    mask_dir = os.path.join(source_dir, 'masks')
    jpeg_dir = os.path.join(voc_root,'JPEGImages')
    mask_voc_dir = os.path.join(voc_root,'SegmentationClass')
    split_dir = os.path.join(voc_root,'ImagSets/Segmentation')

    os.makedirs(jpeg_dir,exist_ok=True)
    os.makedirs(mask_voc_dir, exist_ok=True)
    os.makedirs(split_dir, exist_ok=True)

    splits = ['train','val','test']
    for split in splits:
        cur_img_dir = os.path.join(image_dir,split)
        cur_mask_dir = os.path.join(mask_dir,split)

        name_list = []

        for fname in os.listdir(cur_mask_dir):
            if not fname.endswith('.png'):
                continue

            base = os.path.splitext(fname)[0]
            name_list.append(base)

            scr_img = os.path.join(cur_img_dir,base+'.jpg')
            dst_img = os.path.join(jpeg_dir,base+'.jpg')

            if os.path.exists(scr_img) and not os.path.exists(dst_img):
                shutil.copyfile(scr_img,dst_img)

            scr_mask = os.path.join(cur_mask_dir,fname)
            dst_mask = os.path.join(cur_mask_dir,fname)

            if os.path.exists(scr_mask) and not os.path.exists(dst_mask):
                shutil.copyfile(scr_mask,dst_mask)

        txt_path = os.path.join(split_dir,split + '.txt')
        with open(txt_path,'w') as f:
            f.write('\n'.join(sorted(name_list)))

        print(f'{source_dir}写入{split}.txt,共{len(name_list)}个样本')

split_voc('./Recto','./data_recto/VoCdevkit/VOC2012')
