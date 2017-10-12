
from random import shuffle
from array import *
from PIL import Image
import gzip
import os

class image_mnist(object):
    """description of class"""


    def __init__(self, main_folder, output_folder, train_folder = "training-images", 
                 test_folder = "test-images"):
        self.main_folder = main_folder
        self.names = [[ main_folder + train_folder,'train'], [ main_folder + test_folder,'t10k']]
        self.data_image = array('B')
        self.data_label = array('B')
        self.FileList = []
        self.output_folder = output_folder

    # Get all the images in the folder
    def get_all_images(self, name):
        for dirname in os.listdir(name[0])[1:]: # [1:] Excludes .DS_Store from Mac OS
            path = os.path.join(name[0],dirname)
            for filename in os.listdir(path):
                if filename.endswith(".png"):
                    self.FileList.append(os.path.join(name[0],dirname,filename))

    def make_square(self, im, min_size, fill_color=(0, 0, 0, 0)):
        x, y = im.size
        size = max(min_size, x, y)
        new_im = Image.new('RGBA', (size, size), fill_color)
        new_im.paste(im, ((size - x) // 2, (size - y) // 2))
        return new_im

    # Gets all the directory names as the classification label 
    # and the file as the image
    def extract_images_and_labels(self, toSquare, squareSize):
        for filename in self.FileList:
            print("Extracting " + filename)
            splitfilename = filename.split(os.sep)
            label = int(splitfilename[len(splitfilename) - 2])
            Im = Image.open(filename)
            if toSquare :
                rgba_im = self.make_square(Im, min_size = squareSize)
            else: rgba_im = Im.convert('RGBA')
            width, height = rgba_im.size
            for x in range(0,width):
                for y in range(0,height):
                    r, g, b, a = rgba_im.getpixel((x, y))
                    # For a Grayscale image RGB are all the same
                    #self.data_image.append(r)
                    self.data_image.append(g)
                    #self.data_image.append(b)

            self.data_label.append(label) # labels start (one unsigned byte each)

        return width, height


    def header_label(self):
        hexval = "{0:#0{1}x}".format(len(self.FileList),10) # number of files in HEX

        # header for label array
        header = array('B')

        header.extend([0,0,8,1])
        header.append(int('0x'+hexval[2:][:2],16))
        header.append(int('0x'+hexval[4:][:2],16))
        header.append(int('0x'+hexval[6:][:2],16))
        header.append(int('0x'+hexval[8:][:2],16))

        return header

    def header_image(self, width, height, header):
        hexval = "{0:#0{1}x}".format(width,10) # width in HEX

        header.append(int('0x'+hexval[2:][:2],16))
        header.append(int('0x'+hexval[4:][:2],16))
        header.append(int('0x'+hexval[6:][:2],16))
        header.append(int('0x'+hexval[8:][:2],16))
        hexval = "{0:#0{1}x}".format(height,10) # height in HEX
        header.append(int('0x'+hexval[2:][:2],16))
        header.append(int('0x'+hexval[4:][:2],16))
        header.append(int('0x'+hexval[6:][:2],16))
        header.append(int('0x'+hexval[8:][:2],16))

        header[3] = 3 # Changing MSB for image data (0x00000803)

        return header

    def save_mnist_data(self, name):
        output_file = open(self.main_folder + self.output_folder + name[1] + '-images-idx3-ubyte', 'wb')
        self.data_image.tofile(output_file)
        output_file.close()

        output_file = open(self.main_folder + self.output_folder + name[1] + '-labels-idx1-ubyte', 'wb')
        self.data_label.tofile(output_file)
        output_file.close()
        print("MNIST data saved for " + name[1])

    def make_sure_path_exists(self, path):
        try:
            os.makedirs(path)
        except OSError as exception:
            print("Output folder is " + self.main_folder)

    def GzipMnistFiles(self):
        for name in self.names:
            f_names = [self.main_folder + self.output_folder + name[1] + '-images-idx3-ubyte', 
                       self.main_folder + self.output_folder + name[1] + '-labels-idx1-ubyte'];

            for f_name in f_names:   
                f_in = open(f_name, "rb")
                f_out = gzip.open(f_name + '.gz', 'wb')
                f_out.write(f_in.read())
                f_out.close()
                f_in.close()

        print("MNIST data gzipped")

    def image_to_mnist(self, toSquare = False, minSquareSize = 28, convertToGZip = True):
        self.make_sure_path_exists(self.main_folder + self.output_folder)
        for name in self.names:

            # Get all the image paths
            self.get_all_images(name)

            if (len(self.FileList) > 0): 

                shuffle(self.FileList) # Usefull for further segmenting the validation set

                # Extract the images and labels
                width, height = self.extract_images_and_labels(toSquare, minSquareSize)
            
                print("Width " + str(width) + " Height " + str(height))

                # Get header for labels
                header = self.header_label()
                self.data_label = header + self.data_label

                # Get header for images for specified width and height
                self.data_image = self.header_image(width, height, header) + self.data_image

                # Save data to file
                self.save_mnist_data(name)

            else: print("Sorry no files detected in the given path")

        if convertToGZip: self.GzipMnistFiles()
            
