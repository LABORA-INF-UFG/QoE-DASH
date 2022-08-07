import os
import csv
import json
import time
import argparse

def generateFile (file, size):

	userList = []

	with open (file, newline = '') as users:

		reader = csv.reader(users)

		for line in reader:

			line = ''.join(line)
			user = line.split("#", size)

			userList.append(user)

	return userList

def serviceManager (catalog, moviesCache, usersMovies, fileADir):

	usersList = generateFile(usersMovies, 2)
	moviesCacheList = generateFile(moviesCache, 1)

	maxStreamDur = 0

	for indexUsers in range (len(usersList)):

		with open('../../InputFiles/configTemplate.json', 'r') as file:
			filedata = file.read()

		movieInCache = 0

		for indexMovies in range (len(moviesCacheList)):

			if(moviesCacheList[indexMovies][0] == usersList[indexUsers][1]):
				movieInCache = 1
				#All init files are stored in the Cloud
				url = '"url": "[http://10.16.0.2/cacheMovies/manifestMovie{}.mpd]",'.format(usersList[indexUsers][1])

		if (movieInCache == 0):
			url = '"url": "[http://10.16.0.2/cacheMovies/cloudManifest.mpd]",'

		logFile = "log_usr{}_mov{}_rep{}".format(usersList[indexUsers][0], usersList[indexUsers][1], usersList[indexUsers][2])
				
		if (int(usersList[indexUsers][2]) == 1):
			maxHeight = 360

		if (int(usersList[indexUsers][2]) == 2):
			maxHeight = 480

		if (int(usersList[indexUsers][2]) == 3):
			maxHeight = 720

		if (int(usersList[indexUsers][2]) == 4):
			maxHeight = 1080

		outputFolder = "dir_usr{}_mov{}_rep{}".format(usersList[indexUsers][0], usersList[indexUsers][1], usersList[indexUsers][2])

		with open(catalog, "r") as csvcatalog:

		    reader = csv.reader(csvcatalog)

		    for line_num, content in enumerate(reader):
		        if content[0] == usersList[indexUsers][1]:
		            streamDuration = content[2]
		            if(int(streamDuration) > maxStreamDur):
		            	maxStreamDur = int(streamDuration)

		filedata = filedata.replace('"url" : "",', url)
		filedata = filedata.replace('"logFile" : "",', '"logFile" : "{}",'.format(logFile))
		filedata = filedata.replace('"maxHeight" : ,', '"maxHeight" : {},'.format(maxHeight))
		filedata = filedata.replace('"outputFolder" : "",', '"outputFolder" : "{}",'.format(outputFolder))
		filedata = filedata.replace('"streamDuration" : ,', '"streamDuration" : {},'.format(streamDuration))

		configName = 'config{}.json'.format(indexUsers + 1)

		with open(configName, 'w') as file:
			file.write(filedata)

	userIndex = 1
	with open(fileADir, "r") as json_file:

		data = json.load(json_file)
		nodes = data["nodes"]

		for node in nodes:

			if(node["nodeType"] == "UE"):
				os.system ("docker cp config{}.json UE{}:/goDASH/godash/config{}.json".format(userIndex, node["nodeNumber"], userIndex))
				os.system ('docker exec -d UE{} sh -c "cd goDASH/godash/ && ./godash -config config{}.json"'.format(node["nodeNumber"], userIndex))
				userIndex += 1

	print ("Emulation running!")
	print ("Now QoE-DASH will wait {} seconds (duration of the longest movie you requested to emulate) before copying the results to your machine.".format(maxStreamDur))

	for index in range(maxStreamDur,0,-1):
		time.sleep(1)
		print (index)

	print ("Emulation finished!")

	print ("Copying results")

	if (not os.path.isdir('EmulationResults')):
		os.system ("mkdir EmulationResults")

	userIndex = 0
	with open(fileADir, "r") as json_file:

		data = json.load(json_file)
		nodes = data["nodes"]

		for node in nodes:

			if(node["nodeType"] == "UE"):

				outputLocation = "dir_usr{}_mov{}_rep{}/logDownload.txt".format(usersList[userIndex][0], usersList[userIndex][1], usersList[userIndex][2])
				logName = "usr{}_mov{}_rep{}".format(usersList[userIndex][0], usersList[userIndex][1], usersList[userIndex][2])

				os.system ("docker cp UE{}:/goDASH/godash/files/{} EmulationResults/".format(node["nodeNumber"], outputLocation))
				os.system ("mv EmulationResults/logDownload.txt EmulationResults/{}.csv".format(logName))

				userIndex += 1

	os.system ("rm config*.json")

	print ("Results saved in 'EmulationResults'")
	
def main ():

	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--catalog", help="A CSV file describing the movie catalog")
	parser.add_argument("-m", "--moviesCache", help="A CSV file describing the movies in cache")
	parser.add_argument("-u", "--usersMovies", help="A CSV file describing the movies the users are going to request")
	parser.add_argument("-t", "--infra", help="The topology file created by the Topology generator")
	
	args = parser.parse_args()

	serviceManager (args.catalog, args.moviesCache, args.usersMovies, args.infra)

if __name__ == '__main__':
	main()