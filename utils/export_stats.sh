#!/bin/sh
./see_stats.py -u http://sokobot.googlecode.com/svn/trunk/ >../export/html/stats_num_visited.html
./see_stats.py -m cost -u http://sokobot.googlecode.com/svn/trunk/ >../export/html/stats_cost.html
