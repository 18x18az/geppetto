#!/usr/bin/env sh
xset -dpms
xset s off
xset s noblank

while true; do
	unclutter &
	cd /home/admin/geppetto && /usr/bin/python display.py
	sleep 5
done
