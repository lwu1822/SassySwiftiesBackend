#!/bin/bash
# run this in the local repository to update website
docker-compose kill
git pull
docker-compose build --no-cache
docker-compose up -d --remove-orphans