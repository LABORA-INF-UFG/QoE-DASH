# QoE-DASH: DASH QoE Performance Evaluation Tool for Edge-Cache and Recommendation

QoE-DASH was tested in Ubuntu 20.04 LTS and Ubuntu Server 20.04 LTS. Although it may work in some other Debian-based Linux distributions, we do not guarantee that all features will work well.

- [Getting started](#getting-started)
	- [Installing the prerequisites](#installing-the-prerequisites)
	- [Cloning the repository](#cloning-the-repository)
	- [QoE-DASH architecture](#QoE-DASH-architecture)
	- [QoE-DASH workflow](#QoE-DASH-workflow)
- [Data set generation](#dataset-generation)
	- [Topology generator](#topology-generator)
	- [Video enconding](#video-enconding)
		- [IEEE ICC paper data set](#IEEE-ICC-paper-data-set)
	- [Manifest generator](#manifest-generator)
- [Contact us](#contact-us)

## Getting started

These instructions will guide you to get QoE-DASH up and running.

### Installing the prerequisites

```
sudo apt update
sudo apt install python3 python3-pip ffmpeg gpac openvswitch-switch git curl unzip
pip3 install argparse gdown
```

It is also necessary to install **[Docker](https://docs.docker.com/)**, please refer to the official Docker documentation on [how to install it](https://docs.docker.com/engine/install/ubuntu/).

### Cloning the repository

```
git clone https://github.com/LABORA-INF-UFG/QoE-DASH.git
```

### QoE-DASH architecture

The QoE-DASH architecture is divided into two modules and five sub-modules, as depicted in the figure below. Each module
and sub-module is detailed below.

<div align="center">
<img src="Figures/Architecture.jpg" width="85%" height="85%">
</div>

### QoE-DASH workflow

The QoE-DASH workflow is organized as follows. Solid arrows represent mandatory flow; dashed arrows represent optional flow; rectangles identify the system modules, and ellipses represent input and output files.

<div align="center">
<img src="Figures/Workflow.jpg" width="85%" height="85%">
</div>

## Data set generation

Data set generation is the module responsible for generating all data needed to emulate a DASH streaming service in QoE-DASH. We design this module using three sub-modules.

### Topology generator

This sub-module generates the topology for QoE-DASH (steps 1a and 2a in [QoE-DASH workflow](#QoE-DASH-workflow)). The Topology generator is at [Scripts/DatasetGeneration/](Scripts/DatasetGeneration/).

You can run the Topology generator by running the following script combined with the arguments:

```
python3 topologyGenerator.py -tpd topologyDescription -ilc internetLinkCapacity
```

Where:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -tpd (file) – The topology description in CSV.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -ilc (float) – The internet link capacity.

Here is an example:

```
python3 topologyGenerator.py -tpd ../../InputFiles/topologyDescription.csv -ilc 100
```

The topology description file details the number of users in the emulation, the wireless link capacity, the maximum screen resolution for each User Equipment (UE), and the connection between each UE and each base station (BS).

One example of this file is 'topologyDescription.csv', which is located at [InputFiles/](InputFiles/), the file is structured as follows: userID#userCQI#screnRes#bsAsc, where:

* **userID** – An ID for each user.
* **userCQI** – The UE CQI. We consider the CQI to bandwidth conversion proposed in this [paper](https://doi.org/10.1109/TVT.2018.2889196) on Table I.
* **screnRes** – An integer from 1 to 4 that defines the screen resolution of the UE, where:
	* {1: 360p, 2: 480p, 3: 720p, 4: 1080p}.
* **bsAsc** – The BS to which the UE is connected.

This module also gives the flexibity of defining the Internet link capacity. This capacity  is represented as a value varying from 0% to 99% bottleneck compared to the sum of the BS capacities. For example:

If the sum of the BSs capacities is 1000 Mbps, and 'ilc' is defined as 70, the internet link capacity will be 700 Mbps.

Once you run the Topology generator, a file named 'topology.json' will be generated describing the topology for QoE-DASH. An example of this file, 'topology.json', is located at [InputFiles/](InputFiles/).

### Video enconding

This sub-module provides the user the flexibility of generating different representations for a given content (steps 1d and 2d in [QoE-DASH workflow](#QoE-DASH-workflow)). The Video enconding sub-module provides the user a plethora of options, such as defining the Frames Per Second (FPS) for the representations, the bit rate for each resolution (e.g., 360p, 480p, 720p, and 1080p) and the audio bit rate, sample rate, and number of channels.

You can run the Video encoding sub-module by running the following script combined with the arguments:

```
python3 videoEncoding.py -v Video.mp4 -fps FPS -segLen X -b360 Y -b480 Z -b720 K -b1080 L -bAud M -bAr N -bAc O
```

Where:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -v (file) – The video that will be encoded (in MP4 format).\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -fps (int) – The desired video FPS.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -segLen (float) – DASH segment length (in seconds).\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -b360 (float) – Video bitrate (in Mbps) for 360p.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -b480 (float) – Video bitrate (in Mbps) for 480p.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -b720 (float) – Video bitrate (in Mbps) for 720p.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -b1080 (float) – Video bitrate (in Mbps) for 1080p.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -bAud (float) – Audio bit rate (in kbps).\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -bAr (float) – Audio sample rate (in kHz).\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -bAc (float) – Number of audio channels.

Here is an example:

```
python3 videoEncoding.py -v ../../InputFiles/videoExample.mp4 -fps 48 -segLen 4 -b360 1.5 -b480 4 -b720 7.5 -b1080 12 -bAud 384 -bAr 48 -bAc 2
```

Once the video is encoded, a directory called "encodedVideo" will be created and this directory will contain the video encoded accordingly to your arguments.

#### IEEE ICC paper data set

The data set we generated for the IEEE ICC 2022 paper is publicly available. Due to the data set size, we divided it into four compressed files, each with four resolutions (360p, 480p, 720p, 1080p) and a different FPS (either 24 FPS, or 30 FPS, or 48 FPS or 60 FPS). If you prefer, you can also download the complete data set with all different resolutions and FPSs as well.

Please check the data set file size before downloading it:

<div align="center">

| Data set | File size |
|:--------:|:---------:|
|  24 FPS  |   14 GB   |
|  30 FPS  |   14 GB   |
|  48 FPS  |   22 GB   |
|  60 FPS  |   22 GB   |
|   Full   |   70 GB   |

</div>

In order to do download the data set you chose, first enter the [Scripts/IEEE-ICC-Dataset/](Scripts/IEEE-ICC-Dataset/) directory inside the repository you cloned, then run the script accordingly to your choice:

* **24 FPS**
```
python3 datasetDownloader.py -24
```

* **30 FPS**
```
python3 datasetDownloader.py -30
```

* **48 FPS**
```
python3 datasetDownloader.py -48
```

* **60 FPS**
```
python3 datasetDownloader.py -60
```

* **Full**
```
python3 datasetDownloader.py -full
```

This data set was generated using our [Video encoding](#video-enconding) sub-module. The video we used is on [YouTube](https://www.youtube.com/watch?v=zdZ97vxMfkE&ab_channel=GKorb).

We first downloaded the video, then we created a 2 hour version of the original video with [FFmpeg](https://video.stackexchange.com/questions/12905/repeat-loop-input-video-with-ffmpeg), and finally we used the [Video encoding](#video-enconding) sub-module to generate the data set.

### Manifest generator

This sub-module is responsible for the cache modeling in QoE-DASH (steps 1b and 2b in [QoE-DASH workflow](#QoE-DASH-workflow)). The Manifest generator receives a file, denoted Cache/cloud description, describing the video representations stored in the Cache and the ones stored in the Cloud. According to this description, for each video content, a manifest is created, associating each representation of this content to a location (Cache or Cloud). This association allows the player to know where to search for each representation of a given video content.

You can run the Manifest generator sub-module by running the following script combined with the arguments:

```
python3 manifestGenerator.py -c cacheDescription -d encodedVideoLocation
```

Where:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -c (file) – The cache description in CSV.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -l (string) – The location of the video encoded by 'Video enconding'.

Here is an example:

```
python3 manifestGenerator.py -c ../../InputFiles/moviesCache.csv -l ../../InputFiles/encodedVideo
```

The cache description file details the representations that are going to be stored in the Cache.

One example of this file is 'moviesCache.csv', which is located at [InputFiles/](InputFiles/), the file is structured as follows: movieID#representation, where:

* **movieID** – An ID for movie that you want a representation to be stored in the Cache.
* **representation** – An integer from 1 to 4 that defines the resolution of the movie that will be stored in the Cache, where:
	* {1: 360p, 2: 480p, 3: 720p, 4: 1080p}.

Once you run the Manifest generator, a new directory named 'cacheMovies' will be generated. This directory will contain a manifest for each representation defined on the cache description. In QoE-DASH, '10.16.0.2' is the Cloud IP, and '10.16.0.3' is the Cache IP. The representations on each manifest are located following the cache description.

An example of the output generated by the Manifest generator is located at [InputFiles/cacheMovies](InputFiles/cacheMovies).

### Contact us

If you would like to contact us to contribute to this project, ask questions or suggest improvements, feel free to e-mail us at: qoedash@gmail.com