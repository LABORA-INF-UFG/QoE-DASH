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

def generateTopology (tpd, ilc, abr):

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
		1: round(2.768 + abr, 3),
		2: round(2.768 + abr, 3),
		#4 Mbps, 480p
		3: round(4.432 + abr, 3),
		#7.5 Mbps, 720p
		4: round(7.548 + abr, 3),
		5: round(10.320 + abr, 3),
		#12 Mbps, 1080p
		6: round(13.936 + abr, 3),
		7: round(17.520 + abr, 3),
		8: round(22.896 + abr, 3),
		#24 Mbps, 1440p (2K)
		9: round(30.528 + abr, 3),
		10: round(32.832 + abr, 3),
		11: round(42.768 + abr, 3),
		12: round(50.912 + abr, 3),
		#53 Mbps, 2160p (4K)
		13: round(56.672 + abr, 3),
		14: round(63.408 + abr, 3),
		15: round(63.408 + abr, 3)

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
	parser.add_argument("-tpd", "--tpd", help="A CSV file describing the topology")
	parser.add_argument("-ilc", "--ilc", help="The internet link capacity")
	parser.add_argument("-bAud", "--abr", help="Audio bit rate (in kbps) (The same audio bitrate used to encode the video).")

	args = parser.parse_args()

	generateTopology (args.tpd, args.ilc, (float(args.abr) / 1000.0))

if __name__ == '__main__':
	main()