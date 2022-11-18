#!/bin/sh

# make the file executable "chmod +x ./automation.sh"
# and start it after boot 

# or  create a coron command 
# 1 * * * * bash /link-to-this-file


# only pulling from the backend for now
cd /home/greengang/Desktop/project-backtrack
git pull
