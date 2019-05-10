# -*- coding: UTF-8
# !/usr/bin/python 

import csv 
import numpy as np 

class Database:
	""" Create a database connections """
	def __init__(self, f):    	
		self.file = f 

	def insert(self, rows, type_insert):
		""" 
			Insert multiple line in file 
		"""
		try:
			with open(self.file, "a") as csvfile:
				if type_insert=="multiple":
					for r in rows: 
						writer = csv.writer(csvfile)
						writer.writerow(r)
				if type_insert=="solo":						
					writer = csv.writer(csvfile)
					writer.writerow(rows)

		except Exception as a:
			print(a)
	
	def load(self):
		with open("data/data_train.csv", "r") as csvfile:
			rows = csv.reader(csvfile)
			stats, results = [], []
			for r in rows:
				results.append(r)				
		return np.array(results).astype(np.float)


