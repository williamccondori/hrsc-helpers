# Archivo para convertir el formato de de VOC a YOLO V2.
# Creado por: pjreddie.
# Modificado por: William Condori Quispe - CiTeSoft.
# Se modifica el archivo para omitir los anios en el Dataset VOC.

import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

# sets = [('2012', 'train'), ('2012', 'val'),
#        ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]
# classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
#           "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

CLASSES = ['ship']  # Clases disponibles en el Dataset.
# Directorio de entrada (Xml).
INPUT_DIR = '/home/william/Images/hrsc/voc/'
# Directorio de salida (Debe existir).
OUTPUT_DIR = '/home/william/Images/hrsc/yolo/'


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x, y, w, h)


def convert_annotation(image_id):
    in_file = open(INPUT_DIR + '/%s.xml' % (image_id))
    out_file = open(OUTPUT_DIR + '/%s.txt' % (image_id), 'w')

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        print obj.find('name').text
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in CLASSES or int(difficult) == 1:
            continue
        cls_id = CLASSES.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(
            xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " +
                       " ".join([str(a) for a in bb]) + '\n')
    out_file.close()
	

def main():
    for file_xml in sorted(os.listdir(INPUT_DIR)):
        image_id = str(file_xml).rstrip('.xml')
        print image_id
        convert_annotation(image_id)


if __name__ == '__main__':
    main()
