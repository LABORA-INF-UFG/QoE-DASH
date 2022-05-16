import os
import re
import csv
import argparse

def moviesInCache (cachefile):

	cacheMovies = []

	with open (cachefile, newline = '') as caches:

		reader = csv.reader(caches)

		for line in reader:

			line = ''.join(line)
			cache = line.split("#", 1)

			cacheMovies.append(cache)

	return cacheMovies

def generateConciseMPD (datasetLocation):

	originalMPD = datasetLocation + "/manifest.mpd"

	with open (originalMPD, 'r') as orgMPD:
		originalMPD = orgMPD.read()

	#Line 3
	minBufferTime = re.search('minBufferTime="([^"]*)"', originalMPD).group(1)
	mediaPresentationDuration = re.search('mediaPresentationDuration="([^"]*)"', originalMPD).group(1)
	maxSegmentDuration = re.search('maxSegmentDuration="([^"]*)"', originalMPD).group(1)
	#Line 9
	duration = re.search('Period duration="([^"]*)"', originalMPD).group(1)
	#Line 11
	maxFrameRate = re.search('maxFrameRate="([^"]*)"', originalMPD).group(1)
	#Line 15
	codecs360 = re.search('id="360p" mimeType="video/mp4" codecs="([^"]*)"', originalMPD).group(1)
	frameRate360 = re.search('id="360p" mimeType="video/mp4" codecs="{}" width="640" height="360" frameRate="([^"]*)"'.format(codecs360), originalMPD).group(1)
	sar360 = re.search('id="360p" mimeType="video/mp4" codecs="{}" width="640" height="360" frameRate="{}" sar="([^"]*)"'.format(codecs360, frameRate360), originalMPD).group(1)
	bandwidth360 = re.search('id="360p" mimeType="video/mp4" codecs="{}" width="640" height="360" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="([^"]*)"'.format(codecs360, frameRate360, sar360), originalMPD).group(1)
	#Line 17
	timescale360 = re.search('<Representation id="360p" mimeType="video/mp4" codecs="{}" width="640" height="360" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="{}">\n    <SegmentList timescale="([^"]*)"'.format(codecs360, frameRate360, sar360, bandwidth360), originalMPD).group(1)
	duration360 = re.search('<Representation id="360p" mimeType="video/mp4" codecs="{}" width="640" height="360" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="{}">\n    <SegmentList timescale="{}" duration="([^"]*)"'.format(codecs360, frameRate360, sar360, bandwidth360, timescale360), originalMPD).group(1)
	#Line 21
	codecs480 = re.search('id="480p" mimeType="video/mp4" codecs="([^"]*)"', originalMPD).group(1)
	frameRate480 = re.search('id="480p" mimeType="video/mp4" codecs="{}" width="854" height="480" frameRate="([^"]*)"'.format(codecs480), originalMPD).group(1)
	sar480 = re.search('id="480p" mimeType="video/mp4" codecs="{}" width="854" height="480" frameRate="{}" sar="([^"]*)"'.format(codecs480, frameRate480), originalMPD).group(1)
	bandwidth480 = re.search('id="480p" mimeType="video/mp4" codecs="{}" width="854" height="480" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="([^"]*)"'.format(codecs480, frameRate480, sar480), originalMPD).group(1)
	#Line 23
	timescale480 = re.search('<Representation id="480p" mimeType="video/mp4" codecs="{}" width="854" height="480" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="{}">\n    <SegmentList timescale="([^"]*)"'.format(codecs480, frameRate480, sar480, bandwidth480), originalMPD).group(1)
	duration480 = re.search('<Representation id="480p" mimeType="video/mp4" codecs="{}" width="854" height="480" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="{}">\n    <SegmentList timescale="{}" duration="([^"]*)"'.format(codecs480, frameRate480, sar480, bandwidth480, timescale480), originalMPD).group(1)
	#Line 27
	codecs720 = re.search('id="720p" mimeType="video/mp4" codecs="([^"]*)"', originalMPD).group(1)
	frameRate720 = re.search('id="720p" mimeType="video/mp4" codecs="{}" width="1280" height="720" frameRate="([^"]*)"'.format(codecs720), originalMPD).group(1)
	sar720 = re.search('id="720p" mimeType="video/mp4" codecs="{}" width="1280" height="720" frameRate="{}" sar="([^"]*)"'.format(codecs720, frameRate720), originalMPD).group(1)
	bandwidth720 = re.search('id="720p" mimeType="video/mp4" codecs="{}" width="1280" height="720" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="([^"]*)"'.format(codecs720, frameRate720, sar720), originalMPD).group(1)
	#Line 29
	timescale720 = re.search('<Representation id="720p" mimeType="video/mp4" codecs="{}" width="1280" height="720" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="{}">\n    <SegmentList timescale="([^"]*)"'.format(codecs720, frameRate720, sar720, bandwidth720), originalMPD).group(1)
	duration720 = re.search('<Representation id="720p" mimeType="video/mp4" codecs="{}" width="1280" height="720" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="{}">\n    <SegmentList timescale="{}" duration="([^"]*)"'.format(codecs720, frameRate720, sar720, bandwidth720, timescale720), originalMPD).group(1)
	#Line 33
	codecs1080 = re.search('id="1080p" mimeType="video/mp4" codecs="([^"]*)"', originalMPD).group(1)
	frameRate1080 = re.search('id="1080p" mimeType="video/mp4" codecs="{}" width="1920" height="1080" frameRate="([^"]*)"'.format(codecs1080), originalMPD).group(1)
	sar1080 = re.search('id="1080p" mimeType="video/mp4" codecs="{}" width="1920" height="1080" frameRate="{}" sar="([^"]*)"'.format(codecs1080, frameRate1080), originalMPD).group(1)
	bandwidth1080 = re.search('id="1080p" mimeType="video/mp4" codecs="{}" width="1920" height="1080" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="([^"]*)"'.format(codecs1080, frameRate1080, sar1080), originalMPD).group(1)
	#Line 35
	timescale1080 = re.search('<Representation id="1080p" mimeType="video/mp4" codecs="{}" width="1920" height="1080" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="{}">\n    <SegmentList timescale="([^"]*)"'.format(codecs1080, frameRate1080, sar1080, bandwidth1080), originalMPD).group(1)
	duration1080 = re.search('<Representation id="1080p" mimeType="video/mp4" codecs="{}" width="1920" height="1080" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="{}">\n    <SegmentList timescale="{}" duration="([^"]*)"'.format(codecs1080, frameRate1080, sar1080, bandwidth1080, timescale1080), originalMPD).group(1)
	#Line 45
	codecsAudio = re.search('audio/mp4" codecs="([^"]*)"', originalMPD).group(1)
	audioSamplingRate = re.search('audioSamplingRate="([^"]*)"', originalMPD).group(1)
	bandwidthAudio = re.search('audioSamplingRate="{}" startWithSAP="1" bandwidth="([^"]*)"'.format(audioSamplingRate), originalMPD).group(1)
	#Line 47
	valueAudio = re.search('configuration:2011" value="([^"]*)"', originalMPD).group(1)
	#Line 49
	timescaleAudio = re.search('configuration:2011" value="{}"/>\n    <SegmentList timescale="([^"]*)"'.format(valueAudio), originalMPD).group(1)
	durationAudio = re.search('configuration:2011" value="{}"/>\n    <SegmentList timescale="{}" duration="([^"]*)"'.format(valueAudio, timescaleAudio), originalMPD).group(1)
	
	with open ('../../InputFiles/basemanifest.mpd', 'r') as bseMPD:
		baseMPD = bseMPD.read()

	#minBufferTime
	tmpFinalMPD = baseMPD.split('minBufferTime="')
	finalMPD = tmpFinalMPD[0] + 'minBufferTime="' + minBufferTime + tmpFinalMPD[1]
	#mediaPresentationDuration
	tmpFinalMPD = finalMPD.split('mediaPresentationDuration="')
	finalMPD = tmpFinalMPD[0] + 'mediaPresentationDuration="' + mediaPresentationDuration + tmpFinalMPD[1]
	#maxSegmentDuration
	tmpFinalMPD = finalMPD.split('maxSegmentDuration="')
	finalMPD = tmpFinalMPD[0] + 'maxSegmentDuration="' + maxSegmentDuration + tmpFinalMPD[1]
	#duration
	tmpFinalMPD = finalMPD.split('Period duration="')
	finalMPD = tmpFinalMPD[0] + 'Period duration="' + duration + tmpFinalMPD[1]
	#maxFrameRate
	tmpFinalMPD = finalMPD.split('maxFrameRate="')
	finalMPD = tmpFinalMPD[0] + 'maxFrameRate="' + maxFrameRate + tmpFinalMPD[1]
	#codecs360
	tmpFinalMPD = finalMPD.split('id="360p" mimeType="video/mp4" codecs="')
	finalMPD = tmpFinalMPD[0] + 'id="360p" mimeType="video/mp4" codecs="' + codecs360 + tmpFinalMPD[1]
	#frameRate360
	tmpFinalMPD = finalMPD.split('id="360p" mimeType="video/mp4" codecs="{}" width="640" height="360" frameRate="'.format(codecs360))
	finalMPD = tmpFinalMPD[0] + 'id="360p" mimeType="video/mp4" codecs="{}" width="640" height="360" frameRate="'.format(codecs360) + frameRate360 + tmpFinalMPD[1]
	#sar360
	tmpFinalMPD = finalMPD.split('id="360p" mimeType="video/mp4" codecs="{}" width="640" height="360" frameRate="{}" sar="'.format(codecs360, frameRate360))
	finalMPD = tmpFinalMPD[0] + 'id="360p" mimeType="video/mp4" codecs="{}" width="640" height="360" frameRate="{}" sar="'.format(codecs360, frameRate360) + sar360 + tmpFinalMPD[1]
	#bandwidth360
	tmpFinalMPD = finalMPD.split('id="360p" mimeType="video/mp4" codecs="{}" width="640" height="360" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="'.format(codecs360, frameRate360, sar360))
	finalMPD = tmpFinalMPD[0] + 'id="360p" mimeType="video/mp4" codecs="{}" width="640" height="360" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="'.format(codecs360, frameRate360, sar360) + bandwidth360 + tmpFinalMPD[1]
	#duration360
	tmpFinalMPD = finalMPD.split('<Representation id="360p" mimeType="video/mp4" codecs="{}" width="640" height="360" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="{}">'.format(codecs360, frameRate360, sar360, bandwidth360) + 2*'\n' + '            <SegmentTemplate duration="')
	finalMPD = tmpFinalMPD[0] + '<Representation id="360p" mimeType="video/mp4" codecs="{}" width="640" height="360" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="{}">'.format(codecs360, frameRate360, sar360, bandwidth360) + 2*'\n' + '            <SegmentTemplate duration="' + duration360 + tmpFinalMPD[1]
	#timescale360
	tmpFinalMPD = finalMPD.split('segment_360p_$Number$.m4s" startNumber="1" timescale="')
	finalMPD = tmpFinalMPD[0] + 'segment_360p_$Number$.m4s" startNumber="1" timescale="' + timescale360 + tmpFinalMPD[1]
	#codecs480
	tmpFinalMPD = finalMPD.split('id="480p" mimeType="video/mp4" codecs="')
	finalMPD = tmpFinalMPD[0] + 'id="480p" mimeType="video/mp4" codecs="' + codecs480 + tmpFinalMPD[1]
	#frameRate480
	tmpFinalMPD = finalMPD.split('id="480p" mimeType="video/mp4" codecs="{}" width="854" height="480" frameRate="'.format(codecs480))
	finalMPD = tmpFinalMPD[0] + 'id="480p" mimeType="video/mp4" codecs="{}" width="854" height="480" frameRate="'.format(codecs480) + frameRate480 + tmpFinalMPD[1]
	#sar480
	tmpFinalMPD = finalMPD.split('id="480p" mimeType="video/mp4" codecs="{}" width="854" height="480" frameRate="{}" sar="'.format(codecs480, frameRate480))
	finalMPD = tmpFinalMPD[0] + 'id="480p" mimeType="video/mp4" codecs="{}" width="854" height="480" frameRate="{}" sar="'.format(codecs480, frameRate480) + sar480 + tmpFinalMPD[1]
	#bandwidth480
	tmpFinalMPD = finalMPD.split('id="480p" mimeType="video/mp4" codecs="{}" width="854" height="480" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="'.format(codecs480, frameRate480, sar480))
	finalMPD = tmpFinalMPD[0] + 'id="480p" mimeType="video/mp4" codecs="{}" width="854" height="480" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="'.format(codecs480, frameRate480, sar480) + bandwidth480 + tmpFinalMPD[1]
	#duration480
	tmpFinalMPD = finalMPD.split('<Representation id="480p" mimeType="video/mp4" codecs="{}" width="854" height="480" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="{}">'.format(codecs480, frameRate480, sar480, bandwidth480) + 2*'\n' + '            <SegmentTemplate duration="')
	finalMPD = tmpFinalMPD[0] + '<Representation id="480p" mimeType="video/mp4" codecs="{}" width="854" height="480" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="{}">'.format(codecs480, frameRate480, sar480, bandwidth480) + 2*'\n' + '            <SegmentTemplate duration="' + duration480 + tmpFinalMPD[1]
	#timescale480
	tmpFinalMPD = finalMPD.split('segment_480p_$Number$.m4s" startNumber="1" timescale="')
	finalMPD = tmpFinalMPD[0] + 'segment_480p_$Number$.m4s" startNumber="1" timescale="' + timescale480 + tmpFinalMPD[1]
	#codecs720
	tmpFinalMPD = finalMPD.split('id="720p" mimeType="video/mp4" codecs="')
	finalMPD = tmpFinalMPD[0] + 'id="720p" mimeType="video/mp4" codecs="' + codecs720 + tmpFinalMPD[1]
	#frameRate720
	tmpFinalMPD = finalMPD.split('id="720p" mimeType="video/mp4" codecs="{}" width="1280" height="720" frameRate="'.format(codecs720))
	finalMPD = tmpFinalMPD[0] + 'id="720p" mimeType="video/mp4" codecs="{}" width="1280" height="720" frameRate="'.format(codecs720) + frameRate720 + tmpFinalMPD[1]
	#sar720
	tmpFinalMPD = finalMPD.split('id="720p" mimeType="video/mp4" codecs="{}" width="1280" height="720" frameRate="{}" sar="'.format(codecs720, frameRate720))
	finalMPD = tmpFinalMPD[0] + 'id="720p" mimeType="video/mp4" codecs="{}" width="1280" height="720" frameRate="{}" sar="'.format(codecs720, frameRate720) + sar720 + tmpFinalMPD[1]
	#bandwidth720
	tmpFinalMPD = finalMPD.split('id="720p" mimeType="video/mp4" codecs="{}" width="1280" height="720" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="'.format(codecs720, frameRate720, sar720))
	finalMPD = tmpFinalMPD[0] + 'id="720p" mimeType="video/mp4" codecs="{}" width="1280" height="720" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="'.format(codecs720, frameRate720, sar720) + bandwidth720 + tmpFinalMPD[1]
	#duration720
	tmpFinalMPD = finalMPD.split('<Representation id="720p" mimeType="video/mp4" codecs="{}" width="1280" height="720" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="{}">'.format(codecs720, frameRate720, sar720, bandwidth720) + 2*'\n' + '            <SegmentTemplate duration="')
	finalMPD = tmpFinalMPD[0] + '<Representation id="720p" mimeType="video/mp4" codecs="{}" width="1280" height="720" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="{}">'.format(codecs720, frameRate720, sar720, bandwidth720) + 2*'\n' + '            <SegmentTemplate duration="' + duration720 + tmpFinalMPD[1]
	#timescale720
	tmpFinalMPD = finalMPD.split('segment_720p_$Number$.m4s" startNumber="1" timescale="')
	finalMPD = tmpFinalMPD[0] + 'segment_720p_$Number$.m4s" startNumber="1" timescale="' + timescale720 + tmpFinalMPD[1]
	#codecs1080
	tmpFinalMPD = finalMPD.split('id="1080p" mimeType="video/mp4" codecs="')
	finalMPD = tmpFinalMPD[0] + 'id="1080p" mimeType="video/mp4" codecs="' + codecs1080 + tmpFinalMPD[1]
	#frameRate1080
	tmpFinalMPD = finalMPD.split('id="1080p" mimeType="video/mp4" codecs="{}" width="1920" height="1080" frameRate="'.format(codecs1080))
	finalMPD = tmpFinalMPD[0] + 'id="1080p" mimeType="video/mp4" codecs="{}" width="1920" height="1080" frameRate="'.format(codecs1080) + frameRate1080 + tmpFinalMPD[1]
	#sar1080
	tmpFinalMPD = finalMPD.split('id="1080p" mimeType="video/mp4" codecs="{}" width="1920" height="1080" frameRate="{}" sar="'.format(codecs1080, frameRate1080))
	finalMPD = tmpFinalMPD[0] + 'id="1080p" mimeType="video/mp4" codecs="{}" width="1920" height="1080" frameRate="{}" sar="'.format(codecs1080, frameRate1080) + sar1080 + tmpFinalMPD[1]
	#bandwidth1080
	tmpFinalMPD = finalMPD.split('id="1080p" mimeType="video/mp4" codecs="{}" width="1920" height="1080" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="'.format(codecs1080, frameRate1080, sar1080))
	finalMPD = tmpFinalMPD[0] + 'id="1080p" mimeType="video/mp4" codecs="{}" width="1920" height="1080" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="'.format(codecs1080, frameRate1080, sar1080) + bandwidth1080 + tmpFinalMPD[1]
	#duration1080
	tmpFinalMPD = finalMPD.split('<Representation id="1080p" mimeType="video/mp4" codecs="{}" width="1920" height="1080" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="{}">'.format(codecs1080, frameRate1080, sar1080, bandwidth1080) + 2*'\n' + '            <SegmentTemplate duration="')
	finalMPD = tmpFinalMPD[0] + '<Representation id="1080p" mimeType="video/mp4" codecs="{}" width="1920" height="1080" frameRate="{}" sar="{}" startWithSAP="1" bandwidth="{}">'.format(codecs1080, frameRate1080, sar1080, bandwidth1080) + 2*'\n' + '            <SegmentTemplate duration="' + duration1080 + tmpFinalMPD[1]
	#timescale1080
	tmpFinalMPD = finalMPD.split('segment_1080p_$Number$.m4s" startNumber="1" timescale="')
	finalMPD = tmpFinalMPD[0] + 'segment_1080p_$Number$.m4s" startNumber="1" timescale="' + timescale1080 + tmpFinalMPD[1]
	#codecsAudio
	tmpFinalMPD = finalMPD.split('audio/mp4" codecs="')
	finalMPD = tmpFinalMPD[0] + 'audio/mp4" codecs="' + codecsAudio + tmpFinalMPD[1]
	#audioSamplingRate
	tmpFinalMPD = finalMPD.split('audioSamplingRate="')
	finalMPD = tmpFinalMPD[0] + 'audioSamplingRate="' + audioSamplingRate + tmpFinalMPD[1]
	#bandwidthAudio
	tmpFinalMPD = finalMPD.split('audioSamplingRate="{}" startWithSAP="1" bandwidth="'.format(audioSamplingRate))
	finalMPD = tmpFinalMPD[0] + 'audioSamplingRate="{}" startWithSAP="1" bandwidth="'.format(audioSamplingRate) + bandwidthAudio + tmpFinalMPD[1]
	#valueAudio
	tmpFinalMPD = finalMPD.split('configuration:2011" value="')
	finalMPD = tmpFinalMPD[0] + 'configuration:2011" value="' + valueAudio + tmpFinalMPD[1]
	#durationAudio
	tmpFinalMPD = finalMPD.split('configuration:2011" value="{}"/>'.format(valueAudio) + 2*'\n' + '            <SegmentTemplate duration="')
	finalMPD = tmpFinalMPD[0] + 'configuration:2011" value="{}"/>'.format(valueAudio) + 2*'\n' + '            <SegmentTemplate duration="' + durationAudio + tmpFinalMPD[1]
	#timescaleAudio
	tmpFinalMPD = finalMPD.split('Audio_$Number$.m4s" startNumber="1" timescale="')
	finalMPD = tmpFinalMPD[0] + 'Audio_$Number$.m4s" startNumber="1" timescale="' + timescaleAudio + tmpFinalMPD[1]

	fManifest = open("conciseManifest.mpd", "w")
	fManifest.write(finalMPD)
	fManifest.close()

	os.system ("mv conciseManifest.mpd ../../InputFiles")

