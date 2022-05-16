import os
import gdown
import argparse

def downloadDataset (d24fps, d30fps, d48fps, d60fps, dfull):

	if (d24fps):

		print ("Downloading 24 FPS data set")
		id = "1jxTB24SOmPBqjH6lnIRHjFwApOi_24Iy"
		gdown.download(id=id, output='24fps-QoE-DASH-Dataset.zip', quiet=False)

		if(os.path.exists('24fps-QoE-DASH-Dataset.zip')):

			print ("Extracting 24 FPS data set")
			os.system ("unzip 24fps-QoE-DASH-Dataset.zip")

			print ("Deleting zipped 24 FPS data set")
			os.system ("rm 24fps-QoE-DASH-Dataset.zip")

	if (d30fps):

		print ("Downloading 30 FPS data set")
		id = "1q-frHrcd_FRrFIdz1uKy-clTKBup2xG3"
		gdown.download(id=id, output='30fps-QoE-DASH-Dataset.zip', quiet=False)

		if(os.path.exists('30fps-QoE-DASH-Dataset.zip')):

			print ("Extracting 30 FPS data set")
			os.system ("unzip 30fps-QoE-DASH-Dataset.zip")

			print ("Deleting zipped 30 FPS data set")
			os.system ("rm 30fps-QoE-DASH-Dataset.zip")

	if (d48fps):

		print ("Downloading 48 FPS data set")
		id = "12L86kWZi8d02IPPPUuCA3VodxFtn57hT"
		gdown.download(id=id, output='48fps-QoE-DASH-Dataset.zip', quiet=False)

		if(os.path.exists('48fps-QoE-DASH-Dataset.zip')):

			print ("Extracting 48 FPS data set")
			os.system ("unzip 48fps-QoE-DASH-Dataset.zip")

			print ("Deleting zipped 48 FPS data set")
			os.system ("rm 48fps-QoE-DASH-Dataset.zip")

	if (d60fps):

		print ("Downloading 60 FPS data set")
		id = "18PVqHgQ06OSykbwzm1FUjEMmjOH5Tf46"
		gdown.download(id=id, output='60fps-QoE-DASH-Dataset.zip', quiet=False)

		if(os.path.exists('60fps-QoE-DASH-Dataset.zip')):

			print ("Extracting 60 FPS data set")
			os.system ("unzip 60fps-QoE-DASH-Dataset.zip")

			print ("Deleting zipped 60 FPS data set")
			os.system ("rm 60fps-QoE-DASH-Dataset.zip")

	if (dfull):

		print ("Downloading Full data set")
		id = "1Zz-XXOawPS1qll920ddcSxIt_4pLMAtK"
		gdown.download(id=id, output='QoE-DASH-Dataset-Full.zip', quiet=False)

		if(os.path.exists('QoE-DASH-Dataset-Full.zip')):

			print ("Extracting Full data set")
			os.system ("unzip QoE-DASH-Dataset-Full.zip")

			print ("Deleting zipped Full data set")
			os.system ("rm QoE-DASH-Dataset-Full.zip")

def main ():

	parser = argparse.ArgumentParser()

	parser.add_argument("-24", "--d24fps", help="Indicates that we want to download the 24 FPS data set", action='store_true')
	parser.add_argument("-30", "--d30fps", help="Indicates that we want to download the 30 FPS data set", action='store_true')
	parser.add_argument("-48", "--d48fps", help="Indicates that we want to download the 48 FPS data set", action='store_true')
	parser.add_argument("-60", "--d60fps", help="Indicates that we want to download the 60 FPS data set", action='store_true')
	parser.add_argument("-full", "--dfull", help="Indicates that we want to download the full data set", action='store_true')

	args = parser.parse_args()

	downloadDataset (args.d24fps, args.d30fps, args.d48fps, args.d60fps, args.dfull)

if __name__ == '__main__':
	main()