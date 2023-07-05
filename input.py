import pickle
import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt

def print_images(images):
    fig, axes = plt.subplots(3, 3, figsize=(5, 5))
    axes = axes.flatten()
    for i in range(9):
        axes[i].imshow(images[i])
        axes[i].axis('off')
    plt.tight_layout()
    plt.show()

def process(img):
    imx = np.zeros((128,128,3))
    for ch in range(3):
        sub_channel = np.array(img[:,:,ch])
        imx[:, :, ch] = cv2.resize(sub_channel, (128, 128))
    return imx/255

# Load the image
image_path = '/home/sanat/Documents/Projects/ALL/Captcha Image/Test Captcha/2.png'
image = cv2.imread(image_path)
height = image.shape[0]//3
print(height)
images = []
for i in range(3):
    for j in range(3):
        print(height*i,height*(i+1), height*j,height*(j+1))
        ix = image[height*i+5:height*(i+1)-5, height*j+5:height*(j+1)-5, : ]
        images.append(process(ix))
images = np.array(images)

print(images.shape)

pickle_in = open("Best_model.pkl", "rb")  ## rb = READ BYTE
Model = pickle.load(pickle_in)
file = open('Categories.txt')
categories = [x.strip() for x in file.readline()[1:-1].replace("'", "").split(",")]
print(categories)

pred = np.round(Model.predict(images), 2)
print(pred)
print_images(images)

np.savez('test', images)