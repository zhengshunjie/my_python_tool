import cv2
import os
import numpy as np
import random
import xml.etree.ElementTree as ET
import mytool

classes = ["head_shoulder"]
DARKNET_DATA_PATH = '/media/zsj/256ssd/dataset/head_shoulder_darknet'

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

def main():
    image_path = '/media/zsj/256ssd/dataset/head_shoulder_darknet/images'
    image_names,_,_ = mytool.type_file_name(image_path,'.jpg')
    train_txt = open('train.txt','w')

    for image_name in image_names:
        train_txt.write(image_name)
        train_txt.write('\n')
        xml_name = image_name.replace('.jpg','.xml')
        image_txt = open(DARKNET_DATA_PATH + '/labels/' + image_name.split('/')[-1].replace('.jpg', '.txt'), 'w')
        if not os.path.exists(xml_name):
            print("not exists",xml_name)
            image_txt.close()
            continue
        xml_tree = ET.parse(xml_name)
        xml_root = xml_tree.getroot()
        size = xml_root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for obj in xml_root.iter('object'):
            cls = obj.find('name').text
            if cls not in classes:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            image_txt.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
            # print(bb)
        image_txt.close()
    train_txt.close()
#flip image and create new xml
def image_to_flip():
    image_path = '/media/zsj/256ssd/dataset/head_shoulder_darknet/images'
    image_names,_,_ = mytool.type_file_name(image_path,'.jpg')
    for image_name in image_names:
        image = cv2.imread(image_name)
        image = cv2.flip(image, 0)
        cv2.imwrite(image_name.replace('.','_flip.'),image)
        # cv2.imshow('1', image)
        # cv2.waitKey()

        #create xml
        xml_name = image_name.replace('.jpg', '.xml')
        if not os.path.exists(xml_name):
            print("not exists", xml_name)
            continue
        xml_tree = ET.parse(xml_name)
        xml_root = xml_tree.getroot()
        size = xml_root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in xml_root.iter('object'):
            xmlbox = obj.find('bndbox')
            #xmin = xmlbox.find('xmin')
            ymin = xmlbox.find('ymin')
            #xmax = xmlbox.find('xmax')
            ymax = xmlbox.find('ymax')
            tmp_ymin = int(ymin.text)
            tmp_ymax = int(ymax.text)
            ymin.text = str(h - tmp_ymax)
            ymax.text = str(h - tmp_ymin)
        xml_tree.write(xml_name.replace('.','_flip.'))

#resize image and create new xml
def image_resize():
    image_path = '/media/zsj/256ssd/dataset/head_shoulder_darknet/images'
    image_names, _, _ = mytool.type_file_name(image_path, '.jpg')
    for image_name in image_names:
        image = cv2.imread(image_name)
        if image is None:
            print("not exists", image_name)
            continue
        src_w = int(image.shape[1])
        src_h = int(image.shape[0])
        w = int(image.shape[1]/2)
        h = int(image.shape[0]/2)

        image = cv2.resize(image,(w,h))
        ground_image = np.zeros((src_h,src_w,3),dtype=np.uint8)
        start_x = random.randint(0,w)
        start_y = random.randint(0,h)
        ground_image[start_y:int(start_y+h),start_x:int(start_x+w),:] = image
        cv2.imwrite(image_name.replace('.', '_resize.'), ground_image)
        # cv2.imshow('1', ground_image)
        # cv2.waitKey()

        # create xml
        xml_name = image_name.replace('.jpg', '.xml')
        if not os.path.exists(xml_name):
            print("not exists", xml_name)
            continue
        xml_tree = ET.parse(xml_name)
        xml_root = xml_tree.getroot()
        size = xml_root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in xml_root.iter('object'):
            xmlbox = obj.find('bndbox')
            xmin = xmlbox.find('xmin')
            ymin = xmlbox.find('ymin')
            xmax = xmlbox.find('xmax')
            ymax = xmlbox.find('ymax')

            xmin.text = str(int(int(xmin.text)/2 + start_x))
            xmax.text = str(int(int(xmax.text)/2 + start_x))
            ymin.text = str(int(int(ymin.text)/2 + start_y))
            ymax.text = str(int(int(ymax.text)/2 + start_y))
        #     cv2.rectangle(ground_image, (int(xmin.text),int(ymin.text)),(int(xmax.text),int(ymax.text)),(255,0,0))
        # cv2.imshow('1', ground_image)
        # cv2.waitKey()
        xml_tree.write(xml_name.replace('.', '_resize.'))
if __name__ == '__main__':
    main()