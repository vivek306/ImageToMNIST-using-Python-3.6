from image_mnist import image_mnist

import os
import sys, getopt

def main(argv):
    mainfolder = './'
    trainfolder = 'training-images'
    testfolder = 'test-images'
    outputfolder = ''
    issquare = False
    minsquare = 28
    try:
        opts, args = getopt.getopt(argv,"hm:r:e:o:q:s",["mainfolder=","trainfolder=","testfolder=",
                                                        "outputfolder=","square=","minsquare="])
    except getopt.GetoptError:
        print ('main.py -m <mainfolder> -r <trainfolder> -e <testfolder> -o <outputfolder> -q <square> -s <minsquare>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('main.py -m <mainfolder> -r <trainfolder> -e <testfolder> -o <outputfolder> -q <square> -s <minsquare>')
            print ('main.py -m <mainfolder>    - The parent folder containing train, test and output images')
            print ('main.py -r <trainfolder>   - The folder that contains all training images')
            print ('main.py -e <testfolder>    - The folder that contains all testing images')
            print ('main.py -o <outputfolder>  - The folder outputting the idx images')
            print ('main.py -q <square>        - Force converts all the images to squares')
            print ('main.py -q <minsquare>     - Minimum size of the images')
            print ('Default is set to -> main.py  -m ./ -r training-images -e test-images')
            sys.exit()
        elif opt in ("-m", "--mainfolder"):
            if arg != "":
                mainfolder = arg
                if mainfolder == "./":
                    mainfolder = os.path.dirname(os.path.realpath(__file__)) + "\\"
        elif opt in ("-r", "--trainfolder"):
            if arg != "":
                trainfolder = arg
        elif opt in ("-e", "--testfolder"):
            if arg != "":
                testfolder = arg
        elif opt in ("-o", "--outputfolder"):
            if arg != "":
                outputfolder = arg + "\\"
        elif opt in ("-q", "--square"):
            if arg != "" and arg.isdigit():
                if arg == 1: 
                    issquare = True
        elif opt in ("-s", "--minsquare"):
            if arg != "" and arg.isdigit():
                minsquare = arg
   
    ### Convert Image to MNIST Data
    itm = image_mnist(main_folder = mainfolder, output_folder = outputfolder,
                        train_folder = trainfolder, test_folder = testfolder)
    itm.image_to_mnist()


if __name__ == "__main__":
    main(sys.argv[1:])

