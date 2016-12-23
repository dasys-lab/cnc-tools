#!/bin/sh

set -e

# vars
step_count=8
current_step=0
ubuntu_packages='git vim gitk meld bison re2c libode-dev gnuplot-qt libxv-dev libtbb-dev libcgal-demo libcgal-dev xsdcxx libxerces-c-dev freeglut3-dev libvtk5-dev libvtk5-qt4-dev libopencv-dev myrepos openjdk-8-jdk'
ubuntu_distro=xenial
ros_distro=kinetic
ros_packages="ros-${ros_distro}-desktop-full ros-${ros_distro}-qt-gui-core ros-${ros_distro}-qt-build ros-${ros_distro}-serial python-catkin-tools ros-${ros_distro}-mrpt-map python-catkin-tools"
workspace_path="$HOME/cnws"
workspace_src="${workspace_path}/src"
ros_setup_file="/opt/ros/${ros_distro}/setup.sh"
github_url='git@github.com:carpe-noctem-cassel/'
repos='alica alica-plan-designer supplementary cnc-msl msl_gazebo_simulator'

# functions
msg() {
	printf "\033[1m$@\n\033[m"
}

err() {
	msg "ERROR $@"
	exit 1
}

step() {
	current_step=$((current_step+1))
	msg "[${current_step}/${step_count}] $@"
}

append_unique() {
	f="$1"
	shift 1
	grep -q -F "$*" "$f" || echo "$*" >>"$f"
}

# tasks
ros_setup() {
	ros_repo_file="/etc/apt/sources.list.d/ros-latest.list"
	dep_string="deb http://packages.ros.org/ros/ubuntu ${ubuntu_distro} main"

	if [ ! -f $ros_repo_file ] ; then
		echo "$dep_string" >$ros_repo_file
	fi

	# add repo key
	apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 0xB01FA116
}

install_packages () {
	apt-get update
	apt-get -y install $ubuntu_packages
	# for some reason you can't install all packages at once?
	apt-get -y install $ros_packages
}

rosdep_init() {
	[ -f /etc/ros/rosdep/sources.list.d/20-default.list ] || rosdep init
}

rosdep_update() {
	rosdep update
	rosdep fix-permissions
}

init_workspace() {
	mkdir -p "${workspace_src}"

	if [ ! -f "${workspace_src}/CMakeLists.txt" ] ; then
		lpwd="$(pwd)"
		. $ros_setup_file
		cd "${workspace_src}"
		catkin_init_workspace
		cd "$lpwd"
	fi
}

append_bashrc() {
	append_unique ~/.bashrc "$*"
}

setup_bashrc() {
	# repo that contains domain specific configuration like etc
	etc_repo='cnc-msl'

	append_bashrc "source /opt/ros/${ros_distro}/setup.bash"
	append_bashrc "source ${workspace_path}/devel/setup.bash"

	append_bashrc "# The next two lines determine the application domain for ALICA (Team-Modelling software)"
	append_bashrc "export DOMAIN_FOLDER=\"${workspace_src}/${etc_repo}\""
	append_bashrc "export DOMAIN_CONFIG_FOLDER=\"${workspace_src}/${etc_repo}/etc\""
	
	append_bashrc "# Fancy prompt that also shows the current branch"
	append_bashrc "export PS1='\[\033[01;32m\]\u@\h\[\033[01;34m\] \w \[\033[01;31m\]\$(__git_ps1 \"[%s]\")\[\033[01;34m\]\$\[\033[00m\] '"

	# The only way to break a habit
	append_bashrc "alias catkin_make='catkin build'"
}

# "main"

# Check for root permissions.
# The if condition makes sure root_tasks and user_tasks run with the
# right privileges.
if [ "$(id -u)" -ne 0 ] ; then
	# Second entry
	err "Must be run using sudo, exiting..."
else
	echo "Setup ros dependency"
	ros_setup 
	
	echo "Install ros and development packages"
	install_packages
	
	echo "Running: rosdep init"
	rosdep_init 
    
    	echo "Running: rosdep update"
	rosdep_update 
	
	echo "Initializing ros workspace at ${workspace_path}"
	init_workspace 
    
    	echo "Configure ~/.bashrc for you"
	setup_bashrc
fi
