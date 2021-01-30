
from tensorflow.keras.models import model_from_json

json_file = open('model.json','r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
#load woeights into new model
loaded_model.load_weights("ReTraining.h5")
print("Loaded Model from disk")


from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from imutils import paths
# import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import cv2
import os


# from PIL import Image
import requests


def weAreLive():
    pic_url=input('enter the url ')
    with open('test.jpg', 'wb') as handle:
            response = requests.get(pic_url, stream=True)

            if not response.ok:
                print (response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
#     preprocessing the image 
    image = cv2.imread('test.jpg')
    image = cv2.resize(image, (160,160))
    image = img_to_array(image)
#     cv2.imshow('ImageWindow',image)
#     cv2.waitKey()
#         Making the predictions
    res=loaded_model.predict(np.expand_dims(image, axis=0))
    if res[0][0]>res[0][1]:
        print("Baseball")
    else:
        print("Cricket")
#     deleting the file at last
    os.remove("test.jpg")
    


weAreLive()
