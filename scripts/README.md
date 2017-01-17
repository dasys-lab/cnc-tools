cnc-setup
=========

scripts to install [ROS](http://www.ros.org/) Kinetic and domain specific repositories of [carpe-noctem-cassel](https://github.com/carpe-noctem-cassel/cnc-msl)

Scripts
-------

### msl-setup.sh

This script installs ROS Kinetic on Ubuntu 16.04 and clones all repositories needed
for [MSL](https://en.wikipedia.org/wiki/RoboCup_Middle_Size_League).

Usage:
 
	$ sudo ./msl-setup.sh

### ttb-setup.sh

Just like the script above, this script installs ROS Kinetic.
Instead of cloning all repositories for MSL it clones all repositories
to work with the [TurtleBot 2](http://www.turtlebot.com/).

Usage:
 
	$ sudo ./ttb-setup.sh

Notes/Issues
------------

It is highly recommended to update your system before running the script
by `sudo apt-get update && sudo apt-get upgrade`.

The script won't build the workspace because you might want to call catkin
with parameters for your ide(e.g. eclipse).

License
-------

ROS Kinetic and other software products used and listed in the script have
their respective licenses.

The scripts and this note itself is licensed under the MIT License.
