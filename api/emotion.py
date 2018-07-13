import json
import requests
import operator
from pprint import pprint


def get_key_emotions(filepath, quantity, threshold):
	url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"

	querystring = {"returnFaceId":"true","returnFaceLandmarks":"false","returnFaceAttributes":"age,emotion"}

	# payload = "{\r\n    \"url\": \"https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg\"\r\n}"
	image_path = filepath
	payload = open(image_path, "rb").read()
	headers = {
	    'Content-Type': "application/octet-stream",
	    'Ocp-Apim-Subscription-Key': "f7cc7188927541078caa21df324807fc",
	    'Cache-Control': "no-cache"
	    }

	response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

	emotions = []
	for face in json.loads(response.text):
		emotions.append(face['faceAttributes']['emotion'])

	return find_keys_emotion(emotions, quantity, threshold)

def find_keys_emotion(emotions, quantity, threshold):
	list_of_emotion_tuples = []
	emotions_over_threshold = []
	visited = set()
	for person_emotion in emotions:
		list_of_emotion_tuples += person_emotion.items()

  	for emotion_tuple in sorted(list_of_emotion_tuples, key=operator.itemgetter(1))[::-1]:
  		# print emotion_tuple, type(emotion_tuple[1]), emotion_tuple[1], threshold
  		if emotion_tuple[1]>threshold and not emotion_tuple[0] in visited:
  			emotions_over_threshold.append(emotion_tuple)
  			visited.add(emotion_tuple[0])

  	if emotions_over_threshold:
  		print emotions_over_threshold
  		return emotions_over_threshold[0][0]
  	else:
  		return None
