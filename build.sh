#!/usr/bin/env bash
gcc -lwiringPi -c -fPIC dht22.c -o dht22.o
gcc -lwiringPi -shared dht22.o -o dht22.so
