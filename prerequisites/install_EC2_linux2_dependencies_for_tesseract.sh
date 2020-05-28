#!/bin/bash

$leptonica_version=1.79.09

sudo yum install gcc gcc-c++ make -y
sudo yum install autoconf aclocal automake -y
sudo yum install libtool -y
sudo yum install libjpeg-devel libpng-devel libpng-devel libtiff-devel zlib-devel -y

wget https://github.com/DanBloomberg/leptonica/releases/download/1.79.0/leptonica-1.79.0.tar.gz

tar -zxf leptonica-1.79.0.tar.gz 

