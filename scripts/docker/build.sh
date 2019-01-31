#!/bin/bash

NAME="sphere/prod"
VERSION=$1

###############################################################################
if [[ "$VERSION" == "" ]]; then
    echo "./build.sh <version>";
    echo "example: ./build.sh 0.6";
    exit 1;
fi
if [[ ! -f "$VERSION.Dockerfile" ]]; then
    echo "No $VERSION.Dockerfile file";
    exit 2;
fi

###############################################################################
docker build -t "$NAME:$VERSION" -f "$VERSION.Dockerfile" .
ret=$?
if [[ $ret -eq 0 ]]; then

fi
