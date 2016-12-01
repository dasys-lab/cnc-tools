#!/usr/bin/env python3

import argparse
import os
from subprocess import call

CWD = os.getcwd()

# TODO: Make it possible to call cntools from everywhere(no ./script/...)
# In shell you can do `dirname $0` to get the scripts path
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

def eclipse(args):
	eargs = ['./scripts/eclipse.sh']
	eargs.extend(args)
	call(eargs)


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
	'setup': setup,
	'eclipse': eclipse
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
