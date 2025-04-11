# OpenStreetTouch

A tool to extract geodata from openstreetmap and create suitable file for image2touch or DesktopBrailleRAP. The main goal is to extract openstreetmap data to build tangible maps.

In many cities, public transport map are not available in Braille nor in suitable format to build accessible description. Most of the needed data is available in [openstreetmap](https://www.openstreetmap.org/) in open database licence. OpenStreetTouch aim to extract these data to build accessible transport map.

Here is an example of Subway map of Amsterdam.
![OpenStreetTouch displaying subway lines in Amsterdam](./screenshot/amsterdamsubway.jpg)

An example of city map with ULB campus in Bruxelles.
![OpenStreetTouch displaying Bruxelles ULB campus map](./screenshot/ulbmap.jpg)

Here is an usage exemple with DesktopBrailleRAP on a residential area in France.
![DesktopBrailleRAP view translating a vector map in tangible map](./screenshot/petiteferme.jpg)

Another usage exemple with the Askoria campus in Rennes - France
![DesktopBrailleRAP view translating a vector map in tangible map](./screenshot/askoria.jpg)

Using a BrailleRAP to emboss cultural center access map at ![Tech Inn'Vitre](https://techinn.vitrecommunaute.bzh/)
![A BrailleRAP embossing a city map in France](./screenshot/brap_vitre.jpg)


## Features
- Build SVG map from public transport data. These SVG can then be use to build tangible map with a laser cutter, a 3d printer or a [BrailleRAP](https://github.com/braillerap/BrailleRap) with software like [image2touch](https://github.com/myhumankit/Image2Touch) or [DesktopBrailleRAP](https://github.com/braillerap/DesktopBrailleRAP).
- Extract ordered station name from public transport data.
- Extract small city map to help build accessible description of local area.

## Releases
We provide pre-built binaries for Windows, Debian 12, Ubuntu 24.04. See [releases](https://github.com/braillerap/OpenStreetTouch/releases) for more information.

OpenStreetTouch depends on glibc version. Unfortunately recent Debian and Ubuntu distribution are not using exactly the same. If your are using Debian 12 or a derivate distribution, use desktopbraillerap-debian. If you are using Ubuntu 24.04 or a derivate distribution, use desktopbraillerap-ubuntu

[![auto_build_for_ubuntu](https://github.com/braillerap/OpenStreetTouch/actions/workflows/auto_build_for_ubuntu.yml/badge.svg?event=release)](https://github.com/braillerap/OpenStreetTouch/actions/workflows/auto_build_for_ubuntu.yml)

[![auto_build_for_debian](https://github.com/braillerap/OpenStreetTouch/actions/workflows/auto_build_for_debian.yml/badge.svg?event=release)](https://github.com/braillerap/OpenStreetTouch/actions/workflows/auto_build_for_debian.yml)

## User manual
The user manual is available [https://openstreettouch.readthedocs.io/en/main/](https://openstreettouch.readthedocs.io/en/main/)

**en** [![Documentation Status](https://readthedocs.org/projects/openstreettouch_en/badge/?version=main&style=plastic)](https://openstreettouch.readthedocs.io/en/main/)

**fr** [![Documentation Status](https://readthedocs.org/projects/openstreettouch/badge/?version=main&style=plastic)](https://openstreettouch.readthedocs.io/fr/main/)


## Contributing

### Translation
If you need the software in your locale language, we will be happy to add a new translation. Translation files will be hosted on codeberg community translation platform and can be updated by anyone [weblate host on codeberg] for more information.


### Code and features
Feel free to open issues or pull requests ! We will be happy to review and merge your changes. BTW we have a great focus on accessibility and user friendly design.

## Translations status

</a>
<a href="https://translate.codeberg.org/engage/openstreettouch/">
<img src="https://translate.codeberg.org/widget/openstreettouch/ihm/multi-green.svg" alt="Translation status" width="75%"/>
</a>

## Funding

This project is funded through [NGI0 Entrust](https://nlnet.nl/entrust), a fund established by [NLnet](https://nlnet.nl) with financial support from the European Commission's [Next Generation Internet](https://ngi.eu) program. Learn more at the [NLnet project page](https://nlnet.nl/project/BrailleRAP).

[<img src="https://nlnet.nl/logo/banner.png" alt="NLnet foundation logo" width="20%" />](https://nlnet.nl)
[<img src="https://nlnet.nl/image/logos/NGI0_tag.svg" alt="NGI Zero Logo" width="20%" />](https://nlnet.nl/entrust)


# Building on Windows

## Prerequisites

* Python 3.6 or later
* NodeJS 20.12 or later

## Create a python virtual environment

```
python -m venv venv
```

## Activate python virtual environment

```
.\venv\Scripts\activate
```

## Install python dependencies

```
pip install -r requirements.txt
```

## Install nodejs dependencies

```
npm install
```

## Run in dev environement

```
npm run startview
```

## Build windows .exe

```
npm run buildview
```
check OpenStreetTouch.exe in dist folder


# Building on Linux (Debian)

## Prerequisites
We need several development tools to build OpenStreetTouch, python, nodejs and gcc to build some python dependencies.
Depending on your system, you will also need a desktop environment installed on the build machine.


### Python / gcc / nodejs

General build tools:

    
    apt install  -y cmake build-essential git 
    apt install  -y ninja-build
    apt install  -y autoconf gnulib

    apt install  -y ca-certificates curl gnupg
    apt install  -y software-properties-common

    apt install  -y gnome-core
    apt install  -y python3 python3-venv python3-dev
    apt install  -y pkg-config 
    apt install  -y gir1.2-gtk-3.0 gir1.2-webkit2-4.1
    apt install  -y python3-tk 

    
    apt install  -y libcairo2 libcairo2-dev libgirepository1.0-dev
    apt install  -y tcl tree
    apt install  -y git-extras lintian

Nodejs:

General Nodejs
    
    curl -sL https://deb.nodesource.com/setup_20.x | bash -
    apt update
    apt install -y nodejs
    npm i npm@latest -g

Install OpenStreetTouch nodejs dependencies

    npm install

Python:

Create a python3 virtual environment

    python3 -m venv venv

Activate python3 virtual environment

    source ./venv/bin/activate

Install python3 OpenStreetTouch dependencies

    pip install -r requirement_linux.txt

## Build OpenStreetTouch

Activate python virtual env 

    source ./venv/bin/activate

### Run in development environement

    npm run startview

### Build OpenStreetTouch

    npm run builddebian

Check the ./dist folder for the openstreettouch-debian executable. You can install the .deb package with:

    sudo dpkg -i openstreettouch-debian-x.x.x.deb



# Building on Linux (Ubuntu)

## Prerequisites
We need several development tools to build OpenStreetTouch, python, nodejs and gcc to build some python dependencies.
Depending on your system, you will also need a desktop environment installed on the build machine.


### Python / gcc / nodejs

General build tools:

    
    apt install  -y cmake build-essential git ninja-build autoconf gnulib
    apt install  -y libyaml-dev texinfo texlive
    apt install  -y ca-certificates curl gnupg
    apt install  -y software-properties-common
    apt install  -y ubuntu-desktop-minimal 
    apt install  -y python3 python3-venv python3-dev
    apt install  -y pkg-config 
    apt install  -y gir1.2-gtk-3.0 gir1.2-webkit2-4.1
    apt install  -y python3-tk 
    apt install  -y libcairo2 libcairo2-dev libgirepository1.0-dev
    apt install  -y tcl tree
    apt install  -y git-extras lintian

Nodejs:

General Nodejs
    
    curl -sL https://deb.nodesource.com/setup_20.x | bash -
    apt update
    apt install -y nodejs
    npm i npm@latest -g

Install OpenStreetTouch nodejs dependencies

    npm install

Python:

Create a python3 virtual environment

    python3 -m venv venv

Activate python3 virtual environment

    source ./venv/bin/activate

Install python3 OpenStreetTouch dependencies

    pip install -r requirement_linux.txt

## Build OpenStreetTouch

Activate python virtual env 

    source ./venv/bin/activate

### Run in development environement

    npm run startview

### Build OpenStreetTouch

    npm run buildubuntu

Check the ./dist folder for the openstreettouch-ubuntu executable. You can install the .deb package with:

    sudo dpkg -i openstreettouch-ubuntu-x.x.x.deb


# Building for Linux using Docker

You can use Docker configuration to build OpenStreetTouch for a Linux distribution. 

Docker configuration to build OpenStreetTouch for Debian or Ubuntu are available here:

[Debian](https://github.com/braillerap/BuildOpenStreetTouchDebian)

[Ubuntu](https://github.com/braillerap/BuildOpenStreetTouchUbuntu)
