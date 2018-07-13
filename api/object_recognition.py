import requests
import json
from pprint import pprint
from io import BytesIO

def get_tags(filepath, threshold):
	subscription_key = "8bee5113c3314984b4350a52fc01796b"
	assert subscription_key

	vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"
	analyze_url = vision_base_url + "analyze"

	# Set image_path to the local path of an image that you want to analyze.
	image_path = filepath

	# Read the image into a byte array
	image_data = open(image_path, "rb").read()
	headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
	              'Content-Type': 'application/octet-stream'}
	params     = {'visualFeatures': 'Categories,Description,Color,Tags'}
	response = requests.post(
	    analyze_url, headers=headers, params=params, data=image_data)
	response.raise_for_status()

	# The 'analysis' object contains various fields that describe the image. The most
	# relevant caption for the image is obtained from the 'description' property.
	analysis = response.json()

	return [str(tag['name']) for tag in analysis['tags'] if tag['confidence'] > threshold]