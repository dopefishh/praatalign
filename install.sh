#!/bin/bash
set -e
case "$OSTYPE" in
	solaris* | *bsd* | linux*)
		echo "Detected LINUX/SOLARIS/BSD"
		dir="$HOME/.praat-dir/plugin_pralign/"
		;;
	darwin*)
		echo "Detected MAC"
		dir="$HOME/Library/Preferences/Praat Prefs/plugin_pralign"
		;;
	msys* | win32*)
		echo "You are running windows? Please run install_win.bat"
		exit 2
		;;
	*)
		echo "Unknown operating system..."
		exit 2
esac
scriptdir="$(cd "$(dirname "$0")" && pwd)"

set -x
mkdir -p "$dir"
rm -r "$dir"/* || true
cp -R "$scriptdir/"*.{py,praat} "$dir"
cp -R "$scriptdir/"par.* "$dir"
set +x
echo "Installing complete"
