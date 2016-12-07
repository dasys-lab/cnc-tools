#!/bin/sh

sudo apt install python3-urwid

chmod +x cnctools.py
sudo ln -s ${PWD}/cnctools.py /usr/local/bin/cnctools
