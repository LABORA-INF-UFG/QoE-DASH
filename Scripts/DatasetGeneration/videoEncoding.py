import os
import argparse

def createChunks (video, fps, segLen, b360, b480, b720, b1080, bAud, bAr, bAc):

	class color:
		RED = '\033[91m'
		END = '\033[0m'

	ResolutionHeightList = [360, 480, 720, 1080]
	VideoBitRates = []

	VideoBitRates.append(b360 * 1000)
	VideoBitRates.append(b480 * 1000)
	VideoBitRates.append(b720 * 1000)
	VideoBitRates.append(b1080 * 1000)

	segLen = float(segLen) * 1000

	for ResIndex in range (len(ResolutionHeightList)):

		print("{}Starting video enconding for {}p{}".format(color.RED, int(ResolutionHeightList[ResIndex]), color.END))

		os.system ('ffmpeg -y -i {} -c:v libx264 \
				-r {} -x264opts \'keyint={}:min-keyint={}:no-scenecut\' \
				-vf scale=-2:{} -b:v {}k -maxrate {}k \
				-movflags faststart -bufsize {}k \
				-profile:v main -preset fast -an \"video_intermed_{}p_{}fps.mp4\"'.
			format(video, fps, fps * 2, fps * 2, int(ResolutionHeightList[ResIndex]),
				   float(VideoBitRates[ResIndex]), float(VideoBitRates[ResIndex]), float(VideoBitRates[ResIndex]) * 2,
				   int(ResolutionHeightList[ResIndex]), fps))
		
		print ("{}Finished video enconding for {}p{}".format(color.RED, int(ResolutionHeightList[ResIndex]), color.END))

	if (bAud != -1.0 and bAr != -1.0 and bAc != -1.0):

		print ("{}Starting audio enconding{}".format(color.RED, color.END))

		os.system ('ffmpeg -y -i {} -map 0:1 -vn -c:a aac -b:a {}k -ar {}k -ac {} audio{}.m4a'
				.format(video, bAud, bAr, bAc, fps))

		print ("{}Finished audio enconding{}".format(color.RED, color.END))

		print ("{}Starting dashing{}".format(color.RED, color.END))

		os.system ("MP4Box -dash {} -frag {} -rap \
				-segment-name 'segment_$RepresentationID$_' -fps {} \
				video_intermed_{}p_{}fps.mp4#video:id=360p \
				video_intermed_{}p_{}fps.mp4#video:id=480p \
				video_intermed_{}p_{}fps.mp4#video:id=720p \
				video_intermed_{}p_{}fps.mp4#video:id=1080p \
				audio{}.m4a#audio:id=Audio:role=main \
				-out manifest.mpd".
				format(segLen, segLen, fps, ResolutionHeightList[0], fps, ResolutionHeightList[1], fps, ResolutionHeightList[2], fps, ResolutionHeightList[3], fps, fps))

		print ("{}Finished dashing{}".format(color.RED, color.END))

	else:

		print ("{}Starting dashing{}".format(color.RED, color.END))

		os.system ("MP4Box -dash {} -frag {} -rap \
				-segment-name 'segment_$RepresentationID$_' -fps {} \
				video_intermed_{}p_{}fps.mp4#video:id=360p \
				video_intermed_{}p_{}fps.mp4#video:id=480p \
				video_intermed_{}p_{}fps.mp4#video:id=720p \
				video_intermed_{}p_{}fps.mp4#video:id=1080p \
				-out manifest.mpd".
				format(segLen, segLen, fps, ResolutionHeightList[0], fps, ResolutionHeightList[1], fps, ResolutionHeightList[2], fps, ResolutionHeightList[3], fps))

		print ("{}Finished dashing{}".format(color.RED, color.END))

	os.system ("mkdir encodedVideo encodedVideo/360p encodedVideo/480p encodedVideo/720p encodedVideo/1080p encodedVideo/Audio")

	os.system ("mv *.mpd manifest_set1_init.mp4 segment_Audio_.mp4 encodedVideo/")
	os.system ("mv *360p*.m4s encodedVideo/360p/")
	os.system ("mv *480p*.m4s encodedVideo/480p/")
	os.system ("mv *720p*.m4s encodedVideo/720p/")
	os.system ("mv *1080p*.m4s encodedVideo/1080p/")
	os.system ("mv *Audio*.m4s encodedVideo/Audio/")

	with open('encodedVideo/manifest.mpd', 'r') as MPDfile:
		fileData = MPDfile.read()

	fileData = fileData.replace('segment_360', '360p/segment_360')
	fileData = fileData.replace('segment_480', '480p/segment_480')
	fileData = fileData.replace('segment_720', '720p/segment_720')
	fileData = fileData.replace('segment_Audio', 'Audio/segment_Audio')

	if (bAud != -1.0 and bAr != -1.0 and bAc != -1.0):
		os.system ("rm *.m4a *.mp4")
		fileData = fileData.replace('segment_1080', '1080p/segment_1080')

	else:
		os.system ("rm *.m4a *.mp4")

	with open('encodedVideo/manifest.mpd', 'w') as MPDfile:
		MPDfile.write(fileData)

def main ():

	parser = argparse.ArgumentParser()

	parser.add_argument("-v", "--video", help="The video that will be encoded (in MP4 format)")
	parser.add_argument("-fps", "--fps", help="The desired video FPS")
	parser.add_argument("-segLen", "--segLen", help="DASH segment length")

	parser.add_argument("-b360", "--b360", help="Video bitrate (in Mbps) for 360p")
	parser.add_argument("-b480", "--b480", help="Video bitrate (in Mbps) for 480p")
	parser.add_argument("-b720", "--b720", help="Video bitrate (in Mbps) for 720p")
	parser.add_argument("-b1080", "--b1080", help="Video bitrate (in Mbps) for 1080p")

	parser.add_argument("-bAud", "--bAud", help="Audio bit rate (in kbps)", nargs='?')
	parser.add_argument("-bAr", "--bAr", help="Audio sample rate (in kHz)", nargs='?')
	parser.add_argument("-bAc", "--bAc", help="Number of audio channels", nargs='?')

	args = parser.parse_args()

	if (args.bAud and args.bAr and args.bAc):
		createChunks (args.video, args.fps, args.segLen, float(args.b360), float(args.b480), float(args.b720), float(args.b1080), float(args.bAud), float(args.bAr), float(args.bAc))

	else:
		createChunks (args.video, args.fps, args.segLen, float(args.b360), float(args.b480), float(args.b720), float(args.b1080), -1.0, -1.0, -1.0)

if __name__ == '__main__':
	main()