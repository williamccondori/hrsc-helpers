import tkinter as tk
import os
import glob
import cv2
import math
from PIL import Image, ImageTk


class Application(tk.Frame):

    def __init__(self, master=None):

        #self.imageDir = ''
        self.image_list = []
        #self.egDir = ''
        #self.egList = []
        #self.outDir = ''
        self.current = 0
        self.total = 0
        #self.category = 0
        #self.imagename = ''
        #self.labelfilename = ''
        self.image_tk = None

        super().__init__(master)

        self.parent = master
        self.parent.title('William Tools')
        self.parent.geometry('1200x930')
        self.parent.resizable(width=tk.FALSE, height=tk.FALSE)
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=tk.YES)

        # Control panel

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
        self.cnv_image.config(width=1175, height=680)
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


  

        self.pnl_dir = tk.Frame(self.frame)
        self.pnl_dir.grid(row=2, column=0, sticky='we')

        self.lbl_image_dir = tk.Label(self.pnl_dir, text="Ruta de la carpeta de imágenes:")
        self.lbl_image_dir.pack(side=tk.LEFT, padx=5, pady=5)

        self.ety_path = tk.Entry(self.pnl_dir, width=60)
        
        self.ety_path.insert(tk.END, '/home/william/Descargas/perusat/images/')
        self.ety_path.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.btn_load = tk.Button(self.pnl_dir, text="Cargar", command=self.load_dir)
        self.btn_load.pack(side=tk.LEFT, padx=5, pady=5)

        self.pnl_log = tk.Frame(self.frame, bg="#f5f5f5")
        self.pnl_log.grid(row=3, column=0, sticky='we')

        self.txt_log = tk.Text(self.pnl_log)
        self.txt_log.config(height=3)

        self.txt_log.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH,padx=5, pady=5)
        self.s_start = tk.Scrollbar(self.pnl_log)
        self.s_start.pack(side=tk.RIGHT, fill=tk.Y)
        self.s_start.config(command=self.txt_log.yview)
        self.txt_log.config(yscrollcommand=self.s_start.set)

        self.txt_log.insert('end', 'WILLIAM TOOLS VERSIÓN 0.0.1\n')
        self.txt_log.insert('end', '===========================\n')
        self.txt_log.configure(state=tk.DISABLED)
        self.txt_log.see(tk.END)

    def load_dir(self):
        self.image_dir = self.ety_path.get()
        self.image_list = sorted(glob.glob(os.path.join(self.image_dir, '*.jpg')))
        
        if len(self.image_list) == 0:
            self.print_log('No se encontraron imágenes en el directorio')
            return

        self.current = 1
        self.total = len(self.image_list)

        self.print_log('Se encontraron {0} imágenes'.format(len(self.image_list)))

        self.load_image()

    def prev_image(self, event=None):
        if self.current > 1:
            self.current -= 1
            self.load_image()

    def next_image(self, event=None):
        if self.current < self.total:
            self.current += 1
            self.load_image()

    def convert_yolo_voc(self, img_size, x, y, w, h):
        x_min = (x * img_size[0]) - ((w*img_size[0])/2)
        y_min = (y * img_size[1]) - ((h*img_size[1])/2)
        x_max = (x * img_size[0]) + ((w*img_size[0])/2)
        y_max = (y * img_size[1]) + ((h*img_size[1])/2)
        return (math.ceil(x_min), math.ceil(y_min), math.ceil(x_max), math.ceil(y_max))

    def load_image(self):
        current = self.current - 1
        image_path = self.image_list[current]

        img_opencv = cv2.imread(image_path)
        



        height, width, channels = img_opencv.shape

        annotation_path = image_path.rstrip('jpg') + 'txt'
        file_txt = open(annotation_path, 'r')

        self.print_log(image_path)
        self.print_log(annotation_path)

        self.print_log(width)
        self.print_log(height)

        for line in file_txt:
            line = line.rstrip('\n')
            bbox = line.split(' ')
            x = float(bbox[1])
            y = float(bbox[2])
            w = float(bbox[3])
            h = float(bbox[4])
            img_size = (width, height)
            b_box = self.convert_yolo_voc(img_size, x, y, w, h)
            cv2.rectangle(img_opencv, (b_box[0], b_box[1]), (b_box[2], b_box[3]), (0, 255, 0), 2)

        b, g, r = cv2.split(img_opencv)
        self.img = cv2.merge((r, g, b))

        self.img = Image.fromarray(self.img)

        self.cnv_image.config(scrollregion=(0,0,width,height))
        self.img_tk = ImageTk.PhotoImage(self.img)          
        self.imgtag=self.cnv_image.create_image(0,0,anchor="nw",image=self.img_tk)

    def print_log(self, message):
        self.txt_log.configure(state=tk.NORMAL)
        self.txt_log.insert("end", "\n> " + str(message).upper())
        self.txt_log.configure(state=tk.DISABLED)
        self.txt_log.see(tk.END)

root = tk.Tk()
app = Application(master=root)
app.mainloop()