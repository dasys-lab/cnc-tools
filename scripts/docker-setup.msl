#!/bin/sh

set -e

# vars
step_count=8
current_step=0
root_taskfile=.root_done
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

taskdir=$HOME/.msl_tasks
mark_done() {
	touch $taskdir/$1
}

is_done() {
	test -f $taskdir/$1
}

# $1 = task function, $2,$3,... = task description
do_task() {
	func="$1"
	task_file="t_${func}"
	shift 1
	desc="$*"
	step "$desc"

	if ! is_done "${task_file}" ; then
		$func && mark_done "${task_file}"
	else
		msg "Already done!"
	fi
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

# This portion of the script has to be run as root
run_tasks() {
	do_task ros_setup "Setup ros dependency"
	do_task install_packages "Install ros and development packages"
	do_task rosdep_init "Running: rosdep init"
    
    do_task rosdep_update "Running: rosdep update"
	do_task init_workspace "Initializing ros workspace at ${workspace_path}"
    
	do_task setup_bashrc "Configure ~/.bashrc for you"
}

# "main"

# Check for root permissions.
# The if condition makes sure root_tasks and user_tasks run with the
# right privileges.
if [ "$(id -u)" -ne 0 ] ; then
	# Second entry
	[ -f $root_taskfile ] || err "Must be run using sudo, exiting..."
else
	# First entry
	if [ -n "$1" ]
	then
		$1
		exit 0
	fi

	mkdir -p $taskdir

	run_tasks

	touch $root_taskfile
	chown -R $SUDO_USER $taskdir
fi
