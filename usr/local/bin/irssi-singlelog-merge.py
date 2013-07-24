#!/usr/bin/env python
# -*- coding: utf-8 -*-

# irssi-singlelog-merge.py - Merges two single irssi log files
# 
# Copyright (C) 2011  Amadeusz Żołnowski <aidecoe@aidecoe.name>
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.


# USAGE: irssi-singlelog-merge.py file1.log file2.log > merged.log
#
# It works only for default format.


import sys
from datetime import datetime


def cmp_lines(lines, static):
    if lines[0] == lines[1]:
        return None

    for i in (0, 1):
        if lines[i][:3] == '---':
            if lines[i][:14] in ('--- Log opened', '--- Log closed'):
                return i
            elif lines[i][:15] == '--- Day changed':
                if lines[i] != static['day']:
                    static['day'] = lines[i]
                    return i
                else:
                    # Skip -- Day changed line
                    lines[0] = lines[i-1]
                    return None

    times = [datetime.strptime(line[:5], '%H:%M') \
            for line in lines]

    if times[0] <= times[1]:
        return 0

    return 1


def main():
    logfiles = None
    try:
        logfiles = (open(sys.argv[1], 'r'), open(sys.argv[2], 'r'))
    except IndexError:
        print 'USAGE: irssi-singlelog-merge.py file1.log file2.log > merged.log'
        return 1

    out = []

    static = {
            'day' : ''
            }

    try:
        lines = [logfiles[0].readline(), logfiles[1].readline()]

        while all(lines):
            winner = cmp_lines(lines, static)

            if winner is None:
                out.append((None, lines[0]))
                lines = [logfiles[0].readline(), logfiles[1].readline()]
            else:
                out.append((winner, lines[winner]))
                lines[winner] = logfiles[winner].readline()

        if any(lines):
            for i in (0, 1):
                if lines[i]:
                    out.append((i, lines[i]))
                    out.extend([(i, line) for line in logfiles[i].readlines()])
                    break
    finally:
        for i in (0, 1):
            logfiles[i].close()


    for (x, line) in out:
        print line,

    return 0

if __name__ == '__main__':
    sys.exit(main())
