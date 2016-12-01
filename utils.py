#!/usr/bin/env python3

def prompt(text, default=False):
	answer = str.lower(input(text + " [" + ("Y" if default == True else "y") + "/" + ("N" if default == False else "n") + "] "))

	if(answer == 'y'):
		return True
	
	if(answer == 'n'):
		return False

	if(default != None and answer == ''):
		return default

	# wrong input, repeat
	return prompt("Type 'y' or 'n': ", default)
