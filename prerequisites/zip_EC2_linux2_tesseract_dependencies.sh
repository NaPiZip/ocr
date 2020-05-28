#!/bin/bash

mkdir tesseract-lambda
pushd tesseract-lambda

cp /usr/local/bin/tesseract .

mkdir lib
cd lib

cp /usr/local/lib/libtesseract.so.4.0.1 .
cp /usr/local/lib/libtesseract.so.4 .

cp /usr/local/lib/liblept.so.5.0.4 .
cp /usr/local/lib/liblept.so.5 .

cp /usr/lib64/libpng15.so.15.13.0 .
cp /usr/lib64/libpng15.so.15 .

cd ..

mkdir tessdata
cd tessdata

cp /usr/local/share/tessdata/deu.traineddata .
cp /usr/local/share/tessdata/eng.traineddata .

popd
zip -r tesseract-lambda.zip tesseract-lambda
