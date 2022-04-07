#!/usr/bin/env bash
# Remove all images created in a CI run
s3="playlist"
if [[ "$1"x = "$s3"x ]]; then
  docker image rm --force ci_db:latest ci_s1:latest ci_s3:latest ci_test:latest
else
  docker image rm --force ci_db:latest ci_s1:latest ci_s2:latest ci_test:latest
fi
