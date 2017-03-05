#!/bin/bash

# Place your compile and execute script here.
# You can write any bash script that will run on campus linux machines.
# The below script will compile and execute the HelloEC program.
# HelloEC will also be passed the first argument to this script, a config file.
configFile=$1

python3 src/hw1c.py $configFile
# ./HelloEC $configFile
