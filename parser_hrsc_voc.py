# Archivo para convertir el formato de HRSC a VOC.
# Creado por: William Condori Quispe - CiTeSoft.

import os
import xml.etree.ElementTree as ET
from PIL import Image

DATABASE_NAME = 'hrsc'  # Nombre de la base de datos.
BASE_DIR = '/home/william/Images/hrsc'  # Modificar.

INPUT_DIR = BASE_DIR + '/hrsc/'
OUTPUT_DIR = BASE_DIR + '/voc/'
IMAGE_DIR = BASE_DIR + '/images/'


def main():
    for file_xml in sorted(os.listdir(INPUT_DIR)):
        annotation_xml = ET.parse(INPUT_DIR + file_xml)
        output_filename = OUTPUT_DIR + file_xml

        # Image
    img = Image.open(IMAGE_DIR + '{0}.jpg'.format(file_xml.rstrip('.xml')))
    width, height = img.size

        file_output = open(output_filename, "w")
        file_output.write('<annotation>\n')
        file_output.write('	<folder>{0}</folder>\n'.format(DATABASE_NAME))
        file_output.write('	<path>{0}</path>\n'.format(output_filename))
        file_output.write('	<source>\n')
        file_output.write('		<database>{0}</database>\n'.format(DATABASE_NAME))
        file_output.write('	</source>\n')

        for elements_xml in annotation_xml.iter():
            for attribute in list(elements_xml):
                if attribute.tag == 'Img_FileName':
                    file_output.write(
                        '	<filename>{0}</filename>\n'.format(file_xml.rstrip('.xml')))
                if attribute.tag == 'Img_SizeWidth':
                    file_output.write('	<size>\n')
                    file_output.write(
                        '		<width>{0}</width>\n'.format(width))
                if attribute.tag == 'Img_SizeHeight':
                    file_output.write(
                        '		<height>{0}</height>\n'.format(height))
                if attribute.tag == 'Img_SizeDepth':
                    file_output.write(
                        '		<depth>{0}</depth>\n'.format(attribute.text))
                    file_output.write('	</size>\n')
                if attribute.tag == 'HRSC_Objects':
                    for objects in list(attribute):

                        # if len(list(attribute)) == 0:
                        file_output.write('	<object>\n')
                        file_output.write(
                            '		<name>{0}</name>\n'.format('ship'))
                        file_output.write(
                            '		<pose>{0}</pose>\n'.format('Frontal'))

                        for object_attribute in list(objects):
                            if object_attribute.tag == 'truncated':
                                file_output.write(
                                    '		<truncated>{0}</truncated>\n'.format(object_attribute.text))
                            if object_attribute.tag == 'difficult':
                                file_output.write(
                                    '		<difficult>{0}</difficult>\n'.format(object_attribute.text))
                                file_output.write(
                                    '		<occluded>{0}</occluded>\n'.format(0))
                            if object_attribute.tag == 'box_xmin':
                                file_output.write('		<bndbox>\n')
                                file_output.write(
                                    '			<xmin>{0}</xmin>\n'.format(object_attribute.text))
                            if object_attribute.tag == 'box_xmax':
                                file_output.write(
                                    '			<xmax>{0}</xmax>\n'.format(object_attribute.text))
                            if object_attribute.tag == 'box_ymin':
                                file_output.write(
                                    '			<ymin>{0}</ymin>\n'.format(object_attribute.text))
                            if object_attribute.tag == 'box_ymax':
                                file_output.write(
                                    '			<ymax>{0}</ymax>\n'.format(object_attribute.text))
                                file_output.write('		</bndbox>\n')

                        file_output.write('	</object>\n')
        file_output.write('	<segmented>{0}</segmented>\n'.format(0))
        file_output.write('</annotation>\n')
        file_output.close()


if __name__ == '__main__':
    main()
