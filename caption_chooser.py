import csv
import random

column_inds = {'Caption':0, 'Keywords': 1, 'Emotion':2, 'selfie':3, 'group':4, 'summer':5, 'night':6, 'out': 7, 'birthday': 8}



class Caption():
	def __init__(self, row):
		self.text = str(row[column_inds['Caption']]).decode('utf-8')
		self.keywords = set(row[column_inds['Keywords']].split('/'))
		self.emotions = set(row[column_inds['Emotion']].split(', '))
		self.selfie = True if row[column_inds['selfie']] == "TRUE" else False
		self.group = True if row[column_inds['group']] == "TRUE" else False
		self.summer = True if row[column_inds['summer']] == "TRUE" else False
		self.night = True if row[column_inds['night']] == "TRUE" else False
		self.bday = True if row[column_inds['birthday']] == "TRUE" else False
		self.club = True if row[column_inds['out']] == "TRUE" else False


class Lookup():
	def __init__(self, csv_):
		with open(csv_, 'r') as infile:
			self.keyword_set = set([])
			self.captions = []

			for r in infile:
				row = r.split('|')
				self.keyword_set = self.keyword_set.union(row[column_inds['Keywords']].split("/"))
				self.captions.append(Caption(row))
			self.query_set = set(self.captions)
 


	def filter_by_option(self, button, value):
		return set([c for c in self.captions if getattr(c, button) == value])

	def return_keyword_intersection(self, api_set):
		return self.keyword_set.intersection(api_set)

	def captions_with_emotions(self, emotion):
		return set([c for c in self.captions if emotion in c.emotions])


	def captions_with_keywords(self, keywords):
		s = set([c for c in self.captions if c.keywords.intersection(keywords)])
		print([a.text for a in s])
		print("###")
		return s
 

	def get_captions(self, emotion, api_keywords):
		keywords = self.return_keyword_intersection(api_keywords)

		from_emotion = self.captions_with_emotions(emotion)
		print([f.keywords for f in from_emotion])
		print("####")
 
		print get_text(from_emotion)
		from_keywords = from_emotion.intersection(self.captions_with_keywords(keywords))
		if from_keywords:
			return random.choice(get_text(from_keywords))
		elif from_emotion:
			return random.choice(get_text(from_emotion))
		else: 
			return "I only love my bed and my momma, Im sorry"

def get_text(captions):
	return [str(c.text) for c in captions]
