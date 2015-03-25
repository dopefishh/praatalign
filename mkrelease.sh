#!/bin/bash
VERSION=1.31
zip -9rv praatalign_$VERSION.zip *.{praat,py,md} {install,par,LICENCE}*
tar -cvf praatalign_$VERSION.tar *.{praat,py,md} {install,par,LICENCE}*
gzip -vv9c praatalign_$VERSION.tar > praatalign_$VERSION.tar.gz
bzip2 -vv9c praatalign_$VERSION.tar > praatalign_$VERSION.tar.bz2
xz -vvec praatalign_$VERSION.tar > praatalign_$VERSION.tar.xz
rm praatalign_$VERSION.tar
