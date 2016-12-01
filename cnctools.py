#!/usr/bin/env python3

import argparse
import os
from subprocess import call
import utils

CWD = os.getcwd()
DIR = os.path.dirname(os.path.realpath(__file__))

def setup(args):
	if(len(args) > 0):
		if(args[0] == 'msl'):
			if(utils.prompt("Do you really want to start the MSL setup?")):
				call(['sudo', DIR + '/scripts/msl-setup.sh'])

		elif(args[0] == 'ttb'):
			if(utils.prompt("Do you really want to start the MSL setup?")):
				call(['sudo', DIR + '/scripts/ttb-setup.sh'])
	else:
		print("Choose msl or ttb")


def eclipse(args):
	eargs = [DIR + '/scripts/eclipse.sh']
	eargs.extend(args)
	call(eargs)


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
