#!/bin/sh
cnctpath="$(dirname $0)/.."
econf="$cnctpath/data/eclipse/language.settings.xml"

if [ -z "$1" ]
then
	echo "usage: $0 cnws"
	exit 1
fi

workspace="$1"
buildfolder="$workspace/build"

if [ ! -d "$buildfolder" ]
then
	echo "$buildfolder does not exist!"
	exit 1
fi

echo "copying eclipse config into $buildfolder"
for pro in $buildfolder/*
do
	settings="$pro/.settings"
	mkdir -p "$settings"
	cp "$econf" "$settings"
	
done

echo "fixing _cplusplus defines"
ldir="$PWD"
cd "$buildfolder"
find ./ -type f -readable -writable -exec sed -i "s/199711L/201103L/g" {} \;
cd "$ldir"

echo "done"
