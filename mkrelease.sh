#!/bin/bash
VERSION=1.6
zip -9rv praatalign_$VERSION.zip *.{praat,py,md} {install,par,LICENCE}*
tar -cvf praatalign_$VERSION.tar *.{praat,py,md} {install,par,LICENCE}*
xz -ve praatalign_$VERSION.tar
