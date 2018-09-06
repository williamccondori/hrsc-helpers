import os
import cv2
import tkinter as tk
from PIL import Image, ImageTk

class Application(tk.Frame):
    
    def __init__(self, master=None):
        
        self.path_test_file = '/home/william/data/hrsc/test.txt'
        self.path_dir_image = '/home/william/data/hrsc/images'
        self.path_dir_annotation = '/home/william/Projects/map/ground-truth'
        self.path_dir_predict = '/home/william/Projects/map/predicted'
        self.image_list = []
        self.current = 0
        self.total = 0

        super().__init__(master)

        self.parent = master
        self.parent.title('Validador')
        self.parent.geometry('842x680')
        self.parent.resizable(width=tk.FALSE, height=tk.FALSE)
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=tk.YES)

        self.pnl_control = tk.Frame(self.frame)
        self.pnl_control.grid(row=0, column=0, columnspan=2, sticky='we')
        self.btn_prev = tk.Button(
            self.pnl_control, text='Anterior', width=10, command=self.prev_image)
        self.btn_prev.pack(side=tk.LEFT, padx=5, pady=5)
        self.btn_next = tk.Button(
            self.pnl_control, text='Siguiente', width=10, command=self.next_image)
        self.btn_next.pack(side=tk.LEFT, padx=5, pady=5)


        self.pnl_image = tk.Frame(self.frame, bg='black')
        self.pnl_image.grid(row=1, column=0, sticky='we')


        self.cnv_image = tk.Canvas(self.pnl_image, relief=tk.SUNKEN, cursor='tcross', bg='black')
        self.cnv_image.config(width=820, height=480)
        #self.cnv_image.configure(scrollregion=self.cnv_image.bbox('all'))
        self.cnv_image.config(highlightthickness=0)
    
        self.sbarV = tk.Scrollbar(self.pnl_image, orient=tk.VERTICAL)
        self.sbarH = tk.Scrollbar(self.pnl_image, orient=tk.HORIZONTAL)

        self.sbarV.config(command=self.cnv_image.yview)
        self.sbarH.config(command=self.cnv_image.xview)

        self.cnv_image.config(yscrollcommand=self.sbarV.set)
        self.cnv_image.config(xscrollcommand=self.sbarH.set)


        self.sbarV.pack(side=tk.RIGHT, fill=tk.Y)
        self.sbarH.pack(side=tk.BOTTOM, fill=tk.X)
        self.cnv_image.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH,padx=5, pady=5)

        self.load_list_image()

    def prev_image(self, event=None):
        if self.current > 1:
            self.current -= 1
            self.load_image()

    def next_image(self, event=None):
        if self.current < self.total:
            self.current += 1
            self.load_image()

    def load_list_image(self):
        file_test = open(self.path_test_file, 'r')
        for line in file_test:
            line = line.rstrip('\n')
            paths = line.split('/')
            file_name = paths[6].rstrip('.jpg')
            self.image_list.append(file_name)

        self.current = 1
        self.total = len(self.image_list)

        self.load_image()

    def load_image(self):
        current = self.current - 1
        current_file_name = self.image_list[current]
        image_path = '{0}/{1}.jpg'.format(self.path_dir_image, current_file_name)
        img_opencv = cv2.imread(image_path)
        height, width, channels = img_opencv.shape


        path_annotation = '{0}/{1}.txt'.format(self.path_dir_annotation, current_file_name)
        file_annotation = open(path_annotation,'r')
        for line in file_annotation:
            line = line.rstrip('\n')
            numbers = line.split(' ')
            print(numbers)
            b_box = (int(numbers[1]), int(numbers[2]), int(numbers[3]), int(numbers[4]))
            cv2.rectangle(img_opencv, (b_box[0], b_box[1]), (b_box[2], b_box[3]), (0, 0, 255), 2)


        path_predicted = '{0}/{1}.txt'.format(self.path_dir_predict, current_file_name)
        file_predicted = open(path_predicted,'r')
        for line in file_predicted:
            line = line.rstrip('\n')
            numbers = line.split(' ')
            print(numbers)
            x_max = int(numbers[3]) + int(numbers[5])
            y_max = int(numbers[4]) + int(numbers[6])
            b_box = (int(numbers[3]), int(numbers[4]), x_max, y_max)
            cv2.rectangle(img_opencv, (b_box[0], b_box[1]), (b_box[2], b_box[3]), (0, 255, 0), 2)

        b, g, r = cv2.split(img_opencv)
        self.img = cv2.merge((r, g, b))
        self.img = Image.fromarray(self.img)

        self.cnv_image.config(scrollregion=(0,0,width,height))
        self.img_tk = ImageTk.PhotoImage(self.img)          
        self.imgtag=self.cnv_image.create_image(0,0,anchor="nw",image=self.img_tk)

root = tk.Tk()
app = Application(master=root)
app.mainloop()