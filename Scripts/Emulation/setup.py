import os
import argparse

def setup (cacheMovies, encodedVideo):

	imageServer = os.system ("docker image inspect qdserver >/dev/null 2>&1")
	imageClient = os.system ("docker image inspect qdclient >/dev/null 2>&1")

	if(imageServer == 256):

		print ("Downloading QoE-DASH server Docker image")
		os.system ("docker pull joaopauloesper/qdserverclean")

		print ("Starting QoE-DASH server container")
		os.system ("docker run -dit --name qdserverclean -p 8080:80 joaopauloesper/qdserverclean")

		print ("Copying encoded video and manifests to QoE-DASH server container")
		os.system ("docker cp {}/. qdserverclean:/usr/local/apache2/htdocs/cacheMovies/".format(cacheMovies))

		print ("Copying encoded video to QoE-DASH server container")
		print ("This may take a while depending on the size of your video")
		os.system ("docker cp {}/. qdserverclean:/usr/local/apache2/htdocs/".format(encodedVideo))

		print ("Saving QoE-DASH server container to image")
		os.system ("docker commit qdserverclean qdserver")
		os.system ("docker stop qdserverclean")
		os.system ("docker rm qdserverclean")
		os.system ("docker rmi joaopauloesper/qdserverclean")

	if(imageClient == 256):

		print ("Downloading QoE-DASH client Docker image")
		os.system ("docker pull joaopauloesper/qdclient")

		print ("Configuring QoE-DASH client Docker image")
		os.system ("docker image tag joaopauloesper/qdclient qdclient")
		os.system ("docker rmi joaopauloesper/qdclient")

	if (imageServer != 256 and imageClient != 256):
		print ("QoE-DASH is ready to run")

def main ():

	parser = argparse.ArgumentParser()

	parser.add_argument("-c", "--cacheMovies", help="The location of the manifests created by 'Manifest generator'")
	parser.add_argument("-e", "--encodedVideo", help="The location of the video that was enconded by 'Video enconding'")

	args = parser.parse_args()

	checkDockerInstallation = os.system ("docker >/dev/null 2>&1")

	if (checkDockerInstallation == 32512):
		print ("Please install Docker before running the setup script")

	else:
		setup (args.cacheMovies, args.encodedVideo)

if __name__ == '__main__':
	main()