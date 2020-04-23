# Import TensorFlow
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import cv2
import numpy as np
import morphsnakes as ms

# global Edge detection
# 1. loading photo
def cv2plt(img):
    plt.axis('off')
    if np.size(img.shape) == 3:
        plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    else:
        plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    plt.show()

# 2. print out edge
imgfile = '/Users/zhangle/Documents/IS/tabledetection/Data/test/IMG_0366.JPG'
imgfile = '/Users/zhangle/Documents/IS/tabledetection/Data/test/IMG_0623.jpg'
sym = cv2.imread(imgfile)
symg = cv2.cvtColor(sym, cv2.COLOR_BGR2GRAY)
symc = cv2.Canny(symg, 100, 127)

# 3. threthod 
i


