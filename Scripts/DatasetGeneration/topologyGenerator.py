import csv
import json
import argparse

def serialize (obj):
	return obj.__dict__

def generateUsers (file):

	userList = []

	with open (file, newline = '') as users:

		reader = csv.reader(users)

		for line in reader:

			line = ''.join(line)
			user = line.split("#", 3)

			userList.append(user)

	return userList

def generateTopology (tpd, ilc):

	#Generating users list
	userList = generateUsers(tpd)
	numberOfUsers = len (userList)
	nodeList = []

	#Definition of Cloud and MECHost nodes
	cloud = {"nodeNumber": 1, "nodeType": "Cloud"}
	MECHost = {"nodeNumber": 2, "nodeType": "MECHost"}
	nodeList.append(cloud)
	nodeList.append(MECHost)

	#Reference: https://doi.org/10.1109/TVT.2018.2889196
	ciqDict = {

		#1.5 Mbps, 360p
		1: 2.768,
		2: 2.768,
		#4 Mbps, 480p
		3: 4.432,
		#7.5 Mbps, 720p
		4: 7.548,
		5: 10.320,
		#12 Mbps, 1080p
		6: 13.936,
		7: 17.520,
		8: 22.896,
		#24 Mbps, 1440p (2K)
		9: 30.528,
		10: 32.832,
		11: 42.768,
		12: 50.912,
		#53 Mbps, 2160p (4K)
		13: 56.672,
		14: 63.408,
		15: 63.408

	}

	#Generating base station list
	bsList = []
	for bsIndex in range (len (userList)):

		if (userList[bsIndex][3] not in bsList):
			bsList.append (userList[bsIndex][3])

	#Calculating CQI sum and creating bs dict
	cqiSum = 0
	bsDict = {index: [0, []] for index in bsList}
	for userIndex in range (numberOfUsers):
		bsDict[userList[userIndex][3]][0] += ciqDict[int(userList[userIndex][1])]
		bsDict[userList[userIndex][3]][1].append (int(userList[userIndex][0]))
		cqiSum += ciqDict[int(userList[userIndex][1])]

	#Appending each BS
	for bsIndex in range (len (bsDict)):
		nodeNumber = bsIndex + 3
		BS = {"nodeNumber": nodeNumber, "nodeType": "BaseStation", "numberUEs": len(bsDict[userList[bsIndex][3]][1]), "bsCapacity": bsDict[userList[bsIndex][3]][0]}
		nodeList.append(BS)

	#Appending each UE
	for userIndex in range (numberOfUsers):
		nodeNumber = nodeNumber + 1
		userCQI = ciqDict[int(userList[userIndex][1])]
		screenRes = int(userList[userIndex][2])
		bsAsc = int(userList[userIndex][3])
		UE = {"nodeNumber": nodeNumber, "nodeType": "UE", "bsAsc": bsAsc, "ueCapacity": userCQI, "screenRes": screenRes}
		nodeList.append(UE)

	#Defining and calculating network limits, in this case, the internet capacity
	limits = {"internetCapacity": round((cqiSum * float(ilc)) / 100.0, 3)}

	topology = {"nodes": nodeList, "limits": limits}

	#Exporting JSON
	json_out_file = open('topology.json', 'w')
	json.dump(topology, json_out_file, default = serialize, indent = 4)

def main ():

	parser = argparse.ArgumentParser()
	parser.add_argument("-tpd", "--tpd", help="The topology description in CSV")
	parser.add_argument("-ilc", "--ilc", help="The internet link capacity")

	args = parser.parse_args()

	generateTopology (args.tpd, args.ilc)

if __name__ == '__main__':
	main()