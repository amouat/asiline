#!/bin/bash
#Wrapper script for asiline that calls docker image with file input
set -e

if [[ $# == 1 ]]; then 
  #get full path
  FILENAME=$(basename $1) 
  ABSFILE=$( cd $(dirname $1); pwd)/$FILENAME
  if [ -f "${ABSFILE}" ]; then
    docker run -v $ABSFILE:/input.asiline amouat/asiline /input.asiline
  else
    echo "$1 is not a file"
  fi
else
  echo "$0 expects exactly one file argument"
  exit 1
fi
