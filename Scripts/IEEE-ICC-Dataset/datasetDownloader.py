import os
import gdown
import argparse

def downloadDataset (d24fps, d30fps, d48fps, d60fps, dfull):

	if (d24fps):
		print ("Downloading 24 FPS data set")
		id = "156eHdlnTNOeLjXL5ZdGyfirEl6ncbNDE"
		gdown.download(id=id, output='24fps-QoE-DASH-Dataset.zip', quiet=False)

	if (d30fps):
		print ("Downloading 30 FPS data set")
		id = "1Ext-Ipw7DUd3_SFgoKMExc2h7iTbgoAT"
		gdown.download(id=id, output='30fps-QoE-DASH-Dataset.zip', quiet=False)

	if (d48fps):
		print ("Downloading 48 FPS data set")
		id = "1yDFbu82TpRna5qVmYhyv2ubtgMcVBdAK"
		gdown.download(id=id, output='48fps-QoE-DASH-Dataset.zip', quiet=False)

	if (d60fps):
		print ("Downloading 60 FPS data set")
		id = "1BDJfjPuEdwZcBd8cZhPY4i6nIrmh1Pil"
		gdown.download(id=id, output='60fps-QoE-DASH-Dataset.zip', quiet=False)

	if (dfull):
		print ("Downloading Full data set")
		id = "1Zz-1M0s9qlflMBRecqt_9JUY7peYd4XyMZRA"
		gdown.download(id=id, output='QoE-DASH-Dataset-Full.zip', quiet=False)

def main ():

	parser = argparse.ArgumentParser()

	parser.add_argument("-24", "--d24fps", help="Indicates that you want to download the 24 FPS data set", action='store_true')
	parser.add_argument("-30", "--d30fps", help="Indicates that you want to download the 30 FPS data set", action='store_true')
	parser.add_argument("-48", "--d48fps", help="Indicates that you want to download the 48 FPS data set", action='store_true')
	parser.add_argument("-60", "--d60fps", help="Indicates that you want to download the 60 FPS data set", action='store_true')
	parser.add_argument("-full", "--dfull", help="Indicates that you want to download the full data set", action='store_true')

	args = parser.parse_args()

	downloadDataset (args.d24fps, args.d30fps, args.d48fps, args.d60fps, args.dfull)

if __name__ == '__main__':
	main()