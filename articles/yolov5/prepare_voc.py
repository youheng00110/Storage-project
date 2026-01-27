import xml.etree.ElementTree as ET
import os
from os import getcwd
import yaml
import subprocess

sets = ['train', 'val']
classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# 数据集的绝对路径
abs_path = r"D:\Storage project\articles\deep-learning-for-image-processing\data_set\VOCdevkit\VOC2012"

# Create Junction if not exists
images_path = os.path.join(abs_path, 'images')
jpeg_images_path = os.path.join(abs_path, 'JPEGImages')

if not os.path.exists(images_path):
    print(f"Creating junction from {jpeg_images_path} to {images_path}")
    try:
        subprocess.check_call(['cmd', '/c', 'mklink', '/J', images_path, jpeg_images_path])
    except subprocess.CalledProcessError as e:
        print(f"Failed to create junction: {e}")
        # Fallback: rename? No, copy? too slow. 
        # let's assume it works or user needs to handle it.
        pass

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    in_file = open(os.path.join(abs_path, 'Annotations/%s.xml'%(image_id)), encoding='utf-8')
    out_file = open(os.path.join(abs_path, 'labels/%s.txt'%(image_id)), 'w', encoding='utf-8')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    in_file.close()
    out_file.close()

if not os.path.exists(os.path.join(abs_path, 'labels')):
    os.makedirs(os.path.join(abs_path, 'labels'))

for image_set in sets:
    image_ids = open(os.path.join(abs_path, 'ImageSets/Main/%s.txt'%(image_set))).read().strip().split()
    list_file = open('data_%s.txt'%(image_set), 'w')
    for image_id in image_ids:
        list_file.write(os.path.join(abs_path, 'images/%s.jpg\n'%(image_id)))
        convert_annotation(image_id)
    list_file.close()

# Create yaml file
data = {
    'train': os.path.abspath('data_train.txt'),
    'val': os.path.abspath('data_val.txt'),
    'nc': 20,
    'names': classes
}

with open('my_voc.yaml', 'w') as f:
    yaml.dump(data, f)

print("Data preparation done. 'my_voc.yaml' created.")
