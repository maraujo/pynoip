#!/bin/sh
#Use this in a cron tab
curl -i -H "Content-Type: application/json" -X POST -d '{"label":"casa -p 2222"}' 'http://noip.smellium.com/'
