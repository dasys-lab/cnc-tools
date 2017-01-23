#!/usr/bin/env python3

import copy
from functools import partial
import json
import operator
import os
from os import path
from subprocess import call
import urllib.request
import urwid
import weakref
from collections import OrderedDict

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

def cloneRepo(url, dest):
	call(['git', 'clone', url, dest])

# ========== TUI ==========

def showSelection(title, entries):
	out = [None]

	# create footer
	footer = urwid.Text("Select with <LMB> or <space> or <return>.")

	# create list body
	body = []

	for key, label in entries:
		button = urwid.Button(label)
		urwid.connect_signal(button, 'click', selectionButtonClicked, user_args=[(key, label), out])
		body.append(urwid.AttrMap(button, None, focus_map='reversed'))

	body.append(urwid.Divider())

	main = createListFrame(title, body, footer)

	# start urwid loop
	urwid.MainLoop(main, palette=[('reversed', 'standout', '')]).run()

	# print selection titles
	print("Selection - {}: {}".format(title, out[0][1]))

	# return list with keys
	return out[0][0]


def selectionButtonClicked(choice, out, button):
	out[0] = choice
	raise urwid.ExitMainLoop()

def createListFrame(title, body, footer):
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

	return main

def showMultiSelection(title, entries, selectedKeys = [], selectedLabels = []):
	"""Shows a fullscreen selection for multiple items.
	args:
		title - Selection title
		entries - dict of entries, format: { key: label }
	returns:
		a list containing the keys of the selected items
	"""

	out = []
	out.extend(selectedKeys)

	# create footer
	footer = urwid.Text("Select with <LMB> or <space>, hit <return> when finished.")

	# create list body
	body = []

	for key, label in entries.items():
		if(label in selectedLabels):
			out.append(key)

		checkbox = urwid.CheckBox(label, key in out)
		urwid.connect_signal(checkbox, 'change', multiselectionCheckboxChanged, user_args=[key, out])
		body.append(urwid.AttrMap(checkbox, None, focus_map='reversed'))

	body.append(urwid.Divider())

	main = createListFrame(title, body, footer)

	# start urwid loop
	urwid.MainLoop(main, input_filter=filterEnter, palette=[('reversed', 'standout', '')]).run()

	# get labels of selected items
	labels = list(filter(lambda x: x[0] in out, entries.items()))
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

def multiselectionCheckboxChanged(key, out, checkbox, new_state):
	if(new_state):
		out.append(key)
	else:
		out.remove(key)
