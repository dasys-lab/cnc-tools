cnctpath="$(dirname $0)/.."
econf="$cnctpath/data/eclipse/language.settings.xml"

if [ -z "$1" ]
then
	echo "usage: $0 workspace"
	exit 1
fi

workspace="$1"
buildfolder="$workspace/build"

if [ ! -d "$buildfolder" ]
then
	echo "$buildfolder does not exist!"
	exit 1
fi

for pro in $buildfolder/*
do
	settings="$pro/.settings"

	mkdir -p "$settings"
	cp "$econf" "$settings"
done