def generateMPD (cachefile, datasetLocation):

	generateConciseMPD (datasetLocation)

	cacheMovies = moviesInCache (cachefile)

	for index in range (len (cacheMovies)):
		
		with open ('../../InputFiles/conciseManifest.mpd', 'r') as baseMPD:
			fileData = baseMPD.read()

		if (int(cacheMovies[index][1]) == 1):
			fileData = fileData.replace('http://10.16.0.2/360p/', 'http://10.16.0.3/360p/')

		elif (int(cacheMovies[index][1]) == 2):
			fileData = fileData.replace('http://10.16.0.2/480p/', 'http://10.16.0.3/480p/')

		elif (int(cacheMovies[index][1]) == 3):
			fileData = fileData.replace('http://10.16.0.2/720p/', 'http://10.16.0.3/720p/')

		elif (int(cacheMovies[index][1]) == 4):
			fileData = fileData.replace('http://10.16.0.2/1080p/', 'http://10.16.0.3/1080p/')

		cacheMovieName = "manifestMovie{}.mpd".format(int(cacheMovies[index][0]))

		with open (cacheMovieName, 'w') as MPDfile:
			MPDfile.write(fileData)

	cacheMoviespath = '../../InputFiles/cacheMovies'

	if (not os.path.isdir(cacheMoviespath)):
		os.system ("mkdir ../../InputFiles/cacheMovies")

	os.system ("mv *.mpd ../../InputFiles/cacheMovies")

def main ():

	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--cache", help="The cache description in CSV")
	parser.add_argument("-l", "--datasetLocation", help="he location of the video encoded by 'Video enconding'")
	args = parser.parse_args()

	generateMPD (args.cache, args.datasetLocation)

if __name__ == '__main__':
	main()