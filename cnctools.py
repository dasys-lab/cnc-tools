#!/usr/bin/env python3

import argparse
import os
from subprocess import call

CWD = os.getcwd()

def setup(args):
	if(len(args) > 0):
		if(args[0] == 'msl'):
			if(prompt("Do you really want to start the MSL setup?")):
				call(['sudo', './scripts/msl-setup.sh'])

		elif(args[0] == 'ttb'):
			if(prompt("Do you really want to start the MSL setup?")):
				call(['sudo', './scripts/ttb-setup.sh'])
	else:
		print("Choose msl, ttb or msl-robot")


def prompt(text, default=False):
	answer = str.lower(input(text + " [" + ("Y" if default else "y") + "/" + ("n" if default else "N") + "] "))

	if(answer == 'y'):
		return True
	
	if(answer == 'n'):
		return False

	if(answer == ''):
		return default

	# wrong input, repeat
	return prompt(text, default)


tools = {
	'setup': setup
}


# Main Script

parser = argparse.ArgumentParser(description="Tools that help us getting boring stuff done.")
parser.add_argument('tool', choices=tools.keys(), type=str, help="the name of the tool")
parser.add_argument('args', nargs=argparse.REMAINDER, type=str, help="args for the tool, see <tool> -h")

args = parser.parse_args()
print("Tool:", args.tool)
print("Args:", args.args)

# run tool
if args.tool in tools:
	tools[args.tool](args.args)
