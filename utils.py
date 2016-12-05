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

	showSelection(entries)

	return data

def showSelection(entries):
	footer = urwid.Text("Select with <LMB> or <space>, hit <return> when finished.")

	# create list body
	
	body = []
	for c in entries:
		checkbox = urwid.CheckBox(c)
		urwid.connect_signal(checkbox, 'change', item_chosen, c)
		body.append(urwid.AttrMap(checkbox, None, focus_map='reversed'))

	body.append(urwid.Divider())

	listWalker = urwid.SimpleFocusListWalker(body)
	listBox = urwid.ListBox(listWalker)

	frame = urwid.Frame(
		urwid.LineBox(
			listBox,
			u'GitHub Repositories'
		),
		footer=footer
	)

	main = urwid.Padding(
		frame,
		left=2,
		right=2
	)

	urwid.MainLoop(main, input_filter=filterEnter, palette=[('reversed', 'standout', '')]).run()
	print("Selection finished")

def filterEnter(keys, raw):
	if("enter" in keys):
		raise urwid.ExitMainLoop()
	else:
		return keys


def item_chosen(checkbox, new_state, choice):
	response = urwid.Text([u'You chose ', choice, u'\n'])
	done = urwid.Button(u'Ok')
	#urwid.connect_signal(done, 'click', exit_program)
	#main.original_widget = urwid.Filler(urwid.Pile([response,
	#	urwid.AttrMap(done, None, focus_map='reversed')]))
