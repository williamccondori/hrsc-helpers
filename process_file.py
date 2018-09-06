import glob
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = current_dir + '/perusat'

def isLineEmpty(line):
    return len(line.strip()) == 0

def main():
    # Directory where the data will reside, relative to 'darknet.exe'
    path_data = '/home/william/data/hrsc/dataset/'

    # Percentage of images to be used for the test set
    percentage_test = 10

    # Create and/or truncate train.txt and test.txt
    file_train = open('train.txt', 'w')
    file_test = open('test.txt', 'w')

    print(current_dir)
    print(path_data)

    # Populate train.txt and test.txt
    counter = 1
    index_test = round(100 / percentage_test)

    file_input = open('/home/william/Images/hrsc/images_wibb.txt', 'r')
 
    for line in file_input:
        if not isLineEmpty(line):
            #print line,
            # for pathAndFilename in glob.iglob(os.path.join(path_data, "*.jpg")):
            #title, ext = os.path.splitext(os.path.basename(pathAndFilename))
            title = line.rstrip('.xml\n')
            print ('Linea: {0}'.format(title))
            
            # print(title)
            if counter == index_test:
                counter = 1
                file_test.write(path_data + title + '.jpg' + "\n")
            else:
                file_train.write(path_data + title + '.jpg' + "\n")
                counter = counter + 1


if __name__ == '__main__':
    main()
