# QoE-DASH: DASH QoE Performance EvaluationTool for Edge-Cache and Recommendation

QoE-DASH was tested in Ubuntu 20.04 LTS and Ubuntu Server 20.04 LTS. Although it may work in some other Debian-based Linux distributions, we do not guarantee that all features will work well.

- [Getting started](#getting-started)
	- [Installing the prerequisites](#installing-the-prerequisites)
	- [Cloning the repository](#cloning-the-repository)
	- [QoE-DASH architecture](#QoE-DASH-architecture)
- [Data set generation](#dataset-generation)
	- [Topology generator](#topology-generator)
	- [Manifest generator](#manifest-generator)
	- [Video enconding](#video-enconding)
- [Emulation](#emulation)
	- [Infrastructure manager](#infrastructure-manager)
	- [Video stream emulator](#video-stream-emulator)
- [Destroying an emulated infrastructure](#destroying-an-emulated-infrastructure)
- [Contact us](#contact-us)

## Getting started

These instructions will guide you to get QoE-DASH up and running.

### Installing the prerequisites

```
sudo apt update
sudo apt install python3 python3-pip ffmpeg gpac openvswitch-switch wondershaper git
sudo pip3 install argparse
```

It is also necessary to install [Docker](https://docs.docker.com/), please refer to the official Docker documentation on [how to install it](https://docs.docker.com/engine/install/ubuntu/).

### Cloning the repository

```
git clone https://github.com/LABORA-INF-UFG/QoE-DASH
```

### QoE-DASH architecture

The QoE-DASH architecture is divided into two modules and five sub-modules, as depicted in the figure below. Each module
and sub-module is detailed below.

<div align="center">
<img src="Figures/Architecture.svg">
</div>

## Data set generation

Data set generation is the module responsible for generating all data needed to emulate a DASH streaming service in QoE-DASH. We design this module using three sub-modules.

### Topology generator

### Manifest generator

### Video enconding

## Emulation

Emulation is a module responsible for the video emulation itself. This module comprises two main components: Infrastructure manager and Video stream emulator.

### Infrastructure manager

### Video stream emulator

## Destroying an emulated infrastructure

## Contact us

If you would like to contact us to contribute to this project, ask questions or suggest improvements, feel free to e-mail us at: qoedash@gmail.com