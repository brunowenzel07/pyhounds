# -*- coding: UTF-8
# !/usr/bin/python 

import csv 
import numpy as np 

class Database:
	""" Create a database connections """
	def __init__(self, f):    	
		self.file = f 

	def insert(self, rows):
		""" 
			Insert multiple line in file 
		"""
		try:
			with open(self.file, "a") as csvfile:
				for r in rows: 
					writer = csv.writer(csvfile)
					writer.writerow(r)
		except Exception as a:
			print(a)

	def load_tuning(self):
		data_train = []
		with open("tuning.csv", "r") as csvfile:
			rows = csv.reader(csvfile)
			for r in rows:
				data_train.append(np.array(r).astype(np.float))
		return data_train

	def load(self):

		results = []
		stats = []

		with open(self.file, "r") as csvfile:
			rows = csv.reader(csvfile)
			for r in rows:
				results.append(float(r[0]))
				stats.append(np.array(r[1:]).astype(np.float))
		return [stats, results]