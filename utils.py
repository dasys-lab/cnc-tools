#!/usr/bin/env python3

import urllib.request
import json
import os
import urwid

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

def getGithubRepos(username):
	resp = urllib.request.urlopen("https://api.github.com/users/carpe-noctem-cassel/repos").read().decode("utf-8")
	data = json.loads(resp)

	entries = list(map(lambda x: x['name'], data))

	main = urwid.Padding(urwid.Frame(urwid.LineBox(menu(entries), u'GitHub Repositories'), footer=urwid.Columns([urwid.Button("Select (space)"), urwid.Button("Finish (return)")], dividechars=2)), left=4, right=4)
	top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
		align='center', width=('relative', 100),
		valign='middle', height=('relative', 100),
		min_width=20, min_height=9)
	urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()

	return data

def showSelection(entries):
	selection = 0
	while(True):
		clearTerminal()
		num = 0
		for entry in entries:
			print("[{}] {}".format("x" if num == selection else " ", entry))
			num += 1

		inp = getKey()
		if(inp == 'k'):
			selection = max(0, selection - 1)
		elif(inp == 'i'):
			selection = min(len(entries) - 1, selection + 1)

def menu(choices):
	body = []
	for c in choices:
		checkbox = urwid.CheckBox(c)
		urwid.connect_signal(checkbox, 'change', item_chosen, c)
		body.append(urwid.AttrMap(checkbox, None, focus_map='reversed'))

	body.append(urwid.Divider())
	return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(checkbox, new_state, choice):
	response = urwid.Text([u'You chose ', choice, u'\n'])
	done = urwid.Button(u'Ok')
	urwid.connect_signal(done, 'click', exit_program)
	#main.original_widget = urwid.Filler(urwid.Pile([response,
	#	urwid.AttrMap(done, None, focus_map='reversed')]))

def exit_program(button):
	raise urwid.ExitMainLoop()