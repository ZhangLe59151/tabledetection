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

# 3. threthod detect horizion
# kernel = [0,1,0,1,-4,1,0,1,0] //edge
# kernel = [0,-1,0,0,2,0,0,-1,0] // - edge
# kernel = [0,0,0,-1,2,-1,0,0,0] // | edge
ret,imgbinary = cv2.threshold(symg, 127, 255, cv2.THRESH_BINARY)
kernel = tf.constant([[[0,-1,0],[0,2,0],[0,-1,0]]],shape=[3,3,1,1],dtype=tf.float32)

image_show = tf.constant(imgbinary, shape=[imgbinary.shape[0], imgbinary.shape[1]], dtype=tf.float32)
image_batch = tf.expand_dims(image_show, 0)
image_batch = tf.expand_dims(image_batch, 3)
print(image_batch.shape)

conv2d = tf.nn.conv2d(image_batch, kernel, strides=1, padding='SAME')
activation_map = tf.minimum(tf.nn.relu(conv2d),255)
result = tf.squeeze(activation_map, 0)
result = tf.squeeze(result, 2)

image = result.numpy()
cv2plt(image)