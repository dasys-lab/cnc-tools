#!/usr/bin/env python3

import argparse
import json
import os
from os import path
from collections import OrderedDict
import shutil
from subprocess import call

import utils

CONFIG_PATH = "~/.config/cnctools.json"

CWD = os.getcwd()
DIR = os.path.dirname(os.path.realpath(__file__))

def init(args):
	print("Configure...")

	keys = ['mslws', 'ttbws']

	for key in keys:
		initConfUpdate(key)

	print()
	print("New Config:")
	for key, value in CONFIG.items():
		print("{}: '{}'".format(key, value))
	print()

	if(utils.prompt("Save changes?", True)):
		saveConfig()
		print("Config saved.")

def initConfUpdate(key):
	if(key in CONFIG.keys()):
		if(utils.prompt("{}: {}    Change?".format(key, CONFIG[key]), False)):
			CONFIG[key] = input("{}: ".format(key))
	else:
		if(utils.prompt("{}: <not set>    Set?".format(key), True)):
			CONFIG[key] = input("{}: ".format(key))

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
	selections = [
		('mslws', "MSL Workspace"),
		('ttbws', "TurtleBot Workspace")
	]

	selected_ws = utils.showSelection("Repos of which workspace do you want to change?", selections)

	if not checkConfig(selected_ws):
		return

	repoFolders = os.listdir(path.join(os.path.expanduser(CONFIG[selected_ws]), "src"))


	remoteRepos = OrderedDict()

	ghRepos = utils.getGithubRepos("CarpeNoctem")
	for repo in ghRepos:
		remoteRepos[repo["name"]] = repo

	localRepos = dict(filter(lambda x: x[1]['name'] in repoFolders, remoteRepos.items()))

	# show selection
	entries = OrderedDict(map(lambda x: (x[0], x[1]['name']), remoteRepos.items()))

	selected_repos = utils.showMultiSelection(u'GitHub Repositories', entries, selectedKeys = localRepos.keys())

	print("=============== CHANGES ===============")
	remove = set(localRepos.keys()) - set(selected_repos)
	print("Remove:", list(remove))

	add = set(selected_repos) - set(localRepos.keys())
	print("Add:", list(add))
	print("=======================================")

	if(len(remove) > 0 and not utils.prompt("WARNING: Removed repos will be deleted! Continue?", False)):
		print("Aborting!")
		return

	for repo in remove:
		shutil.rmtree(path.join(os.path.expanduser(CONFIG[selected_ws]), "src/" + repo))

	for repo in add:
		utils.cloneRepo(remoteRepos[repo]['ssh_url'], path.join(os.path.expanduser(CONFIG[selected_ws]), "src/" + repo))


tools = {
	'setup': setup,
	'eclipse': eclipse,
	'repos': repos,
	'init': init,
}


def checkConfig(key):
	if(key in CONFIG.keys()):
		return True

	print("{} not set, please run `cnctools init` first.".format(key))
	return False

def readConfig():
	configPath = path.expanduser(CONFIG_PATH)

	if(path.exists(configPath)):
		configFile = open(configPath, "r+")
	else:
		return dict()

	config = json.load(configFile)
	configFile.close()
	return config

def saveConfig():
	configPath = path.expanduser(CONFIG_PATH)
	configFile = open(configPath, "w+")
	json.dump(CONFIG, configFile, indent=4) # dump with pretty print
	configFile.close()

CONFIG = readConfig()

# Main Script

parser = argparse.ArgumentParser(description="Tools that help us getting boring stuff done.")
parser.add_argument('tool', choices=tools.keys(), type=str, help="the name of the tool")
parser.add_argument('args', nargs=argparse.REMAINDER, type=str, help="args for the tool, see <tool> -h")

args = parser.parse_args()

# run tool
if args.tool in tools:
	tools[args.tool](args.args)
