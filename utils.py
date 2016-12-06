#!/usr/bin/env python3

import urllib.request
import json
import os
import urwid
import copy
import operator

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
	return data

def showMultiSelection(title, entries, selectedKeys = [], selectedLabels = []):
	"""Shows a fullscreen selection for multiple items.
	args:
		title - Selection title
		entries - dict of entries, format: { key: label }
	returns:
		a list containing the keys of the selected items
	"""

	out = copy.deepcopy(selectedKeys)

	# create footer
	footer = urwid.Text("Select with <LMB> or <space>, hit <return> when finished.")

	# create list body
	body = []

	for key, label in entries:
		if(label in selectedLabels):
			out.append(key)

		checkbox = urwid.CheckBox(label, key in out)
		urwid.connect_signal(checkbox, 'change', item_chosen, (key, out))
		body.append(urwid.AttrMap(checkbox, None, focus_map='reversed'))

	body.append(urwid.Divider())

	# create ListBox
	listWalker = urwid.SimpleFocusListWalker(body)
	listBox = urwid.ListBox(listWalker)

	# create frame
	frame = urwid.Frame(
		urwid.LineBox(
			listBox,
			title
		),
		footer=footer
	)

	main = urwid.Padding(
		frame,
		left=2,
		right=2
	)

	# start urwid loop
	urwid.MainLoop(main, input_filter=filterEnter, palette=[('reversed', 'standout', '')]).run()

	# get labels of selected items
	labels = list(filter(lambda x: x[0] in out, entries))
	labels = list(map(lambda x: x[1], labels))

	# print selection titles
	print("Selection - {}: {}".format(title, labels))

	# return list with keys
	return out

def filterEnter(keys, raw):
	if("enter" in keys):
		raise urwid.ExitMainLoop()
	else:
		return keys


def item_chosen(checkbox, new_state, data):
	(key, out) = data
	if(new_state):
		out.append(key)
	else:
		out.remove(key)
