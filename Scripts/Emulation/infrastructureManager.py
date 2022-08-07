import os
import json
import argparse

def destroyInfrastructure(fileADir, removeImages):

	print ("Destroying the infrastructure")

	print ("Deleting main bridge")
	os.system('ovs-vsctl del-br brmain >/dev/null 2>&1')

	print ("Stoping containers")
	os.system("docker stop Cloud && docker rm Cloud >/dev/null 2>&1")
	os.system("docker stop MECHost && docker rm MECHost >/dev/null 2>&1")

	with open(fileADir, "r") as json_file:

		data = json.load(json_file)
		nodes = data["nodes"]

		for node in nodes:

			if(node["nodeType"] == "BaseStation"):
				os.system("ovs-vsctl del-br bs{} >/dev/null 2>&1".format(node["nodeNumber"]))
				os.system("ip link del br-pt{} >/dev/null 2>&1".format(node["nodeNumber"]))

			if(node["nodeType"] == "UE"):
				os.system("docker stop UE{} && docker rm UE{} >/dev/null 2>&1".format(node["nodeNumber"], node["nodeNumber"]))

	if (removeImages):
		print ("Remove QoE-DASH's images")
		os.system ("docker rmi qdserver")
		os.system ("docker rmi qdclient")

	print ("Infrastructure destroyed!")

def deployInfrastructure(fileADir):

	os.system('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
	os.system('sysctl -w net.ipv6.conf.default.disable_ipv6=1')

	with open(fileADir, "r") as json_file:

		data = json.load(json_file)
		nodes = data["nodes"]
		limits = data["limits"]

		print ("Creating main bridge")
		os.system("ovs-vsctl add-br brmain && ifconfig brmain 0 && ifconfig brmain 10.16.0.1/24")

		for node in nodes:

			if(node["nodeType"] == "Cloud"):
				print ("Creating Cloud node")
				os.system("docker run -d -t --network=none --cap-add=NET_ADMIN --name Cloud qdserver")
				os.system("ovs-docker add-port brmain eth1 Cloud --ipaddress=10.16.0.{}/24".format(node["nodeNumber"] + 1))
				#Cint
				Cint = int(float(limits["internetCapacity"]) * 1000.0)
				os.system('docker exec -d Cloud sh -c "wondershaper eth1 {} {}"'.format(Cint, Cint))

			if(node["nodeType"] == "MECHost"):
				print ("Creating MEC Host node")
				os.system("docker run -d -t --network=none --cap-add=NET_ADMIN --name MECHost qdserver")
				os.system("ovs-docker add-port brmain eth1 MECHost --ipaddress=10.16.0.{}/24".format(node["nodeNumber"] + 1))

			if(node["nodeType"] == "BaseStation"):

				print ("Creating base station {}".format(node["nodeNumber"]))

				os.system("ovs-vsctl add-br bs{} && ifconfig bs{} 0 && ifconfig bs{} 10.16.0.{}/24".format(node["nodeNumber"], node["nodeNumber"], node["nodeNumber"], node["nodeNumber"] + 1))

				os.system("ip link add br-pt{} type veth peer name bs-pt{}".format(node["nodeNumber"], node["nodeNumber"]))
				os.system("ifconfig br-pt{} up".format(node["nodeNumber"]))
				os.system("ifconfig bs-pt{} up".format(node["nodeNumber"]))

				os.system("ovs-vsctl add-port brmain bs-pt{}".format(node["nodeNumber"]))
				os.system("ovs-vsctl add-port bs{} br-pt{}".format(node["nodeNumber"], node["nodeNumber"]))

				rate = int(float(node["bsCapacity"]) * 1000.0)
				burst = int(rate / 10)

				#n*C
				os.system("ovs-vsctl set interface bs-pt{} ingress_policing_rate={}".format(node["nodeNumber"], rate))
				os.system("ovs-vsctl set interface bs-pt{} ingress_policing_burst={}".format(node["nodeNumber"], burst))
				#n*C
				os.system("ovs-vsctl set interface br-pt{} ingress_policing_rate={}".format(node["nodeNumber"], rate))
				os.system("ovs-vsctl set interface br-pt{} ingress_policing_burst={}".format(node["nodeNumber"], burst))

			if(node["nodeType"] == "UE"):

				print ("Creating UE {}".format(node["nodeNumber"]))

				os.system("docker run -d -t --network=none --cap-add=NET_ADMIN --name UE{} qdclient".format(node["nodeNumber"]))
				os.system("ovs-docker add-port bs{} eth1 UE{} --ipaddress=10.16.0.{}/24".format(node["bsAsc"], node["nodeNumber"], node["nodeNumber"] + 1))

				#C
				ueCapacity = int(float(node["ueCapacity"]) * 1000.0)
				os.system('docker exec -d UE{} sh -c "wondershaper eth1 {} {}"'.format(node["nodeNumber"], ueCapacity, ueCapacity))
				
def main ():

	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--infra", help="The topology file created by the Topology generator")
	parser.add_argument("-c", "--create", help="Indicates that you want to create the infrastructure", action='store_true')
	parser.add_argument("-d", "--destroy", help="Indicates that you want to destroy the infrastructure", action='store_true')
	parser.add_argument("-r", "--removeImages", help="Indicates that you want to remove the QoE-DASH Docker images", action='store_true')
	args = parser.parse_args()

	if (args.create):
		deployInfrastructure(args.infra)

	elif (args.destroy):
		destroyInfrastructure(args.infra, args.removeImages)

	else:
		print ("You need to select if you want to create or destroy the infrastructure.")

if __name__ == '__main__':
	main()