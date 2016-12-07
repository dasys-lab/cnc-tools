#!/usr/bin/env python3

import argparse
import os
from subprocess import call
import utils

CWD = os.getcwd()
DIR = os.path.dirname(os.path.realpath(__file__))

def setup(args):

	selections = [
		(('/scripts/msl-setup.sh', "MSL Dev PC"), "MSL Dev PC"),
		(('/scripts/ttb-setup.sh', "Turtlebot PC"), "Turtlebot PC")
	]

	selected = utils.showSelection("What do you want to setup?", selections)

	if(utils.prompt("Do you really want to start the {} setup?".format(selected[1]))):
		call(['sudo', DIR + selected[0]])


def eclipse(args):
	eargs = [DIR + '/scripts/eclipse.sh']
	eargs.extend(args)
	call(eargs)

def repos(args):
	repos = utils.getGithubRepos("CarpeNoctem")

	# show selection
	entries = list(map(lambda x: (x, x['name']), repos))
	selected = utils.showMultiSelection(u'GitHub Repositories', entries, selectedLabels = ["alica", "alica-plan-designer", "cnc-msl", "supplementary", "msl_gazebo_simulator"])

	for repo in selected:
		print(repo['ssh_url'])


tools = {
	'setup': setup,
	'eclipse': eclipse,
	'repos': repos
}

# Main Script

parser = argparse.ArgumentParser(description="Tools that help us getting boring stuff done.")
parser.add_argument('tool', choices=tools.keys(), type=str, help="the name of the tool")
parser.add_argument('args', nargs=argparse.REMAINDER, type=str, help="args for the tool, see <tool> -h")

args = parser.parse_args()

# run tool
if args.tool in tools:
	tools[args.tool](args.args)
