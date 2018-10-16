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

	def load_tuning(self):
		results = []
		stats = []
		with open("data/data_test.csv", "r") as csvfile:
			rows = csv.reader(csvfile)
			for r in rows:		
				del(r[5:10])	
				del(r[-6:-1])		
				results.append(float(r[-1]))
				stats.append(np.array(r[:-1]).astype(np.float))
		return [stats, results]

	def load(self):
		results = []
		stats = []

		with open(self.file, "r") as csvfile:
			rows = csv.reader(csvfile)
			for r in rows:	
				results.append(float(r[-1]))
				stats.append(np.array(r[:-1]).astype(np.float))
		return [stats, results]


