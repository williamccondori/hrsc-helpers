import cv2
import math

def convert_voc_yolo(x_min, x_max, y_min, y_max):
    pass


def convert_yolo_voc(img_size, x, y, w, h):
    x_min = (x * img_size[0]) - ((w*img_size[0])/2)
    y_min = (y * img_size[1]) - ((h*img_size[1])/2)
    x_max = (x * img_size[0]) + ((w*img_size[0])/2)
    y_max = (y * img_size[1]) + ((h*img_size[1])/2)
    return (math.ceil(x_min), math.ceil(y_min), math.ceil(x_max), math.ceil(y_max))


def main():
    img = cv2.imread('/home/william/data/hrsc/images/100000001.jpg')
    x = 0.5
    y = 0.498007968127
    w = 0.667238421955
    h = 0.350597609562
    img_size = (1166, 753)
    b_box = convert_yolo_voc(img_size, x, y, w, h)

    cv2.rectangle(img, (b_box[0], b_box[1]), (b_box[2], b_box[3]), (0, 255, 0), 2)

    print('xmin: {0}'.format(b_box[0]))
    print('ymin: {0}'.format(b_box[1]))
    print('xmax: {0}'.format(b_box[2]))
    print('ymax: {0}'.format(b_box[3]))

    cv2.imshow("Bounding Box", img)
    cv2.waitKey(5000)


if __name__ == '__main__':
    main()
