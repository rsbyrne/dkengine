#!/bin/bash
currentDir=$PWD
cd "$(dirname "$0")"
# sh push.sh
docker build -t rsbyrne/dkengine:latest .
docker push rsbyrne/dkengine:latest
cd $currentDir
