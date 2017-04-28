#!/bin/sh

sudo apt install python3-pip
pip3 install urwid pystache

chmod +x cnctools.py
sudo ln -s ${PWD}/cnctools.py /usr/local/bin/cnctools
