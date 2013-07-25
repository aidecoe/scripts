#!/bin/sh
#
# Makes msmtp to read "From:" field and to use corresponding account
#
/usr/bin/msmtp --read-envelope-from -t $@
