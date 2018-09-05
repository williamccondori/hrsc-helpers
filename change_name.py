import os

INPUT_DIR = '/home/william/Images/perusat/hrsc/'


def main():
    i = 100000001
    for file_jpg in sorted(os.listdir(INPUT_DIR)):
        os.rename(INPUT_DIR + file_jpg, INPUT_DIR + "{}.xml".format(i))
        i = i + 1


if __name__ == '__main__':
    main()
