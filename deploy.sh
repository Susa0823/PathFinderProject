#! /bin/bash

psql -V > /dev/null 2>&1

ssh -o StrictHostKeyChecking=no root@143.198.222.14 << 'INITSSH'
    cd /PathFinder
    docker login -u $CI_REGISTRY_USER -p $CI_JOB_TOKEN $CI_REGISTRY
    docker pull $IMAGE:web
    docker-compose -f docker-compose.yml up -d
INITSSH
# `$?` for the exit status of the last command
echo "This deploy script is under development ¯\(°_o)/¯"