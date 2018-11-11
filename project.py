# CS224W Project
# David Golub and Liam Kelly
# Stanford University

import json
import snap
import numpy
import matplotlib.pyplot as plt

def read_json_file(filename="price_data_raw.json"):
	read_file = open(filename, "r")
	data = json.load(read_file)
	read_file.close()
	return data

def write_json_file(data, filename="price_data.json"):
	write_file = open(filename, "w")
	json.dump(data, write_file, indent=4)
	write_file.close()

if __name__ == "__main__":
	price_data = read_json_file()
	write_json_file(price_data)
