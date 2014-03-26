#!/bin/bash
cd Resources
for a in [A-Z] ; do echo $a : $(ls -1 $a|wc -l); done
find . -type f -iname '*jpg' |wc -l

