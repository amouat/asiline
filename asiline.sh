#!/bin/bash

if [ -f "${1}" ]; then
  docker run -v $(pwd)/$1:/data.asi asiline /data.asi
else
  echo "$1 is not a file"
fi
