import os

file_name = ''

file = open('result.txt','r')
for line in file:
    line = line.rstrip('\n')
    if line.find('Enter Image Path: /') == 0:
        text = line.split(' ')
        text = text[3].split('/')
        text = text[6].split('.')
        file_name = str(text[0])
        print('Se creo el archivo {0}.txt'.format(file_name))
        new_file = open('{0}.txt'.format(file_name), 'w')
        new_file.close()
    elif line.find('ship') == 0:
        new_file = open('{0}.txt'.format(file_name), 'a')
        new_file.write(line + '\n')