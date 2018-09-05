import os
import xml.etree.ElementTree as et

# Carpeta de las imagenes a analizar [Modificar].
ANNOTATION_DIR = '/home/william/Images/hrsc/hrsc/'
RESULT_DIR = '/home/william/Images/hrsc/'

def main():
    file_nobb = open(RESULT_DIR + 'images_nobb.txt', "w")
    file_wibb = open(RESULT_DIR + 'images_wibb.txt', "w")
    for file_xml in sorted(os.listdir(ANNOTATION_DIR)):
        print '-> === Archivo leido: {0} ==='.format(file_xml)
        annotation_xml = et.parse(ANNOTATION_DIR + file_xml)
        for elements_xml in annotation_xml.iter():
            for attribute in list(elements_xml):
                if attribute.tag == 'Img_FileName':
                    print '-> - Nombre de la imagen: {0}'.format(
                        attribute.text)
                if attribute.tag == 'HRSC_Objects':
                    if len(list(attribute)) == 0:
                        file_nobb.write(file_xml + '\n')
                    else:
                        file_wibb.write(file_xml + '\n')
    """
                        for objects in list(attribute):
                            for object_attribute in list(objects):
                                if object_attribute.tag == 'Object_ID':
                                    print '-> * Object: {0}'.format(
                                        object_attribute.text)
                                if object_attribute.tag == 'box_xmin':
                                    print '-> ** Bounding Box [XMIN]: {0}'.format(
                                        object_attribute.text)
                                if object_attribute.tag == 'box_ymin':
                                    print '-> ** Bounding Box [YMIN]: {0}'.format(
                                        object_attribute.text)
                                if object_attribute.tag == 'box_xmax':
                                    print '-> ** Bounding Box [XMAX]: {0}'.format(
                                        object_attribute.text)
                                if object_attribute.tag == 'box_ymax':
                                    print '-> ** Bounding Box [YMAX]: {0}'.format(
                                        object_attribute.text)
    """
    file_nobb.close()
    file_wibb.close()    


if __name__ == '__main__':
    main()
