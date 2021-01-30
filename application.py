from flask import Flask,redirect,url_for,render_template,request,jsonify
import requests
app = Flask(__name__)
from PIL import Image
import json
import numpy as np
import os
# os.system('apt update && apt install -y libsm6 libxext6')
from cv2 import imread, resize  
import tensorflow as tf
from flask import send_file
from keras.models import model_from_json
from keras.preprocessing.image import img_to_array
from flask import send_from_directory

json_file = open('model.json','r')
loaded_model_json = json_file.read()
json_file.close()

# some fixes 
graph=None
graph = tf.get_default_graph()

loaded_model = model_from_json(loaded_model_json)
#load woeights into new model
loaded_model.load_weights("Retraining.h5")
print("Loaded Model from disk")

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/vnd.microsoft.icon')

@app.route('/about',methods=['GET'])
def results():
	return jsonify("U are in home page, there is nothing here, go for /post and upload image")

def weAreLive(url):
	pic_url=url
	with open('test.jpg', 'wb') as handle:
	        response = requests.get(pic_url, stream=True)

	        if not response.ok:
	            print (response)

	        for block in response.iter_content(1024):
	            if not block:
	                break

	            handle.write(block)
	#     preprocessing the image 
	image = imread('test.jpg')
	image = resize(image, (160,160))
	image = img_to_array(image)
	image= np.array(image, dtype="float") / 255.0
	#     cv2.imshow('ImageWindow',image)
	#     cv2.waitKey()
	#         Making the predictions
	img=np.expand_dims(image, axis=0)
	# clear_session()
	global loaded_model
	# loaded_model._make_predict_function()
	with graph.as_default():
		res=loaded_model.predict(img)
	os.remove("test.jpg")
	print("prediction from model is ",res)
	predictionResults={}
	predictionResults["Baseball"]=str(res[0][0])
	predictionResults["Cricket"]=str(res[0][1])
	
	return predictionResults
	if res[0][0]>res[0][1]:
	    return "Baseball"
	else:
	    return "Cricket"
	#     deleting the file at last


@app.route("/")
def index():
    return render_template('index.html')

# request would be made from js code
@app.route("/predict",methods=["POST"])
def predict():
	print("request for prediction has body ",request.json)
	# what if user didnot apply any filter
	x=request.json.get("url")
	print("url for image in .py ",x)
	# x="https://i.ytimg.com/vi/O5bV5LVVr5A/maxresdefault.jpg"
	res=weAreLive(x)
	return jsonify(result=res)
	# return json.dumps({"res":"scsasa"})

if __name__ == '__main__':
	app.debug=True
	app.run()