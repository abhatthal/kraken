#!/bin/bash
kill $(echo $(ps -ef | grep bot.py) | awk '{print $2}')
